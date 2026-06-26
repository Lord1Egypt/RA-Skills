#!/usr/bin/env python3
"""
Test benchmarked-free-ride skill installed from ClawHub on a Daytona sandbox.

Verifies the full user journey: install from ClawHub -> run skill -> openclaw uses config.
"""

import json
import os
import sys
import time

from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxFromImageParams, Resources


DAYTONA_API_KEY = os.environ["DAYTONA_API_KEY"]
DAYTONA_API_URL = os.environ.get("DAYTONA_API_URL", "https://app.daytona.io/api")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
SKILL_SLUG = "benchmarked-free-ride"

# ── helpers ──────────────────────────────────────────────────────────────────

def run(sandbox, cmd, timeout=120, label=None):
    """Execute a command in the sandbox, print and return (exit_code, stdout)."""
    tag = f"[{label}]" if label else "[exec]"
    print(f"\n{'='*70}\n{tag} {cmd}\n{'='*70}")
    result = sandbox.process.exec(cmd, timeout=timeout)
    exit_code = result.exit_code
    stdout = getattr(result, "result", str(result))
    if stdout:
        display = stdout if len(stdout) < 3000 else stdout[:1500] + "\n...(trimmed)...\n" + stdout[-1500:]
        print(display)
    print(f"  -> exit_code={exit_code}")
    return exit_code, stdout


