#!/usr/bin/env python3
"""One-click setup for message transport mode and real-time delivery.

[INPUT]: SDKConfig, service_manager, credential_store, secrets, json
[OUTPUT]: Configured settings.json + openclaw.json + HEARTBEAT.md + installed or removed
          ws_listener service according to the selected message transport mode
[POS]: Automation script that bridges the gap between Skill installation and real-time
       message delivery — configures transport mode, OpenClaw hooks, listener settings,
       heartbeat checklist, and background service

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating

Idempotent design: safe to run multiple times. Existing config is merged, not overwritten.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import secrets
import sys
from pathlib import Path
from typing import Any

_scripts_dir = os.path.dirname(os.path.abspath(__file__))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from message_daemon import DEFAULT_LOCAL_DAEMON_HOST, DEFAULT_LOCAL_DAEMON_PORT
from message_transport import RECEIVE_MODE_HTTP, RECEIVE_MODE_WEBSOCKET, write_receive_mode
from service_manager import get_service_manager
from utils.config import SDKConfig
from utils.logging_config import configure_logging

logger = logging.getLogger("setup_realtime")

# Template token placeholder (from settings.example.json)
_TOKEN_PLACEHOLDER = "<run: echo awiki_$(openssl rand -hex 32)>"

# OpenClaw default gateway port
_OPENCLAW_GATEWAY_PORT = 18789


def _generate_token() -> str:
    """Generate a secure webhook token with awiki_ prefix."""
    return f"awiki_{secrets.token_hex(32)}"


def _generate_local_daemon_token() -> str:
    """Generate a secure token for localhost daemon requests."""
    return f"awiki_local_{secrets.token_hex(24)}"


def _is_placeholder_token(token: str) -> bool:
    """Check if a token is a template placeholder rather than a real value."""
    return not token or token.startswith("<") or token == "changeme"


def _openclaw_config_path() -> Path:
    """Return the path to OpenClaw's config file."""
    return Path.home() / ".openclaw" / "openclaw.json"


def _load_json(path: Path) -> dict[str, Any]:
    """Load a JSON file, returning empty dict if missing or invalid."""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read %s: %s", path, exc)
        return {}


