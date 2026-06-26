"""
ChatClaw Skill — Main Entry Point
Relays messages between ChatClaw cloud dashboard and local OpenClaw agent.

Lifecycle:
  on_enable(config)  — called by OpenClaw when the skill is enabled
  on_disable()       — called by OpenClaw when the skill is disabled
  __main__           — standalone mode for local testing
"""

import asyncio
import json
import logging
import os
import re
import sys
import websockets
from pathlib import Path

from relay_client import RelayClient
from gateway_client import GatewayClient, OPENCLAW_DATA_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("chatclaw-skill")

SESSION_KEY    = "chatclaw-bridge"
SESSIONS_FILE  = OPENCLAW_DATA_DIR / "agents" / "main" / "sessions" / "sessions.json"
CONFIG_FILE    = OPENCLAW_DATA_DIR / "openclaw.json"

# Production relay URL — users override via config_schema cloud_url field
PRODUCTION_RELAY_URL = "wss://api.sumeralabs.com"


async def get_session_tokens_from_json(session_key: str):
    """Returns (total_tokens, context_tokens) from sessions.json, or (0, 0) on failure."""
    try:
        with open(SESSIONS_FILE) as f:
            sessions = json.load(f)
        if session_key in sessions:
            s = sessions[session_key]
            input_tokens   = s.get("inputTokens", 0)
            output_tokens  = s.get("outputTokens", 0)
            context_tokens = s.get("contextTokens", 0)
            # Note: sessions.json "totalTokens" == inputTokens only — always sum manually
            total = input_tokens + output_tokens
            logger.info(
                f"[TOKENS] input={input_tokens}, output={output_tokens}, "
                f"total={total}, context={context_tokens}"
            )
            return total, context_tokens
        logger.warning(f"[TOKENS] Session key '{session_key}' not found in sessions.json")
        return 0, 0
    except FileNotFoundError:
        logger.warning(f"[TOKENS] sessions.json not found at {SESSIONS_FILE}")
        return 0, 0
    except Exception as e:
        logger.error(f"[TOKENS] Error reading sessions.json: {e}")
        return 0, 0


def _patch_openclaw_config() -> bool:
    """
    Ensures the /v1/chat/completions HTTP endpoint is enabled in openclaw.json.
    Idempotent — no-ops if already enabled, handles missing file gracefully.
    Returns True if the file was actually written (so on_disable can revert it).
    """
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
        else:
            cfg = {}

        # Check if already enabled — avoid unnecessary writes
        already_enabled = (
            cfg.get("gateway", {})
               .get("http", {})
               .get("endpoints", {})
               .get("chatCompletions", {})
               .get("enabled", False)
        )
        if already_enabled:
            logger.info("openclaw.json: chatCompletions already enabled, skipping patch")
            return False

        cfg.setdefault("gateway", {}) \
           .setdefault("http", {}) \
           .setdefault("endpoints", {}) \
           ["chatCompletions"] = {"enabled": True}

        # Write to temp file first, then atomic rename — prevents corruption
        tmp = CONFIG_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(cfg, indent=2))
        tmp.replace(CONFIG_FILE)
        logger.info("openclaw.json patched: chatCompletions enabled ✓")
        return True

    except PermissionError:
        logger.warning(
            "Could not patch openclaw.json (permission denied). "
            "Manually set gateway.http.endpoints.chatCompletions.enabled = true"
        )
        return False
    except Exception as e:
        logger.warning(
            f"Could not patch openclaw.json: {e}. "
            "Manually set gateway.http.endpoints.chatCompletions.enabled = true"
        )
        return False


_PLACEHOLDER_KEYS = {"", "ck_test_mvp_key_12345", "ck_your_key_here", "YOUR_API_KEY"}


