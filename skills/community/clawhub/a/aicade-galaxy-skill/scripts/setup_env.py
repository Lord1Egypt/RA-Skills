#!/usr/bin/env python3

from pathlib import Path
from typing import Dict


ENV_PATH = Path(".env")

DEFAULTS = {
    "AICADE_GALAXY_BASE_URL": "https://aicadegalaxy.com/agent",
    "AICADE_GALAXY_API_KEY": "xxxx",
    "AICADE_GALAXY_OUTPUT_PATH": "output",
}


def main() -> None:
    existing = load_env(ENV_PATH)

    values = {
        "AICADE_GALAXY_BASE_URL": ask_required(
            "AICADE_GALAXY_BASE_URL",
            existing.get("AICADE_GALAXY_BASE_URL")
            or existing.get("CLAWHUB_BASE_URL")
            or DEFAULTS["AICADE_GALAXY_BASE_URL"],
        ),
        "AICADE_GALAXY_API_KEY": ask_required(
            "AICADE_GALAXY_API_KEY",
            existing.get("AICADE_GALAXY_API_KEY", ""),
            secret=True,
        ),
        "AICADE_GALAXY_OUTPUT_PATH": ask_required(
            "AICADE_GALAXY_OUTPUT_PATH",
            existing.get("AICADE_GALAXY_OUTPUT_PATH")
            or DEFAULTS["AICADE_GALAXY_OUTPUT_PATH"],
        ),
    }

    ENV_PATH.write_text(serialize_env(values), encoding="utf-8")
    print(f"Saved {ENV_PATH}")
    print("Configured header: X-API-Key from AICADE_GALAXY_API_KEY")
    print("Using fixed services path: /admin/gateway/services")
    print(f"Using output directory: {values['AICADE_GALAXY_OUTPUT_PATH']}")
    print(
        f"Output file: {values['AICADE_GALAXY_OUTPUT_PATH']}/aicade-galaxy-skill.json"
    )


def load_env(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}

    result: Dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = strip_quotes(value.strip())
    return result


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def serialize_env(values: Dict[str, str]) -> str:
    return "".join(f"{key}={escape_env_value(value)}\n" for key, value in values.items())


def escape_env_value(value: str) -> str:
    if not value or any(ch.isspace() for ch in value) or '"' in value:
        return '"' + value.replace('"', '\\"') + '"'
    return value


def ask_required(key: str, current: str, secret: bool = False) -> str:
    while True:
        shown = mask_value(current) if current and secret else current
        suffix = f" [{shown}]" if shown else ""
        answer = input(f"{key}{suffix}: ").strip()
        value = answer or current
        if value:
            return value
        print(f"{key} is required.")


def mask_value(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    return "*" * (len(value) - 4) + value[-4:]


if __name__ == "__main__":
    main()
