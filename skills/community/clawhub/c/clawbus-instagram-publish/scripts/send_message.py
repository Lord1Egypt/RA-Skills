#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path

import requests


BASE_URL = "https://api.mybrandmetrics.com/instagram/messaging"


def resolve_config_path(explicit_path: str | None) -> Path:
    if explicit_path:
        return Path(explicit_path).expanduser()

    env_path = os.environ.get("INSTAGRAM_PUBLISH_CONFIG")
    if env_path:
        return Path(env_path).expanduser()

    script_dir = Path(__file__).resolve().parent
    workspace_root = script_dir.parent.parent.parent
    return workspace_root / "config.json"


def load_config(config_path: Path) -> dict:
    try:
        return json.loads(config_path.read_text())
    except FileNotFoundError:
        print(f"Error: config file not found at {config_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: could not decode JSON from {config_path}: {exc}", file=sys.stderr)
        sys.exit(1)


def resolve_credentials(args: argparse.Namespace, config: dict) -> tuple[str, str]:
    instagram_config = config.get("instagram", {})
    api_key = (
        args.api_key
        or os.environ.get("INSTAGRAM_API_KEY")
        or os.environ.get("INSTAGRAM_AUTHORIZATION_TOKEN")
        or instagram_config.get("api_key")
        or instagram_config.get("authorization_token")
    )
    connection_id = (
        args.connection_id
        or os.environ.get("INSTAGRAM_CONNECTION_ID")
        or instagram_config.get("connection_id")
    )

    if not all([api_key, connection_id]):
        print(
            "Error: missing Instagram credentials. Provide API key and connection_id "
            "via arguments, environment variables, or config.json.",
            file=sys.stderr,
        )
        sys.exit(1)

    return api_key, connection_id


def send_message(api_key: str, connection_id: str, conversation_id: str, message: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/messages/send",
        headers={"X-API_KEY": api_key, "Content-Type": "application/json"},
        json={
            "connection_id": connection_id,
            "conversation_id": conversation_id,
            "message": message,
        },
        timeout=60,
    )
    if response.status_code == 200:
        return response.json()

    print(f"Error sending message: HTTP {response.status_code}", file=sys.stderr)
    print(response.text, file=sys.stderr)
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send an Instagram direct message via MyBrandMetrics API")
    parser.add_argument("--api-key", help="MyBrandMetrics API key")
    parser.add_argument("--connection-id", help="Instagram connection ID")
    parser.add_argument("--config", help="Path to config.json")
    parser.add_argument("--conversation-id", required=True, help="Conversation ID returned by receive_messages.py")
    parser.add_argument("--message", required=True, help="Message text to send")
    args = parser.parse_args()

    config = load_config(resolve_config_path(args.config))
    api_key, connection_id = resolve_credentials(args, config)
    result = send_message(api_key, connection_id, args.conversation_id, args.message)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
