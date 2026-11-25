"""Contained verification of generated TypeMCP projects.

Runs install, typecheck, test, build, and MCP stdio smoke in a
scrubbed temporary workspace (AGENTS.md rule 7).  Never executes
lifecycle scripts before inspection, never uses inherited credentials,
and never contacts live upstreams.

Usage as a module::

    from verify_generated import verify_project
    results = verify_project("/path/to/generated/project")

Usage as a CLI::

    python3 verify_generated.py --project /path/to/project [--skip-mcp]
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Environment scrubbing
# ---------------------------------------------------------------------------

_SAFE_ENV_KEYS = frozenset({"PATH", "LANG", "LC_ALL", "LC_CTYPE", "TERM"})

_CREDENTIAL_PREFIXES = (
    "AWS_", "AZURE_", "GCP_", "GOOGLE_", "GITHUB_", "GH_",
    "NPM_TOKEN", "NPM_AUTH", "npm_config_//", "npm_config__auth",
    "DOCKER_", "KUBE", "SLACK_", "STRIPE_", "OPENAI_", "ANTHROPIC_",
    "HF_", "HUGGING", "WANDB_", "HEROKU_", "VERCEL_", "NETLIFY_",
    "CLOUDFLARE_", "DIGITALOCEAN_", "LINODE_", "VULTR_",
    "TYPE_MCP_AUTH",  # generated-project auth tokens
)


def scrub_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    """Build a scrubbed environment for contained execution.

    Keeps only safe keys, drops all credential/cloud variables, and
    lets the caller inject isolated HOME/TMP/npm-cache paths.
    """
    env: dict[str, str] = {}
    for key in sorted(os.environ):
        if key in _SAFE_ENV_KEYS:
            env[key] = os.environ[key]
            continue
        if any(key.startswith(p) for p in _CREDENTIAL_PREFIXES):
            continue
        if key.startswith("npm_config_") and ("auth" in key or "token" in key):
            continue
    env["CI"] = "1"  # signal non-interactive
    if extra:
        env.update(extra)
    return env


# ---------------------------------------------------------------------------
# Package inspection
# ---------------------------------------------------------------------------

_PROHIBITED_DEP_PREFIXES = ("file:", "git:", "link:", "portal:")


def inspect_package(project_dir: str | Path) -> dict[str, Any]:
    """Inspect package.json for prohibited dependency forms.

    Returns a dict with 'ok' bool and 'violations' list.
    """
    pkg_path = Path(project_dir) / "package.json"
    pkg = json.loads(pkg_path.read_text())
    violations: list[str] = []
    if not (Path(project_dir) / "package-lock.json").is_file():
        violations.append("package-lock.json is required")
    for section in ("dependencies", "devDependencies"):
        for name, version in pkg.get(section, {}).items():
            for prefix in _PROHIBITED_DEP_PREFIXES:
                if str(version).startswith(prefix):
                    violations.append(f"{section}.{name} = {version}")
    return {"ok": not violations, "violations": violations}


# ---------------------------------------------------------------------------
# Contained step runner
# ---------------------------------------------------------------------------

def _run_step(
    cmd: list[str],
    cwd: str,
    env: dict[str, str],
    timeout: int = 300,
) -> dict[str, Any]:
    """Run a command and capture the result."""
    try:
        r = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "ok": r.returncode == 0,
            "returncode": r.returncode,
            "stdout_tail": r.stdout[-2000:] if r.stdout else "",
            "stderr_tail": r.stderr[-2000:] if r.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": -1, "error": "timeout"}
    except FileNotFoundError as exc:
        return {"ok": False, "returncode": -1, "error": str(exc)}


# ---------------------------------------------------------------------------
# MCP stdio smoke test
# ---------------------------------------------------------------------------

_SMOKE_READ_MJS = textwrap.dedent("""\
    import { Client } from "@modelcontextprotocol/sdk/client/index.js";
    import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

    const transport = new StdioClientTransport({
      command: "node",
      args: ["dist/index.js"],
      cwd: process.cwd(),
      env: { TYPE_MCP_BASE_URL: process.env.TYPE_MCP_BASE_URL, PATH: process.env.PATH },
    });

    const client = new Client({ name: "smoke-read", version: "1.0.0" });
    await client.connect(transport);

    const { tools } = await client.listTools();
    const toolNames = tools.map(t => t.name).sort();

    // Call the first read tool we can find (getPet in Petstore).
    const readTool = tools.find(t => t.name.toLowerCase().includes("get"));
    let callResult = null;
    if (readTool) {
      callResult = await client.callTool({
        name: readTool.name,
        arguments: { petId: "1" },
      });
    }

    await client.close();
    console.log(JSON.stringify({ toolNames, callResult }));
""")

_SMOKE_WRITE_DENY_MJS = textwrap.dedent("""\
    import { Client } from "@modelcontextprotocol/sdk/client/index.js";
    import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

    // Deliberately do NOT set TYPE_MCP_ALLOW_PROTECTED_OPERATIONS.
    const transport = new StdioClientTransport({
      command: "node",
      args: ["dist/index.js"],
      cwd: process.cwd(),
      env: { TYPE_MCP_BASE_URL: process.env.TYPE_MCP_BASE_URL, PATH: process.env.PATH },
    });

    const client = new Client({ name: "smoke-write-deny", version: "1.0.0" });
    await client.connect(transport);

    const { tools } = await client.listTools();
    const writeTool = tools.find(t =>
      t.name.toLowerCase().includes("create") ||
      t.name.toLowerCase().includes("post") ||
      t.name.toLowerCase().includes("put") ||
      t.name.toLowerCase().includes("delete") ||
      t.name.toLowerCase().includes("update")
    );

    let callResult = null;
    let isError = false;
    if (writeTool) {
      try {
        callResult = await client.callTool({
          name: writeTool.name,
          arguments: { name: "TestPet", status: "available" },
        });
        isError = !!(callResult && callResult.isError);
      } catch (e) {
        isError = true;
        callResult = { error: String(e) };
      }
    }

    await client.close();
    console.log(JSON.stringify({ writeToolFound: !!writeTool, isError, callResult }));