def _save_json(path: Path, data: dict[str, Any], secure: bool = False) -> None:
    """Save a JSON file, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if secure:
        path.chmod(0o600)


def _resolve_token(settings_data: dict[str, Any], openclaw_data: dict[str, Any]) -> str:
    """Resolve the webhook token: reuse existing or generate new.

    Priority: settings.json listener.webhook_token > openclaw.json hooks.token > generate new.
    """
    # Check settings.json
    listener = settings_data.get("listener", {})
    token = listener.get("webhook_token", "")
    if token and not _is_placeholder_token(token):
        return token

    # Check openclaw.json
    hooks = openclaw_data.get("hooks", {})
    token = hooks.get("token", "")
    if token and not _is_placeholder_token(token):
        return token

    # Generate new
    return _generate_token()


def _resolve_local_daemon_token(settings_data: dict[str, Any]) -> str:
    """Resolve the local daemon token from settings or generate a new one."""
    token = (
        settings_data.get("message_transport", {}).get("local_daemon_token", "")
    )
    if token and not _is_placeholder_token(token):
        return token
    return _generate_local_daemon_token()


def setup_settings(
    config: SDKConfig,
    token: str,
    receive_mode: str,
    local_daemon_token: str,
) -> dict[str, Any]:
    """Create or update <DATA_DIR>/config/settings.json with listener config.

    Returns a status dict.
    """
    settings_path = config.data_dir / "config" / "settings.json"
    data = _load_json(settings_path)
    created = not settings_path.exists()

    # Set top-level service URLs if missing
    data.setdefault("user_service_url", config.user_service_url)
    data.setdefault("molt_message_url", config.molt_message_url)
    data.setdefault("did_domain", config.did_domain)

    # Merge listener config
    listener = data.get("listener", {})
    listener.setdefault("mode", "smart")
    listener.setdefault(
        "agent_webhook_url",
        f"http://127.0.0.1:{_OPENCLAW_GATEWAY_PORT}/hooks/agent",
    )
    listener.setdefault(
        "wake_webhook_url",
        f"http://127.0.0.1:{_OPENCLAW_GATEWAY_PORT}/hooks/wake",
    )
    listener["webhook_token"] = token  # Always sync token
    listener.setdefault("agent_hook_name", "IM")
    listener.setdefault("routing", {
        "whitelist_dids": [],
        "private_always_agent": True,
        "command_prefix": "/",
        "keywords": ["urgent", "approval", "payment", "alert"],
        "bot_names": [],
        "blacklist_dids": [],
    })
    listener.setdefault("e2ee_save_interval", 30.0)
    listener.setdefault("e2ee_decrypt_fail_action", "drop")
    data["listener"] = listener
    data["message_transport"] = {
        **data.get("message_transport", {}),
        "receive_mode": receive_mode,
        "local_daemon_host": data.get("message_transport", {}).get(
            "local_daemon_host", DEFAULT_LOCAL_DAEMON_HOST
        ),
        "local_daemon_port": int(
            data.get("message_transport", {}).get(
                "local_daemon_port", DEFAULT_LOCAL_DAEMON_PORT
            )
        ),
        "local_daemon_token": local_daemon_token,
    }

    _save_json(settings_path, data)

    return {
        "status": "ok",
        "action": "created" if created else "updated",
        "path": str(settings_path),
    }


def setup_openclaw_hooks(token: str) -> dict[str, Any]:
    """Create or update ~/.openclaw/openclaw.json with hooks config.

    Returns a status dict.
    """
    config_path = _openclaw_config_path()
    data = _load_json(config_path)
    created = not config_path.exists()

    # Merge hooks config (preserve other top-level keys)
    hooks = data.get("hooks", {})
    hooks["enabled"] = True
    hooks["token"] = token
    hooks.setdefault("path", "/hooks")
    hooks.setdefault("defaultSessionKey", "hook:ingress")
    hooks.setdefault("allowRequestSessionKey", False)
    hooks.setdefault("allowedAgentIds", ["*"])
    data["hooks"] = hooks

    _save_json(config_path, data)

    return {
        "status": "ok",
        "action": "created" if created else "updated",
        "path": str(config_path),
    }


def setup_listener_service(credential: str) -> dict[str, Any]:
    """Install and start the ws_listener background service.

    Returns a status dict.
    """
    mgr = get_service_manager()
    current = mgr.status()

    if current.get("running"):
        return {
            "status": "ok",
            "action": "already_running",
            "detail": current,
        }

    if current.get("installed"):
        # Installed but not running — start it
        mgr.start()
        new_status = mgr.status()
        return {
            "status": "ok",
            "action": "started",
            "detail": new_status,
        }

    # Not installed — install (which also starts)
    mgr.install(credential, config_path=None, mode=None)
    new_status = mgr.status()
    return {
        "status": "ok",
        "action": "installed",
        "detail": new_status,
    }


def disable_listener_service() -> dict[str, Any]:
    """Stop and uninstall the ws_listener background service."""
    mgr = get_service_manager()
    current = mgr.status()
    if not current.get("installed"):
        return {
            "status": "ok",
            "action": "already_disabled",
            "detail": current,
        }
    try:
        if current.get("running"):
            mgr.stop()
    except Exception:
        logger.debug("Failed to stop listener before uninstall", exc_info=True)
    mgr.uninstall()
    return {
        "status": "ok",
        "action": "disabled",
        "detail": mgr.status(),
    }


# --- HEARTBEAT.md -----------------------------------------------------------

# Marker lines used to find the awiki section in HEARTBEAT.md
_HEARTBEAT_SECTION_START = "<!-- awiki-heartbeat-start -->"
_HEARTBEAT_SECTION_END = "<!-- awiki-heartbeat-end -->"


def _resolve_skill_dir() -> str:
    """Return the absolute path to the skill root (one level above scripts/)."""
    return str(Path(__file__).resolve().parent.parent)


def _build_heartbeat_section(skill_dir: str) -> str:
    """Build the awiki heartbeat section content."""
    return f"""{_HEARTBEAT_SECTION_START}
## awiki — DID messaging (every heartbeat)