class ChatClawSkill:
    def __init__(self, config: dict, context=None):
        api_key   = config.get("apiKey", "").strip()
        cloud_url = (config.get("cloud_url", "") or PRODUCTION_RELAY_URL).strip()
        if not api_key or api_key in _PLACEHOLDER_KEYS:
            raise RuntimeError(
                "ChatClaw API key not configured. "
                "Open your OpenClaw skill config and set 'apiKey' to the key from "
                "https://app.chatclaw.sumeralabs.com → Bot Settings."
            )
        self.relay   = RelayClient(cloud_url=cloud_url, api_key=api_key)
        self.gateway = GatewayClient()
        self._running = False

    async def start(self):
        self._running = True
        logger.info("ChatClaw skill starting...")
        while self._running:
            try:
                await asyncio.gather(
                    self.relay.connect(),
                    self.gateway.connect(),
                )
                logger.info("Both connections established — relaying messages ✓")
                await asyncio.gather(
                    self._cloud_to_gateway(),
                    self._drain_gateway(),
                )
            except websockets.ConnectionClosed as e:
                logger.warning(f"Connection lost ({e}). Reconnecting in 3s...")
                await asyncio.sleep(3)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Relay loop error: {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)

    async def _cloud_to_gateway(self):
        """Receives a message from the cloud relay, dispatches it to the appropriate handler:
        - files.list / files.get  → gateway RPC (file browsing)
        - anything with text      → HTTP SSE streaming chat
        """
        while self._running:
            message = await self.relay.receive()
            msg_type = message.get("type", "")

            # ── File listing ──────────────────────────────────────────────────
            if msg_type == "files.list":
                logger.info("[AUDIT] files.list requested")
                try:
                    files = await self.gateway.list_files()
                    logger.info(f"[AUDIT] files.list returned {len(files)} entries")
                    await self.relay.send({"type": "files.list.result", "files": files})
                except Exception as e:
                    logger.error(f"files.list error: {e}")
                    await self.relay.send({"type": "files.list.result", "files": [], "error": str(e)})
                continue

            # ── File content fetch ────────────────────────────────────────────
            if msg_type == "files.get":
                name = message.get("name", "")
                logger.info(f"[AUDIT] files.get requested: '{name}'")
                try:
                    file_data = await self.gateway.get_file(name=name)
                    if file_data:
                        await self.relay.send({
                            "type":    "files.get.result",
                            "name":    name,
                            "content": file_data.get("content", ""),
                        })
                    else:
                        await self.relay.send({
                            "type":    "files.get.result",
                            "name":    name,
                            "content": None,
                            "error":   "File not found",
                        })
                except Exception as e:
                    logger.error(f"files.get error for '{name}': {e}")
                    await self.relay.send({
                        "type":    "files.get.result",
                        "name":    name,
                        "content": None,
                        "error":   str(e),
                    })
                continue

            # ── Skills list ───────────────────────────────────────────────────
            if msg_type == "skills.list":
                try:
                    proc = await asyncio.create_subprocess_exec(
                        "openclaw", "skills", "list", "--json",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
                    output = stdout.decode().strip()
                    try:
                        skills_data = json.loads(output)
                        # Normalise: accept list or {skills: [...]}
                        if isinstance(skills_data, dict):
                            skills_list = skills_data.get("skills", list(skills_data.values()))
                        else:
                            skills_list = skills_data
                    except json.JSONDecodeError:
                        # Fallback: return raw text as single-item list so UI shows something
                        skills_list = [{"name": "raw", "raw": output}] if output else []
                    await self.relay.send({"type": "skills.list.result", "skills": skills_list})
                except asyncio.TimeoutError:
                    await self.relay.send({"type": "skills.list.result", "skills": [], "error": "Command timed out"})
                except Exception as e:
                    logger.error(f"skills.list error: {e}")
                    await self.relay.send({"type": "skills.list.result", "skills": [], "error": str(e)})
                continue

            # ── Skills enable / disable ───────────────────────────────────────
            if msg_type == "skills.set_enabled":
                name    = message.get("name", "")
                enabled = message.get("enabled", True)
                value   = "true" if enabled else "false"
                logger.info(f"[AUDIT] skills.set_enabled requested: '{name}' → enabled={enabled}")
                try:
                    proc = await asyncio.create_subprocess_exec(
                        "openclaw", "config", "set",
                        f"skills.entries.{name}.enabled", value,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
                    success = proc.returncode == 0
                    msg = stdout.decode().strip() or stderr.decode().strip() or ("OK" if success else "Failed")
                    await self.relay.send({"type": "skills.action.result", "success": success, "message": msg})
                except asyncio.TimeoutError:
                    await self.relay.send({"type": "skills.action.result", "success": False, "message": "Command timed out"})
                except Exception as e:
                    logger.error(f"skills.set_enabled error: {e}")
                    await self.relay.send({"type": "skills.action.result", "success": False, "message": str(e)})
                continue

            # ── Skills reinstall ──────────────────────────────────────────────
            if msg_type == "skills.reinstall":
                name = message.get("name", "")
                logger.info(f"[AUDIT] skills.reinstall requested: '{name}'")
                try:
                    proc = await asyncio.create_subprocess_exec(
                        "clawhub", "install", name, "--force",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
                    success = proc.returncode == 0
                    output  = (stdout.decode() + stderr.decode()).strip()
                    await self.relay.send({"type": "skills.action.result", "success": success, "message": output})
                except asyncio.TimeoutError:
                    await self.relay.send({"type": "skills.action.result", "success": False, "message": "Install timed out after 120s"})
                except Exception as e:
                    logger.error(f"skills.reinstall error: {e}")
                    await self.relay.send({"type": "skills.action.result", "success": False, "message": str(e)})
                continue

            # ── Cron list ─────────────────────────────────────────────────────
            if msg_type == "cron.list":
                try:
                    jobs = await self.gateway.cron_list()
                    await self.relay.send({"type": "cron.list.result", "jobs": jobs})
                except Exception as e:
                    logger.error(f"cron.list error: {e}")
                    await self.relay.send({"type": "cron.list.result", "jobs": [], "error": str(e)})
                continue

            # ── Cron add ──────────────────────────────────────────────────────
            if msg_type == "cron.add":
                name         = message.get("name", "")
                prompt       = message.get("message", "")
                schedule     = message.get("schedule", "")
                agent_id     = message.get("agentId", "main")
                logger.info(f"[AUDIT] cron.add requested: name='{name}' schedule='{schedule}'")
                try:
                    job = await self.gateway.cron_add(name, prompt, schedule, agent_id)
                    await self.relay.send({"type": "cron.add.result", "job": job})
                except Exception as e:
                    logger.error(f"cron.add error: {e}")
                    await self.relay.send({"type": "cron.add.result", "job": None, "error": str(e)})
                continue

            # ── Cron update ───────────────────────────────────────────────────
            if msg_type == "cron.update":
                job_id = message.get("id", "")
                patch  = message.get("patch", {})
                logger.info(f"[AUDIT] cron.update requested: id='{job_id}' patch={patch}")
                try:
                    job = await self.gateway.cron_update(job_id, patch)
                    await self.relay.send({"type": "cron.update.result", "job": job})
                except Exception as e:
                    logger.error(f"cron.update error: {e}")
                    await self.relay.send({"type": "cron.update.result", "job": None, "error": str(e)})
                continue

            # ── Cron remove ───────────────────────────────────────────────────
            if msg_type == "cron.remove":
                job_id = message.get("id", "")
                logger.info(f"[AUDIT] cron.remove requested: id='{job_id}'")
                try:
                    await self.gateway.cron_remove(job_id)
                    await self.relay.send({"type": "cron.remove.result", "id": job_id})
                except Exception as e:
                    logger.error(f"cron.remove error: {e}")
                    await self.relay.send({"type": "cron.remove.result", "id": job_id, "error": str(e)})
                continue

            # ── Cron trigger ──────────────────────────────────────────────────
            if msg_type == "cron.trigger":
                job_id = message.get("id", "")
                logger.info(f"[AUDIT] cron.trigger requested: id='{job_id}'")
                try:
                    result = await self.gateway.cron_run(job_id)
                    await self.relay.send({
                        "type":    "cron.trigger.result",
                        "ok":      result.get("ok", True),
                        "runId":   result.get("runId"),
                        "enqueued": result.get("enqueued", True),
                    })
                except Exception as e:
                    logger.error(f"cron.trigger error: {e}")
                    await self.relay.send({"type": "cron.trigger.result", "ok": False, "error": str(e)})
                continue

            # ── Chat (text) ───────────────────────────────────────────────────
            text    = message.get("content") or message.get("text") or message.get("message", "")
            task_id = message.get("task_id")

            if not text:
                continue

            session_key = task_id if task_id else SESSION_KEY
            logger.info(f"Cloud → Gateway (SSE): {str(text)[:60]} (task_id={task_id})")

            full_text   = ""
            first_token = True
            try:
                async for delta in self.gateway.stream_chat(text, session_key=session_key):
                    if first_token:
                        # Signal that streaming has begun — frontend shows streaming bubble
                        await self.relay.send({
                            "type": "task.status",
                            "task_id": session_key,
                            "status": "streaming",
                        })
                        first_token = False
                    full_text += delta
                    await self.relay.send({
                        "type": "message.delta",
                        "text": delta,
                        "task_id": session_key,
                    })
            except Exception as e:
                logger.error(f"stream_chat error for task {session_key}: {e}")
                await self.relay.send({
                    "type": "task.status",
                    "task_id": session_key,
                    "status": "error",
                })
                continue

            if not full_text:
                continue

            # Post-stream: strip LLM internal reasoning and wrapper tags.
            # Must run on the full accumulated string because tags can span multiple SSE chunks.
            for tag in ("think", "thinking", "reasoning", "scratchpad", "internal"):
                full_text = re.sub(
                    rf"<{tag}[^>]*>[\s\S]*?</{tag}>",
                    "",
                    full_text,
                    flags=re.IGNORECASE,
                )
            full_text = re.sub(
                r"</?(?:final|answer|response|output)[^>]*>",
                "",
                full_text,
                flags=re.IGNORECASE,
            )
            full_text = full_text.strip()

            # Read token counts from OpenClaw's sessions.json file.
            # sessions_key includes the "agent:main:" prefix that OpenClaw uses internally.
            sessions_key = f"agent:main:{session_key}"
            total_tokens, context_tokens = await get_session_tokens_from_json(sessions_key)

            # If sessions.json was unavailable, report 0 — never fabricate a count
            if total_tokens == 0:
                logger.warning(
                    f"[TOKENS] Could not read token count for {sessions_key}. "
                    "Reporting 0 — sessions.json may not have been written yet."
                )

            logger.info(f"Gateway → Cloud (complete): {full_text[:60]} (task_id={session_key})")
            complete_payload = {
                "type":    "message.complete",
                "text":    full_text,
                "task_id": session_key,
                "tokens":  total_tokens,
            }
            if context_tokens > 0:
                complete_payload["context_tokens"] = context_tokens

            await self.relay.send(complete_payload)
            await self.relay.send({
                "type":    "task.status",
                "task_id": session_key,
                "status":  "idle",
            })

    async def _drain_gateway(self):
        """Drains the gateway WebSocket queue to prevent memory buildup.
        Chat is handled via HTTP SSE, so WS events from the gateway are not used.
        Raises on disconnect to trigger the outer reconnect loop in start()."""
        while self._running:
            await self.gateway.receive()

    async def stop(self):
        self._running = False
        await asyncio.gather(
            self.relay.close(),
            self.gateway.close(),
            return_exceptions=True,
        )
        logger.info("ChatClaw skill stopped ✓")


_skill_instance = None
_patched_chat_completions = False  # True only if on_enable wrote the config — on_disable reverts


async def on_enable(config: dict, context=None):
    """Called by OpenClaw when the skill is enabled via the Control UI."""
    global _skill_instance, _patched_chat_completions
    _patched_chat_completions = False

    # _patch_openclaw_config returns True if it actually wrote the file
    _patched_chat_completions = _patch_openclaw_config()

    _skill_instance = ChatClawSkill(config, context=context)
    await _skill_instance.start()


async def on_disable():
    """Called by OpenClaw when the skill is disabled via the Control UI."""
    global _skill_instance, _patched_chat_completions
    if _patched_chat_completions:
        try:
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
            cfg.get("gateway", {}).get("http", {}).get("endpoints", {}).pop("chatCompletions", None)
            tmp = CONFIG_FILE.with_suffix(".tmp")
            tmp.write_text(json.dumps(cfg, indent=2))
            tmp.replace(CONFIG_FILE)
            _patched_chat_completions = False
            logger.info("openclaw.json reverted: chatCompletions removed ✓")
        except Exception as e:
            logger.warning(f"Could not revert openclaw.json: {e}")
    if _skill_instance:
        await _skill_instance.stop()
        _skill_instance = None


if __name__ == "__main__":
    # Standalone mode: python main.py <api_key> [cloud_url]
    if len(sys.argv) < 2:
        print("Usage: python main.py <api_key> [cloud_url]", file=sys.stderr)
        print("Get your API key from https://app.chatclaw.sumeralabs.com → Bot Settings", file=sys.stderr)
        sys.exit(1)
    api_key   = sys.argv[1]
    cloud_url = sys.argv[2] if len(sys.argv) > 2 else PRODUCTION_RELAY_URL
    config    = {"apiKey": api_key, "cloud_url": cloud_url}
    logger.info(f"Starting standalone with key: {api_key[:10]}... → {cloud_url}")
    try:
        asyncio.run(on_enable(config))
    except KeyboardInterrupt:
        asyncio.run(on_disable())