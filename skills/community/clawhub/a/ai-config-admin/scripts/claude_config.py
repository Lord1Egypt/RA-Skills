#!/usr/bin/env python3
import argparse
from datetime import datetime
import json
import shutil
import sys
from pathlib import Path


HOME = Path.home()
DEFAULT_CLAUDE_PATH = HOME / ".claude" / "settings.json"
CLAUDE_ENV_KEYS = [
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_MODEL",
    "API_TIMEOUT_MS",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC",
    "CLAUDE_CODE_ATTRIBUTION_HEADER",
]


def load_settings(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit("json root must be an object")
    return data


def load_json_text(text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("json root must be an object")
    return data


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    backup_path = path.with_name(f"{path.name}.{stamp}.bak")
    shutil.copy2(path, backup_path)
    return backup_path


def save_settings(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_file(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def ensure_env(settings: dict) -> dict:
    env = settings.setdefault("env", {})
    if not isinstance(env, dict):
        raise SystemExit("settings.env must be an object")
    return env


def summarize(settings: dict | None) -> dict:
    env = settings.get("env", {}) if isinstance(settings, dict) else {}
    if not isinstance(env, dict):
        env = {}
    return {
        "settingsExists": settings is not None,
        "hasEnv": isinstance(settings.get("env"), dict) if isinstance(settings, dict) else False,
        "envKeys": sorted(env.keys()),
        "anthropicBaseUrl": env.get("ANTHROPIC_BASE_URL"),
        "anthropicModel": env.get("ANTHROPIC_MODEL"),
        "hasAnthropicAuthToken": bool(env.get("ANTHROPIC_AUTH_TOKEN")),
        "claudeCodeDisableNonessentialTraffic": env.get("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"),
        "claudeCodeAttributionHeader": env.get("CLAUDE_CODE_ATTRIBUTION_HEADER"),
    }


def collect_env_updates(args: argparse.Namespace) -> dict[str, str]:
    updates = {}
    mapping = {
        "ANTHROPIC_AUTH_TOKEN": args.anthropic_auth_token,
        "ANTHROPIC_BASE_URL": args.anthropic_base_url,
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": args.anthropic_default_haiku_model,
        "ANTHROPIC_DEFAULT_OPUS_MODEL": args.anthropic_default_opus_model,
        "ANTHROPIC_DEFAULT_SONNET_MODEL": args.anthropic_default_sonnet_model,
        "ANTHROPIC_MODEL": args.anthropic_model,
        "API_TIMEOUT_MS": args.api_timeout_ms,
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": args.disable_nonessential_traffic,
        "CLAUDE_CODE_ATTRIBUTION_HEADER": args.attribution_header,
    }
    for key, value in mapping.items():
        if value is not None:
            updates[key] = value
    if not updates:
        raise SystemExit("pass at least one env flag")
    return updates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("summary")
    sub.add_parser("replace-from-stdin")

    for name in ("set-env", "replace-env"):
        env_parser = sub.add_parser(name)
        env_parser.add_argument("--anthropic-auth-token")
        env_parser.add_argument("--anthropic-base-url")
        env_parser.add_argument("--anthropic-default-haiku-model")
        env_parser.add_argument("--anthropic-default-opus-model")
        env_parser.add_argument("--anthropic-default-sonnet-model")
        env_parser.add_argument("--anthropic-model")
        env_parser.add_argument("--api-timeout-ms")
        env_parser.add_argument("--disable-nonessential-traffic")
        env_parser.add_argument("--attribution-header")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    path = Path(args.file).expanduser() if args.file else DEFAULT_CLAUDE_PATH

    if args.cmd == "replace-from-stdin":
        data = load_json_text(sys.stdin.read())
        save_settings(path, data)
        return 0

    settings = load_settings(path) if path.exists() else {}

    if args.cmd == "summary":
        print(json.dumps(summarize(settings), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "set-env":
        env = ensure_env(settings)
        env.update(collect_env_updates(args))
        save_settings(path, settings)
        return 0

    if args.cmd == "replace-env":
        env = ensure_env(settings)
        for key in CLAUDE_ENV_KEYS:
            env.pop(key, None)
        env.update(collect_env_updates(args))
        save_settings(path, settings)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
