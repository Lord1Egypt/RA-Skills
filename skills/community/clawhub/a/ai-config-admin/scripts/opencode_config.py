#!/usr/bin/env python3
import argparse
from datetime import datetime
import json
import shutil
import sys
from pathlib import Path


HOME = Path.home()
DEFAULT_OPENCODE_PATH = HOME / ".config" / "opencode" / "opencode.json"


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def backup_config(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    backup_path = path.with_name(f"{path.name}.{stamp}.bak")
    shutil.copy2(path, backup_path)
    return backup_path


def save_config(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_config(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def load_json_text(text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("json root must be an object")
    return data


def summarize(data: dict) -> dict:
    providers = data.get("provider", {})
    agent = data.get("agent", {})
    provider_models = {}
    for provider_id, provider in sorted(providers.items()):
        if not isinstance(provider, dict):
            continue
        models = provider.get("models", {})
        if isinstance(models, dict):
            provider_models[provider_id] = sorted(models.keys())
    return {
        "providers": sorted(provider_models.keys()),
        "providerModels": provider_models,
        "agentKeys": sorted(
            key for key, value in agent.items() if isinstance(value, dict)
        ),
        "schema": data.get("$schema"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("summary")
    sub.add_parser("replace-from-stdin")

    args = parser.parse_args()
    path = Path(args.file).expanduser() if args.file else DEFAULT_OPENCODE_PATH

    if args.cmd == "replace-from-stdin":
        data = load_json_text(sys.stdin.read())
        save_config(path, data)
        return 0

    data = load_config(path)

    if args.cmd == "summary":
        print(json.dumps(summarize(data), ensure_ascii=False, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
