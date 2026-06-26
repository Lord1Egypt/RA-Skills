#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
bitcoin-mcp setup helper for OpenClaw.

Checks if bitcoin-mcp is installed and prints the config snippet
to add it as an MCP server in openclaw.json.
"""

import sys
import subprocess
import shutil

MCP_CONFIG = """{
  "mcpServers": {
    "bitcoin": {
      "command": "uvx",
      "args": ["bitcoin-mcp"]
    }
  }
}"""

LINKS = """
Resources:
  GitHub:  https://github.com/Bortlesboat/bitcoin-mcp
  PyPI:    https://pypi.org/project/bitcoin-mcp/
  API:     https://bitcoinsapi.com
"""


def check_uvx() -> bool:
    return shutil.which("uvx") is not None


def check_bitcoin_mcp() -> bool:
    try:
        result = subprocess.run(
            ["uvx", "bitcoin-mcp", "--version"],
            capture_output=True, text=True, timeout=15
        )
        return result.returncode == 0
    except Exception:
        return False


def main():
    args = sys.argv[1:]

    if not args or args[0] == "status":
        uvx_ok = check_uvx()
        mcp_ok = check_bitcoin_mcp() if uvx_ok else False

        print("**bitcoin-mcp status**")
        print(f"- uvx: {'✓ found' if uvx_ok else '✗ not found (install uv)'}")
        print(f"- bitcoin-mcp: {'✓ available' if mcp_ok else '✗ not cached yet (will download on first use)'}")
        print()
        print("Add to openclaw.json mcpServers:")
        print(MCP_CONFIG)
        print(LINKS)

    elif args[0] == "config":
        print(MCP_CONFIG)

    elif args[0] == "test":
        print("Testing bitcoin-mcp connection...")
        if not check_uvx():
            print("✗ uvx not found. Install uv: https://github.com/astral-sh/uv")
            sys.exit(1)
        try:
            result = subprocess.run(
                ["uvx", "bitcoin-mcp", "--version"],
                capture_output=True, text=True, timeout=20
            )
            if result.returncode == 0:
                print(f"✓ bitcoin-mcp is working: {result.stdout.strip()}")
            else:
                print(f"✗ Error: {result.stderr.strip()}")
                sys.exit(1)
        except subprocess.TimeoutExpired:
            print("✗ Timed out — check your network connection")
            sys.exit(1)

    else:
        print(f"Unknown command: {args[0]}")
        print("Usage: bitcoin_mcp_setup.py [status|config|test]")
        sys.exit(1)


if __name__ == "__main__":
    main()
