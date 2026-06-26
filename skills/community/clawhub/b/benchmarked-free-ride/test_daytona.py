#!/usr/bin/env python3
"""
Test benchmarked-free-ride skill on a Daytona sandbox with real openclaw.

Spins up a sandbox, installs Node.js + openclaw + the skill, then runs
each command and verifies the output / config file.
"""

import json
import os
import sys
import time

from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxFromImageParams, Resources


DAYTONA_API_KEY = os.environ["DAYTONA_API_KEY"]
DAYTONA_API_URL = os.environ.get("DAYTONA_API_URL", "https://app.daytona.io/api")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))

# ── helpers ──────────────────────────────────────────────────────────────────

def run(sandbox, cmd, timeout=120, label=None):
    """Execute a command in the sandbox, print and return (exit_code, stdout)."""
    tag = f"[{label}]" if label else "[exec]"
    print(f"\n{'='*70}\n{tag} {cmd}\n{'='*70}")
    result = sandbox.process.exec(cmd, timeout=timeout)
    exit_code = result.exit_code
    stdout = getattr(result, "result", str(result))
    if stdout:
        # Trim very long output
        display = stdout if len(stdout) < 3000 else stdout[:1500] + "\n...(trimmed)...\n" + stdout[-1500:]
        print(display)
    print(f"  -> exit_code={exit_code}")
    return exit_code, stdout