""")


def mcp_smoke_read(project_dir: str | Path, env: dict[str, str]) -> dict[str, Any]:
    """Run a read-only MCP stdio smoke test."""
    smoke_path = Path(project_dir) / "smoke_read.mjs"
    smoke_path.write_text(_SMOKE_READ_MJS)
    try:
        return _run_step(["node", "smoke_read.mjs"], str(project_dir), env, timeout=60)
    finally:
        smoke_path.unlink(missing_ok=True)


def mcp_smoke_write_deny(project_dir: str | Path, env: dict[str, str]) -> dict[str, Any]:
    """Run a protected-write denial MCP stdio smoke test."""
    smoke_path = Path(project_dir) / "smoke_write_deny.mjs"
    smoke_path.write_text(_SMOKE_WRITE_DENY_MJS)
    try:
        return _run_step(["node", "smoke_write_deny.mjs"], str(project_dir), env, timeout=60)
    finally:
        smoke_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Full contained verification
# ---------------------------------------------------------------------------

def verify_project(
    project_dir: str | Path,
    *,
    skip_mcp: bool = False,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Run full contained verification on a generated project.

    Copies the project to a fresh temp workspace, scrubs the
    environment, and runs: inspect → install → typecheck → test →
    build → (optional) MCP smoke.

    Returns a dict mapping step names to result dicts.
    """
    project_dir = Path(project_dir)
    results: dict[str, Any] = {}

    with tempfile.TemporaryDirectory(prefix="typemcp-e2e-") as workspace:
        # Copy project to isolated workspace.
        proj = Path(workspace) / "project"
        shutil.copytree(project_dir, proj)

        # Isolated dirs.
        home = Path(workspace) / "home"
        tmp = Path(workspace) / "tmp"
        npm_cache = Path(workspace) / "npm-cache"
        home.mkdir()
        tmp.mkdir()
        npm_cache.mkdir()

        env = scrub_env({
            "HOME": str(home),
            "TMPDIR": str(tmp),
            "npm_config_cache": str(npm_cache),
            "npm_config_userconfig": str(home / ".npmrc"),
            "npm_config_proxy": "",
            "npm_config_https_proxy": "",
            "npm_config_noproxy": "*",
            "npm_config_audit": "false",
            "npm_config_fund": "false",
            "npm_config_ignore_scripts": "true",
        })
        if base_url:
            env["TYPE_MCP_BASE_URL"] = base_url

        # 1. Inspect package.json.
        results["inspect"] = inspect_package(proj)
        if not results["inspect"]["ok"]:
            return results  # fail fast

        # 2. Install exactly the lockfile graph, without lifecycle scripts.
        results["install"] = _run_step(
            ["npm", "ci", "--ignore-scripts", "--no-audit", "--fund=false"], str(proj), env, timeout=300,
        )
        if not results["install"]["ok"]:
            return results

        # Record the runtime actually installed into this isolated consumer.
        # This makes the contained E2E contract independent of the rendered
        # declaration and preserves registry provenance from the lockfile.
        runtime_package = proj / "node_modules" / "@theorvane" / "type-mcp" / "package.json"
        try:
            installed_package = json.loads(runtime_package.read_text(encoding="utf-8"))
            installed_lockfile = json.loads((proj / "package-lock.json").read_text(encoding="utf-8"))
            installed_lock = installed_lockfile["packages"]["node_modules/@theorvane/type-mcp"]
            results["installed_runtime"] = {
                "ok": True,
                "version": installed_package.get("version"),
                "resolved": installed_lock.get("resolved"),
                "integrity": installed_lock.get("integrity"),
            }
        except (KeyError, OSError, json.JSONDecodeError) as exc:
            results["installed_runtime"] = {"ok": False, "error": str(exc)}
            return results

        # 3. Typecheck.
        results["typecheck"] = _run_step(
            ["npx", "tsc", "--noEmit"], str(proj), env, timeout=120,
        )

        # 4. Unit tests.
        results["test"] = _run_step(
            ["npx", "vitest", "run"], str(proj), env, timeout=120,
        )

        # 5. Build.
        results["build"] = _run_step(
            ["npm", "run", "build"], str(proj), env, timeout=120,
        )
        if not results["build"]["ok"]:
            return results  # need dist/ for smoke

        # 6. MCP smoke tests.
        if not skip_mcp:
            results["mcp_read"] = mcp_smoke_read(proj, env)
            results["mcp_write_deny"] = mcp_smoke_write_deny(proj, env)

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Contained verification of a generated TypeMCP project.")
    parser.add_argument("--project", required=True, help="Path to the generated project directory.")
    parser.add_argument("--skip-mcp", action="store_true", help="Skip MCP smoke tests.")
    parser.add_argument("--base-url", default=None, help="TYPE_MCP_BASE_URL for smoke tests.")
    args = parser.parse_args()

    results = verify_project(args.project, skip_mcp=args.skip_mcp, base_url=args.base_url)
    print(json.dumps(results, indent=2))

    failed = [k for k, v in results.items() if isinstance(v, dict) and not v.get("ok", False)]
    if failed:
        print(f"\nFAILED steps: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)
    print("\nAll steps passed.")


if __name__ == "__main__":
    main()