- Run: `cd {skill_dir} && python scripts/check_status.py`
- If `inbox.messages` has items: surface unread messages to user.
- If `identity.status != "ok"`: alert user.
- If `realtime_listener.running == false`: run `cd {skill_dir} && python scripts/setup_realtime.py` to restart.
{_HEARTBEAT_SECTION_END}"""


def _openclaw_workspace_dir() -> Path:
    """Return the OpenClaw workspace directory.

    Priority: OPENCLAW_WORKSPACE env > ~/.openclaw/workspace
    """
    env = os.environ.get("OPENCLAW_WORKSPACE")
    if env:
        return Path(env)
    return Path.home() / ".openclaw" / "workspace"


def setup_heartbeat() -> dict[str, Any]:
    """Create or update HEARTBEAT.md in the OpenClaw workspace.

    If the file doesn't exist, creates it with the awiki section.
    If it exists, replaces the awiki section (between marker comments)
    or appends it if no marker is found.

    Returns a status dict.
    """
    workspace = _openclaw_workspace_dir()
    heartbeat_path = workspace / "HEARTBEAT.md"
    skill_dir = _resolve_skill_dir()
    new_section = _build_heartbeat_section(skill_dir)

    if not heartbeat_path.exists():
        # Create new file
        workspace.mkdir(parents=True, exist_ok=True)
        content = f"# Heartbeat checklist\n\n{new_section}\n"
        heartbeat_path.write_text(content, encoding="utf-8")
        return {
            "status": "ok",
            "action": "created",
            "path": str(heartbeat_path),
        }

    # File exists — read and update
    existing = heartbeat_path.read_text(encoding="utf-8")

    if _HEARTBEAT_SECTION_START in existing and _HEARTBEAT_SECTION_END in existing:
        # Replace existing awiki section
        start_idx = existing.index(_HEARTBEAT_SECTION_START)
        end_idx = existing.index(_HEARTBEAT_SECTION_END) + len(_HEARTBEAT_SECTION_END)
        updated = existing[:start_idx] + new_section + existing[end_idx:]
        heartbeat_path.write_text(updated, encoding="utf-8")
        return {
            "status": "ok",
            "action": "updated",
            "path": str(heartbeat_path),
        }

    # No marker found — append
    separator = "\n" if existing.endswith("\n") else "\n\n"
    heartbeat_path.write_text(
        existing + separator + new_section + "\n",
        encoding="utf-8",
    )
    return {
        "status": "ok",
        "action": "appended",
        "path": str(heartbeat_path),
    }


def setup_realtime(
    credential_name: str = "default",
    receive_mode: str = RECEIVE_MODE_WEBSOCKET,
) -> dict[str, Any]:
    """Run the full message transport setup pipeline.

    Steps:
    1. Resolve or generate webhook token
    2. Create/update settings.json with transport mode
    3. Create/update openclaw.json
    4. Install/start or disable ws_listener service
    5. Create/update HEARTBEAT.md in OpenClaw workspace

    Returns a JSON-serializable report.
    """
    config = SDKConfig()
    report: dict[str, Any] = {}
    if receive_mode not in (RECEIVE_MODE_HTTP, RECEIVE_MODE_WEBSOCKET):
        raise ValueError(f"Unsupported receive mode: {receive_mode}")

    # Load existing configs to resolve token
    settings_path = config.data_dir / "config" / "settings.json"
    settings_data = _load_json(settings_path)
    openclaw_data = _load_json(_openclaw_config_path())

    # 1. Resolve token
    token = _resolve_token(settings_data, openclaw_data)
    local_daemon_token = _resolve_local_daemon_token(settings_data)
    report["token_action"] = (
        "reused_existing" if token != _generate_token() else "generated_new"
    )
    # Re-check: if token was just generated, mark it
    existing_settings_token = settings_data.get("listener", {}).get("webhook_token", "")
    existing_openclaw_token = openclaw_data.get("hooks", {}).get("token", "")
    if (
        not _is_placeholder_token(existing_settings_token)
        or not _is_placeholder_token(existing_openclaw_token)
    ):
        report["token_action"] = "reused_existing"
    else:
        report["token_action"] = "generated_new"

    # 2. Settings
    report["settings"] = setup_settings(
        config,
        token,
        receive_mode,
        local_daemon_token,
    )
    write_receive_mode(
        receive_mode,
        config=config,
        extra_transport_fields={
            "local_daemon_host": DEFAULT_LOCAL_DAEMON_HOST,
            "local_daemon_port": DEFAULT_LOCAL_DAEMON_PORT,
            "local_daemon_token": local_daemon_token,
        },
    )

    # 3. OpenClaw hooks
    report["openclaw_hooks"] = setup_openclaw_hooks(token)

    # 4. Listener service
    if receive_mode == RECEIVE_MODE_WEBSOCKET:
        report["listener_service"] = setup_listener_service(credential_name)
    else:
        report["listener_service"] = disable_listener_service()

    # 5. HEARTBEAT.md
    report["heartbeat"] = setup_heartbeat()

    report["status"] = "ok"
    if receive_mode == RECEIVE_MODE_WEBSOCKET:
        report["summary"] = (
            "Message transport is configured for WebSocket mode. "
            "The WebSocket listener will receive messages instantly and forward them to OpenClaw."
        )
    else:
        report["summary"] = (
            "Message transport is configured for HTTP mode. "
            "The background WebSocket listener is disabled and message inbox flows will use HTTP RPC."
        )

    return report


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(
        description="One-click setup for real-time message delivery via WebSocket listener",
    )
    parser.add_argument(
        "--credential", default="default",
        help="Credential name (default: default)",
    )
    parser.add_argument(
        "--receive-mode",
        choices=(RECEIVE_MODE_WEBSOCKET, RECEIVE_MODE_HTTP),
        default=RECEIVE_MODE_WEBSOCKET,
        help="Message receive mode (default: websocket)",
    )
    args = parser.parse_args()

    report = setup_realtime(args.credential, args.receive_mode)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
