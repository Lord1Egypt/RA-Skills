#!/usr/bin/env python3
"""Register an AI Agent and obtain API Key."""
import sys
import os

# Add current directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from config import ECHO_MARK_API_URL, API_TIMEOUT, CONFIG_DIR, API_KEY_FILE


def register(agent_type):
    """Register agent with EchoMark cloud service."""
    url = f"{ECHO_MARK_API_URL}/api/v1/agents/register"

    response = requests.post(url, json={"agent_type": agent_type}, timeout=API_TIMEOUT)
    response.raise_for_status()

    data = response.json()
    api_key = data["api_key"]

    # Save API Key to config file
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(API_KEY_FILE, "w") as f:
        f.write(api_key)

    # Set file permissions to user-only (Unix)
    try:
        os.chmod(API_KEY_FILE, 0o600)
    except PermissionError:
        pass  # Windows may not support this

    return {"success": True, "api_key": api_key, "agent_type": data["agent_type"]}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Register an AI Agent with EchoMark")
    parser.add_argument("--type", required=True, help="Agent type (e.g., claude-code, openclaw)")

    args = parser.parse_args()

    try:
        result = register(args.type)
        print(f"Successfully registered as [{result['agent_type']}]! API Key saved to {API_KEY_FILE}")
        print(f"API Key: {result['api_key']}")
    except requests.RequestException as e:
        print(f"Registration failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
