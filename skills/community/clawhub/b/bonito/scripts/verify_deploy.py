#!/usr/bin/env python3
"""Verify prerequisites for Bonito/Atlas deployment.

Checks: Python version, bonito-cli, Docker, git, and optional Atlas clone.
Exit code 0 = all required checks pass, 1 = something missing.
"""

import os
import sys
import shutil
import subprocess


def check(name, passed, detail=""):
    """Print a check result."""
    icon = "✅" if passed else "❌"
    msg = f"{icon} {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return passed


def run_cmd(cmd):
    """Run a command and return (success, stdout)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15
        )
        return result.returncode == 0, result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, ""


def main():
    print("Bonito Deployment Prerequisites Check")
    print("=" * 42)
    print()

    all_passed = True

    # Python version
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_ok = sys.version_info >= (3, 8)
    all_passed &= check("Python 3.8+", py_ok, f"found {py_ver}")

    # git
    git_ok, git_ver = run_cmd(["git", "--version"])
    all_passed &= check("git", git_ok, git_ver if git_ok else "not found")

    # Docker
    docker_path = shutil.which("docker")
    if docker_path:
        docker_running, _ = run_cmd(["docker", "info"])
        if docker_running:
            check("Docker", True, "installed and running")
        else:
            check("Docker", False, "installed but not running — start Docker Desktop")
            all_passed = False
    else:
        check("Docker", False, "not found — install from docker.com")
        all_passed = False

    # bonito-cli
    bonito_ok, bonito_ver = run_cmd(["bonito", "--version"])
    if bonito_ok:
        check("bonito-cli", True, bonito_ver)
    else:
        check("bonito-cli", False, "not found — run: pip install bonito-cli")
        all_passed = False

    # pip (informational)
    pip_ok, pip_ver = run_cmd([sys.executable, "-m", "pip", "--version"])
    check("pip", pip_ok, pip_ver.split(",")[0] if pip_ok else "not found")

    print()

    # Optional: Atlas clone
    atlas_dir = os.path.join(os.getcwd(), "atlas")
    bonito_yaml = os.path.join(atlas_dir, "bonito.yaml")
    if os.path.isdir(atlas_dir) and os.path.isfile(bonito_yaml):
        check("Atlas repo", True, f"found at {atlas_dir}")

        # Check .env
        env_file = os.path.join(atlas_dir, ".env")
        if os.path.isfile(env_file):
            check(".env file", True, "exists")
        else:
            check(".env file", False, f"missing — run: cp {atlas_dir}/.env.example {atlas_dir}/.env")

        # Check docker-compose.mcp.yml
        mcp_compose = os.path.join(atlas_dir, "docker-compose.mcp.yml")
        if os.path.isfile(mcp_compose):
            check("docker-compose.mcp.yml", True, "found")
        else:
            check("docker-compose.mcp.yml", False, "missing from Atlas repo")

        # Check if MCP containers are running
        mcp_running, mcp_out = run_cmd(
            ["docker", "compose", "-f", mcp_compose, "ps", "--format", "json"]
        )
        if mcp_running and mcp_out:
            check("MCP servers", True, "containers found")
        else:
            check("MCP servers", False, "not running — run: docker compose -f docker-compose.mcp.yml up -d")
    else:
        print("ℹ️  Atlas repo not found in current directory (optional)")
        print("   Clone with: git clone https://github.com/ShabariRepo/atlas.git")

    print()
    if all_passed:
        print("🎉 All required prerequisites met! Ready to deploy.")
    else:
        print("⚠️  Some prerequisites are missing. Fix the items above and re-run.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