def upload_file(sandbox, local_path, remote_path):
    """Upload a local file into the sandbox."""
    with open(local_path, "rb") as f:
        sandbox.fs.upload_file(f.read(), remote_path)
    print(f"  uploaded {local_path} -> {remote_path}")


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
            print(f"  ✅ {name}")
        else:
            failed.append(name)
            print(f"  ❌ {name} — {detail}")

    # 1. Create sandbox
    print("\n🚀 Creating Daytona sandbox (node:22-bookworm)...")
    daytona = Daytona(DaytonaConfig(api_key=DAYTONA_API_KEY, api_url=DAYTONA_API_URL))
    sandbox = daytona.create(
        CreateSandboxFromImageParams(
            image="node:22-bookworm",
            labels={"purpose": "free-ride-skill-test"},
            resources=Resources(cpu=2, memory=4, disk=10),
        ),
        timeout=120,
    )
    print(f"  sandbox id: {sandbox.id}")

    try:
        # 2. Install Python (the node image doesn't have it)
        print("\n📦 Installing Python...")
        run(sandbox, "apt-get update -qq && apt-get install -y -qq python3 > /dev/null 2>&1",
            timeout=180, label="apt-python")
        run(sandbox, "ln -sf $(which python3) /usr/local/bin/python; python --version", label="python-ver")

        # 3. Install openclaw
        print("\n📦 Installing openclaw...")
        run(sandbox, "npm install -g openclaw", timeout=180, label="npm")
        ec, ver = run(sandbox, "openclaw --version", label="version")
        check("openclaw installed", ec == 0 and "not found" not in ver, ver)

        # 4. Seed a minimal openclaw config so 'status' has something to show
        run(sandbox, "mkdir -p /root/.openclaw", label="mkdir")
        seed_config = {"agents": {"defaults": {"model": {"primary": "", "fallbacks": []}}}}
        sandbox.fs.upload_file(json.dumps(seed_config, indent=2).encode(), "/root/.openclaw/openclaw.json")

        # 5. Upload the skill (no pip install needed — stdlib only)
        SKILL_CMD = "python /opt/skill/main.py"
        print("\n📦 Uploading benchmarked-free-ride skill...")
        upload_file(sandbox, os.path.join(SKILL_DIR, "main.py"), "/opt/skill/main.py")
        ec, _ = run(sandbox, f"{SKILL_CMD} help", label="help")
        check("skill installed", ec == 0)

        # ── Test: list ───────────────────────────────────────────────────────
        print("\n── TEST: list ──")
        ec, out = run(sandbox, f"{SKILL_CMD} list", label="list")
        check("list exits 0", ec == 0)
        check("list shows models", ":free" in out, "no :free models in output")

        # ── Test: list --secure ──────────────────────────────────────────────
        print("\n── TEST: list --secure ──")
        ec, out = run(sandbox, f"{SKILL_CMD} list --secure", label="list-secure")
        check("list --secure exits 0", ec == 0)
        check("list --secure shows security", "security" in out.lower(), "no security label")

        # ── Test: refresh ────────────────────────────────────────────────────
        print("\n── TEST: refresh ──")
        ec, out = run(sandbox, f"{SKILL_CMD} refresh", label="refresh")
        check("refresh exits 0", ec == 0)
        check("refresh fetched models", "benchmarked free models" in out.lower())

        # ── Test: auto ───────────────────────────────────────────────────────
        print("\n── TEST: auto ──")
        ec, out = run(sandbox, f"{SKILL_CMD} auto", label="auto")
        check("auto exits 0", ec == 0)
        check("auto sets primary", "primary" in out.lower())
        check("auto shows done", "done" in out.lower() or "✅" in out)

        # Verify config was actually written
        cfg_text = read_remote(sandbox, "/root/.openclaw/openclaw.json")
        if cfg_text:
            cfg = json.loads(cfg_text)
            primary = cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
            fallbacks = cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("fallbacks", [])
            check("config has primary", bool(primary) and "openrouter/" in primary, f"primary={primary}")
            check("config has fallbacks", len(fallbacks) >= 1, f"got {len(fallbacks)} fallbacks")
            print(f"  primary = {primary}")
            print(f"  fallbacks = {fallbacks}")
        else:
            check("config readable", False, "could not read openclaw.json")

        # ── Test: status ─────────────────────────────────────────────────────
        print("\n── TEST: status ──")
        ec, out = run(sandbox, f"{SKILL_CMD} status", label="status")
        check("status exits 0", ec == 0)
        check("status shows primary", "primary" in out.lower())

        # ── Test: switch ─────────────────────────────────────────────────────
        print("\n── TEST: switch ──")
        # Pick the second model from the fallbacks to switch to
        if cfg_text:
            fb_model = fallbacks[0].removeprefix("openrouter/") if fallbacks else None
        else:
            fb_model = None

        if fb_model:
            ec, out = run(sandbox, f"{SKILL_CMD} switch {fb_model}", label="switch")
            check("switch exits 0", ec == 0)
            check("switch shows done", "done" in out.lower() or "✅" in out)

            # Verify config updated
            cfg2 = json.loads(read_remote(sandbox, "/root/.openclaw/openclaw.json"))
            new_primary = cfg2.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
            check("switch updated primary", fb_model in new_primary, f"expected {fb_model}, got {new_primary}")
        else:
            print("  (skipped — no fallback model available)")

        # ── Test: fallbacks ──────────────────────────────────────────────────
        print("\n── TEST: fallbacks ──")
        ec, out = run(sandbox, f"{SKILL_CMD} fallbacks", label="fallbacks")
        check("fallbacks exits 0", ec == 0)
        check("fallbacks shows done", "done" in out.lower() or "✅" in out)

        # ── Test: fallbacks --secure ─────────────────────────────────────────
        print("\n── TEST: fallbacks --secure ──")
        ec, out = run(sandbox, f"{SKILL_CMD} fallbacks --secure", label="fallbacks-secure")
        check("fallbacks --secure exits 0", ec == 0)

        # ── Test: auto -f (keep primary) ─────────────────────────────────────
        print("\n── TEST: auto -f ──")
        cfg_before = json.loads(read_remote(sandbox, "/root/.openclaw/openclaw.json"))
        primary_before = cfg_before.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
        ec, out = run(sandbox, f"{SKILL_CMD} auto -f", label="auto-keep")
        check("auto -f exits 0", ec == 0)
        cfg_after = json.loads(read_remote(sandbox, "/root/.openclaw/openclaw.json"))
        primary_after = cfg_after.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
        check("auto -f preserved primary", primary_before == primary_after,
              f"before={primary_before} after={primary_after}")

        # ── Test: auto --secure ──────────────────────────────────────────────
        print("\n── TEST: auto --secure ──")
        ec, out = run(sandbox, f"{SKILL_CMD} auto --secure", label="auto-secure")
        check("auto --secure exits 0", ec == 0)

        # ── Test: auto -c 3 ──────────────────────────────────────────────────
        print("\n── TEST: auto -c 3 ──")
        ec, out = run(sandbox, f"{SKILL_CMD} auto -c 3", label="auto-c3")
        check("auto -c 3 exits 0", ec == 0)
        cfg3 = json.loads(read_remote(sandbox, "/root/.openclaw/openclaw.json"))
        fb3 = cfg3.get("agents", {}).get("defaults", {}).get("model", {}).get("fallbacks", [])
        check("auto -c 3 gives 3 fallbacks", len(fb3) == 3, f"got {len(fb3)}")

        # ── Test: E2E — openclaw actually uses the configured free model ─────
        if OPENROUTER_API_KEY:
            print("\n── TEST: E2E openclaw agent with free model ──")

            # First, run auto to pick the best model
            run(sandbox, f"{SKILL_CMD} auto", label="e2e-auto")

            # Read back which model was selected
            cfg_e2e = json.loads(read_remote(sandbox, "/root/.openclaw/openclaw.json"))
            e2e_primary = cfg_e2e.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
            e2e_fallbacks = cfg_e2e.get("agents", {}).get("defaults", {}).get("model", {}).get("fallbacks", [])
            # Strip openrouter/ prefix for the provider config model id
            raw_model_id = e2e_primary.removeprefix("openrouter/")
            print(f"  model selected: {e2e_primary} (raw: {raw_model_id})")

            # Build full openclaw config with OpenRouter provider credentials
            all_model_ids = [e2e_primary.removeprefix("openrouter/")] + [
                fb.removeprefix("openrouter/") for fb in e2e_fallbacks
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
                                    "id": mid,
                                    "name": mid,
                                    "reasoning": False,
                                    "input": ["text"],
                                    "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
                                    "contextWindow": 128000,
                                    "maxTokens": 8192,
                                }
                                for mid in all_model_ids
                            ],
                        }
                    }
                },
                "agents": {
                    "defaults": {
                        "model": cfg_e2e.get("agents", {}).get("defaults", {}).get("model", {}),
                        "timeoutSeconds": 120,
                    }
                },
            }

            config_json = json.dumps(openclaw_config, indent=2)
            sandbox.fs.upload_file(config_json.encode("utf-8"), "/root/.openclaw/openclaw.json")
            print(f"  wrote openclaw.json with OpenRouter provider + {len(all_model_ids)} models")

            # Send a simple prompt through openclaw
            prompt = "Reply with exactly: HELLO_FREE_RIDE_TEST"
            cmd = (
                f"openclaw agent --agent main "
                f"--session-id test-e2e-{int(time.time())} "
                f"--message {json.dumps(prompt)} "
                f"--json --timeout 120"
            )
            try:
                ec, out = run(sandbox, cmd, timeout=300, label="e2e-openclaw")
            except Exception as e:
                ec, out = 1, f"TIMEOUT/ERROR: {e}"
                print(f"  ⚠️  openclaw agent call failed: {e}")
            check("openclaw agent exits 0", ec == 0, f"exit_code={ec}")

            # Check we got a non-empty response
            got_response = False
            response_text = ""
            if out and out.strip():
                try:
                    data = json.loads(out)
                    got_response = True
                except json.JSONDecodeError:
                    json_start = out.find("{")
                    if json_start >= 0:
                        try:
                            data = json.loads(out[json_start:])
                            got_response = True
                        except json.JSONDecodeError:
                            pass

                if got_response:
                    # Extract text from response (openclaw JSON format)
                    if isinstance(data, dict):
                        response_text = (
                            data.get("result", {}).get("text", "")
                            or data.get("response", "")
                            or data.get("text", "")
                            or json.dumps(data)[:300]
                        )
                    print(f"  response: {response_text[:500]}")

            check("openclaw got response", got_response and len(out.strip()) > 10,
                  f"output length={len(out.strip()) if out else 0}")
            check("response mentions hello", "hello" in (response_text or out or "").lower(),
                  "expected HELLO in response")
            print(f"  E2E test used model: {e2e_primary}")
        else:
            print("\n  (skipping E2E test — no OPENROUTER_API_KEY)")

        # ── Summary ──────────────────────────────────────────────────────────
        print(f"\n{'='*70}")
        print(f"RESULTS: {len(passed)} passed, {len(failed)} failed")
        if failed:
            print("Failed checks:")
            for f in failed:
                print(f"  ❌ {f}")
        print(f"{'='*70}")
        return 1 if failed else 0

    finally:
        print("\n🧹 Deleting sandbox...")
        try:
            daytona.delete(sandbox)
            print("  sandbox deleted.")
        except Exception as e:
            print(f"  warning: cleanup failed: {e}")


if __name__ == "__main__":
    sys.exit(main())