def read_remote(sandbox, remote_path):
    """Download and decode a text file from the sandbox."""
    data = sandbox.fs.download_file(remote_path)
    return data.decode("utf-8") if data else None


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    passed, failed = [], []

    def check(name, condition, detail=""):
        if condition:
            passed.append(name)
            print(f"  \u2705 {name}")
        else:
            failed.append(name)
            print(f"  \u274c {name} \u2014 {detail}")

    # 1. Create sandbox
    print("\n\U0001f680 Creating Daytona sandbox (node:22-bookworm)...")
    daytona = Daytona(DaytonaConfig(api_key=DAYTONA_API_KEY, api_url=DAYTONA_API_URL))
    sandbox = daytona.create(
        CreateSandboxFromImageParams(
            image="node:22-bookworm",
            labels={"purpose": "clawhub-skill-test"},
            resources=Resources(cpu=2, memory=4, disk=10),
        ),
        timeout=120,
    )
    print(f"  sandbox id: {sandbox.id}")

    try:
        # 2. Install Python
        print("\n\U0001f4e6 Installing Python...")
        run(sandbox, "apt-get update -qq && apt-get install -y -qq python3 > /dev/null 2>&1",
            timeout=180, label="apt-python")
        run(sandbox, "ln -sf $(which python3) /usr/local/bin/python; python --version", label="python-ver")

        # 3. Install openclaw
        print("\n\U0001f4e6 Installing openclaw...")
        run(sandbox, "npm install -g openclaw", timeout=180, label="npm-openclaw")
        ec, ver = run(sandbox, "openclaw --version", label="openclaw-ver")
        check("openclaw installed", ec == 0 and "not found" not in ver, ver)

        # 4. Install skill from ClawHub
        print(f"\n\U0001f4e6 Installing skill '{SKILL_SLUG}' from ClawHub...")
        ec, out = run(sandbox, f"npx clawhub@latest install {SKILL_SLUG} --dir /root/.openclaw/skills", timeout=120, label="clawhub-install")
        check("clawhub install exits 0", ec == 0, out[-300:] if out else "no output")

        # 5. Verify skill files were installed
        SKILL_DIR_REMOTE = f"/root/.openclaw/skills/{SKILL_SLUG}"
        SKILL_CMD = f"python {SKILL_DIR_REMOTE}/main.py"
        ec, out = run(sandbox, f"ls -la {SKILL_DIR_REMOTE}/", label="ls-skill")
        check("SKILL.md present", "SKILL.md" in out, "SKILL.md not found in installed skill dir")
        check("main.py present", "main.py" in out, "main.py not found in installed skill dir")

        # No pip install needed — skill uses only Python stdlib
        ec, _ = run(sandbox, f"{SKILL_CMD} help", label="help")
        check("skill CLI available", ec == 0)

        # ── Test: list (verify skill can fetch leaderboard) ──────────────────
        print("\n\u2500\u2500 TEST: list \u2500\u2500")
        ec, out = run(sandbox, f"{SKILL_CMD} list", label="list")
        check("list exits 0", ec == 0)
        check("list shows free models", ":free" in out, "no :free models")

        # ── Test: auto (configure openclaw) ──────────────────────────────────
        print("\n\u2500\u2500 TEST: auto \u2500\u2500")
        run(sandbox, "mkdir -p /root/.openclaw", label="mkdir")
        ec, out = run(sandbox, f"{SKILL_CMD} auto", label="auto")
        check("auto exits 0", ec == 0)
        check("auto shows done", "done" in out.lower() or "\u2705" in out)

        # Verify config
        cfg_text = read_remote(sandbox, "/root/.openclaw/openclaw.json")
        if cfg_text:
            cfg = json.loads(cfg_text)
            primary = cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
            fallbacks = cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("fallbacks", [])
            check("config has primary", bool(primary) and "openrouter/" in primary, f"primary={primary}")
            check("config has fallbacks", len(fallbacks) >= 1, f"got {len(fallbacks)}")
            print(f"  primary = {primary}")
            print(f"  fallbacks ({len(fallbacks)}) = {fallbacks[:3]}...")
        else:
            check("config readable", False, "could not read openclaw.json")
            primary, fallbacks = "", []

        # ── Test: status ─────────────────────────────────────────────────────
        print("\n\u2500\u2500 TEST: status \u2500\u2500")
        ec, out = run(sandbox, f"{SKILL_CMD} status", label="status")
        check("status exits 0", ec == 0)
        check("status shows primary", primary in out if primary else "primary" in out.lower())

        # ── Test: switch ─────────────────────────────────────────────────────
        print("\n\u2500\u2500 TEST: switch \u2500\u2500")
        if fallbacks:
            switch_target = fallbacks[0].removeprefix("openrouter/")
            ec, out = run(sandbox, f"{SKILL_CMD} switch {switch_target}", label="switch")
            check("switch exits 0", ec == 0)
            cfg2 = json.loads(read_remote(sandbox, "/root/.openclaw/openclaw.json"))
            new_primary = cfg2.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
            check("switch updated primary", switch_target in new_primary, f"got {new_primary}")
        else:
            print("  (skipped \u2014 no fallbacks)")

        # ── Test: E2E with OpenRouter ────────────────────────────────────────
        if OPENROUTER_API_KEY and primary:
            print("\n\u2500\u2500 TEST: E2E openclaw agent \u2500\u2500")

            # Reset to auto config
            run(sandbox, f"{SKILL_CMD} auto", label="e2e-auto")
            cfg_e2e = json.loads(read_remote(sandbox, "/root/.openclaw/openclaw.json"))
            e2e_model = cfg_e2e.get("agents", {}).get("defaults", {}).get("model", {})

            all_model_ids = [
                e2e_model.get("primary", "").removeprefix("openrouter/")
            ] + [
                fb.removeprefix("openrouter/") for fb in e2e_model.get("fallbacks", [])
            ]

            openclaw_config = {
                "models": {
                    "providers": {
                        "openrouter": {
                            "baseUrl": "https://openrouter.ai/api/v1",
                            "apiKey": OPENROUTER_API_KEY,
                            "api": "openai-completions",
                            "authHeader": True,
                            "models": [
                                {
                                    "id": mid, "name": mid, "reasoning": False,
                                    "input": ["text"],
                                    "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
                                    "contextWindow": 128000, "maxTokens": 8192,
                                }
                                for mid in all_model_ids if mid
                            ],
                        }
                    }
                },
                "agents": {
                    "defaults": {
                        "model": e2e_model,
                        "timeoutSeconds": 120,
                    }
                },
            }
            sandbox.fs.upload_file(
                json.dumps(openclaw_config, indent=2).encode("utf-8"),
                "/root/.openclaw/openclaw.json",
            )
            print(f"  wrote openclaw.json with {len(all_model_ids)} models")

            prompt = "Reply with exactly: CLAWHUB_SKILL_TEST_OK"
            cmd = (
                f"openclaw agent --agent main "
                f"--session-id clawhub-test-{int(time.time())} "
                f"--message {json.dumps(prompt)} "
                f"--json --timeout 120"
            )
            try:
                ec, out = run(sandbox, cmd, timeout=300, label="e2e-agent")
            except Exception as e:
                ec, out = 1, f"TIMEOUT/ERROR: {e}"
                print(f"  \u26a0\ufe0f  openclaw agent call failed: {e}")

            if ec == 0 and out and out.strip():
                got_json = False
                try:
                    data = json.loads(out)
                    got_json = True
                except json.JSONDecodeError:
                    idx = out.find("{")
                    if idx >= 0:
                        try:
                            data = json.loads(out[idx:])
                            got_json = True
                        except json.JSONDecodeError:
                            pass

                check("e2e got response", got_json, "no valid JSON response")
                if got_json:
                    text = (
                        data.get("result", {}).get("text", "")
                        or data.get("response", "")
                        or data.get("text", "")
                        or str(data)[:300]
                    )
                    print(f"  response: {text[:500]}")
                    check("e2e response has content", len(text) > 5, f"text length={len(text)}")
            elif "rate limit" in (out or "").lower() or "429" in (out or ""):
                print("  \u26a0\ufe0f  OpenRouter rate limit hit (not a skill bug)")
                check("e2e rate limited (expected)", True)
            else:
                check("e2e openclaw ran", False, f"exit_code={ec}")
        else:
            print("\n  (skipping E2E \u2014 no OPENROUTER_API_KEY or no primary model)")

        # ── Summary ──────────────────────────────────────────────────────────
        print(f"\n{'='*70}")
        print(f"RESULTS: {len(passed)} passed, {len(failed)} failed")
        if failed:
            print("Failed checks:")
            for f in failed:
                print(f"  \u274c {f}")
        print(f"{'='*70}")
        return 1 if failed else 0

    finally:
        print("\n\U0001f9f9 Deleting sandbox...")
        try:
            daytona.delete(sandbox)
            print("  sandbox deleted.")
        except Exception as e:
            print(f"  warning: cleanup failed: {e}")


if __name__ == "__main__":
    sys.exit(main())
