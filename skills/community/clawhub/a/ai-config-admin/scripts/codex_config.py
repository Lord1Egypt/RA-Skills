#!/usr/bin/env python3
import argparse
from datetime import datetime
import json
import re
import shutil
import sys
import tomllib
from pathlib import Path


HOME = Path.home()
DEFAULT_CONFIG_PATH = HOME / ".codex" / "config.toml"
DEFAULT_AUTH_PATH = HOME / ".codex" / "auth.json"

SECTION_RE = re.compile(r"^\s*\[(.+)\]\s*(?:#.*)?$")
KEY_RE = re.compile(r"^(\s*)([A-Za-z0-9_.-]+)\s*=")


def load_toml(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit("json root must be an object")
    return data


def load_toml_text(text: str) -> dict:
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise SystemExit(f"invalid toml: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("toml root must be a table")
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_file(path)
    with path.open("w", encoding="utf-8") as f:
        f.write(text)


def summarize(config_data: dict | None, auth_data: dict | None) -> dict:
    providers = config_data.get("model_providers", {}) if isinstance(config_data, dict) else {}
    provider_summary = {}
    for provider_id, provider in sorted(providers.items()):
        if not isinstance(provider, dict):
            continue
        provider_summary[provider_id] = {
            "name": provider.get("name"),
            "base_url": provider.get("base_url"),
            "wire_api": provider.get("wire_api"),
            "requires_openai_auth": provider.get("requires_openai_auth"),
        }
    return {
        "configExists": config_data is not None,
        "authExists": auth_data is not None,
        "modelProvider": config_data.get("model_provider") if isinstance(config_data, dict) else None,
        "model": config_data.get("model") if isinstance(config_data, dict) else None,
        "reviewModel": config_data.get("review_model") if isinstance(config_data, dict) else None,
        "modelReasoningEffort": config_data.get("model_reasoning_effort") if isinstance(config_data, dict) else None,
        "disableResponseStorage": config_data.get("disable_response_storage") if isinstance(config_data, dict) else None,
        "networkAccess": config_data.get("network_access") if isinstance(config_data, dict) else None,
        "modelContextWindow": config_data.get("model_context_window") if isinstance(config_data, dict) else None,
        "modelAutoCompactTokenLimit": config_data.get("model_auto_compact_token_limit") if isinstance(config_data, dict) else None,
        "providers": provider_summary,
        "authMode": auth_data.get("auth_mode") if isinstance(auth_data, dict) else None,
        "hasOpenAIKey": bool(auth_data.get("OPENAI_API_KEY")) if isinstance(auth_data, dict) else False,
        "hasTokens": bool(auth_data.get("tokens")) if isinstance(auth_data, dict) else False,
    }


def format_toml_value(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    raise SystemExit(f"unsupported value type: {type(value).__name__}")


def split_lines(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if not lines:
        return []
    return lines


def current_section(line: str) -> str | None:
    match = SECTION_RE.match(line)
    if not match:
        return None
    return match.group(1).strip()


def replace_assignment(lines: list[str], section: str | None, key: str, rendered_value: str) -> list[str]:
    active_section = None
    section_start = None
    section_end = None

    for idx, line in enumerate(lines):
        header = current_section(line)
        if header is not None:
            if section is not None and header == section and section_start is None:
                section_start = idx
            elif section is not None and section_start is not None and section_end is None:
                section_end = idx
            active_section = header
        match = KEY_RE.match(line)
        if not match or match.group(2) != key:
            continue
        if section is None and active_section is None:
            lines[idx] = f"{match.group(1)}{key} = {rendered_value}\n"
            return lines
        if section is not None and active_section == section:
            lines[idx] = f"{match.group(1)}{key} = {rendered_value}\n"
            return lines

    if section is None:
        insert_at = next((idx for idx, line in enumerate(lines) if current_section(line) is not None), len(lines))
        lines.insert(insert_at, f"{key} = {rendered_value}\n")
        return lines

    if section_start is None:
        if lines and not lines[-1].endswith("\n"):
            lines[-1] = lines[-1] + "\n"
        if lines and lines[-1].strip():
            lines.append("\n")
        lines.append(f"[{section}]\n")
        lines.append(f"{key} = {rendered_value}\n")
        return lines

    if section_end is None:
        section_end = len(lines)
    lines.insert(section_end, f"{key} = {rendered_value}\n")
    return lines


def update_config_text(text: str, updates: dict[str, object], provider_updates: dict[str, object]) -> str:
    if text.strip():
        load_toml_text(text)
    lines = split_lines(text)

    top_level_order = list(updates.items())
    for key, value in reversed(top_level_order):
        if value is None:
            continue
        lines = replace_assignment(lines, None, key, format_toml_value(value))

    for key, value in provider_updates.items():
        if value is None:
            continue
        lines = replace_assignment(lines, "model_providers.OpenAI", key, format_toml_value(value))

    rendered = "".join(lines)
    if not rendered.endswith("\n"):
        rendered += "\n"
    load_toml_text(rendered)
    return rendered


def bool_arg(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--auth-file", default=str(DEFAULT_AUTH_PATH))
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("summary")
    sub.add_parser("replace-config-from-stdin")
    sub.add_parser("replace-auth-from-stdin")

    set_provider = sub.add_parser("set-openai-provider")
    set_provider.add_argument("--model-provider")
    set_provider.add_argument("--model")
    set_provider.add_argument("--review-model")
    set_provider.add_argument("--reasoning-effort")
    set_provider.add_argument("--disable-response-storage", type=bool_arg)
    set_provider.add_argument("--network-access")
    set_provider.add_argument("--windows-wsl-setup-acknowledged", type=bool_arg)
    set_provider.add_argument("--model-context-window", type=int)
    set_provider.add_argument("--model-auto-compact-token-limit", type=int)
    set_provider.add_argument("--provider-name")
    set_provider.add_argument("--base-url")
    set_provider.add_argument("--wire-api")
    set_provider.add_argument("--requires-openai-auth", type=bool_arg)

    args = parser.parse_args()

    config_path = Path(args.config_file).expanduser()
    auth_path = Path(args.auth_file).expanduser()

    if args.cmd == "replace-config-from-stdin":
        text = sys.stdin.read()
        load_toml_text(text)
        write_text(config_path, text if text.endswith("\n") else f"{text}\n")
        return 0

    if args.cmd == "replace-auth-from-stdin":
        data = load_json_text(sys.stdin.read())
        write_text(auth_path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        return 0

    config_data = load_toml(config_path) if config_path.exists() else None
    auth_data = load_json(auth_path) if auth_path.exists() else None

    if args.cmd == "summary":
        print(json.dumps(summarize(config_data, auth_data), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "set-openai-provider":
        existing_text = config_path.read_text("utf-8") if config_path.exists() else ""
        updated_text = update_config_text(
            existing_text,
            updates={
                "model_provider": args.model_provider,
                "model": args.model,
                "review_model": args.review_model,
                "model_reasoning_effort": args.reasoning_effort,
                "disable_response_storage": args.disable_response_storage,
                "network_access": args.network_access,
                "windows_wsl_setup_acknowledged": args.windows_wsl_setup_acknowledged,
                "model_context_window": args.model_context_window,
                "model_auto_compact_token_limit": args.model_auto_compact_token_limit,
            },
            provider_updates={
                "name": args.provider_name,
                "base_url": args.base_url,
                "wire_api": args.wire_api,
                "requires_openai_auth": args.requires_openai_auth,
            },
        )
        write_text(config_path, updated_text)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
