#!/usr/bin/env python3
"""Conservative helper for the BlueGreenPilot skill.

This script creates templates and reports missing deployment facts. It does not
switch traffic, run deploy commands, or modify infrastructure.
"""

from __future__ import annotations

import argparse
import datetime as _dt
from pathlib import Path
import re
import sys


ROOT = Path(".bluegreenpilot")
VALID_SLOTS = {"blue", "green"}


CONFIG_TEMPLATE = """version: 1
app: CHANGE_ME
strategy: blue-green

branches:
  dev: dev
  homolog: homolog
  prod: main

environments:
  dev:
    deploy_mode: local
    strategy: single-slot
  homolog:
    deploy_mode: docker
    strategy: blue-green
    data_mode: snapshot
  prod:
    deploy_mode: docker
    strategy: blue-green

slots:
  homolog:
    blue_url: https://blue.homolog.example.com
    green_url: https://green.homolog.example.com
    public_url: https://homolog.example.com
  prod:
    blue_url: https://blue.example.com
    green_url: https://green.example.com
    public_url: https://example.com

database:
  homolog_data_mode: snapshot # snapshot | mock | empty | manual
  prod_snapshot_required: true
  migration_policy: require_snapshot # require_snapshot | manual | allow_safe_only

state:
  backend: repo # repo | server-file | ci-artifact | object-storage | manual
  path: .bluegreenpilot/state.{environment}.yaml

checks:
  healthcheck_path: /health
  smoke_commands:
    - npm run build
    - npm test

switch:
  method: manual # manual | script | nginx | cloudflare | load-balancer | ci
  command: ""

rollback:
  method: manual # manual | script | ci
  command: ""
"""


STATE_TEMPLATE = """version: 1
environment: {env}
active_slot: UNKNOWN
inactive_slot: UNKNOWN
last_successful_release: ""
last_switch_at: ""
last_snapshot: ""
"""


def _opposite_slot(slot: str) -> str:
    return "green" if slot == "blue" else "blue"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _clean_scalar(value: str) -> str:
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if "#" in value:
        value = value.split("#", 1)[0].strip()
    return value


def _extract_scalar(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        return ""
    return _clean_scalar(match.group(1))


def _extract_section_scalar(text: str, section: str, key: str) -> str:
    lines = text.splitlines()
    in_section = False
    section_indent = 0

    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if stripped == f"{section}:":
            in_section = True
            section_indent = indent
            continue

        if in_section and indent <= section_indent and not stripped.startswith("-"):
            in_section = False

        if in_section:
            match = re.match(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", line)
            if match:
                return _clean_scalar(match.group(1))

    return ""


def cmd_init(_: argparse.Namespace) -> int:
    ROOT.mkdir(exist_ok=True)
    (ROOT / "history").mkdir(exist_ok=True)

    config = ROOT / "config.yaml"
    if not config.exists():
        config.write_text(CONFIG_TEMPLATE, encoding="utf-8")
        print(f"created {config}")
    else:
        print(f"exists  {config}")

    for env in ("dev", "homolog", "prod"):
        state = ROOT / f"state.{env}.yaml"
        if not state.exists():
            state.write_text(STATE_TEMPLATE.format(env=env), encoding="utf-8")
            print(f"created {state}")
        else:
            print(f"exists  {state}")

    print("next: edit .bluegreenpilot/config.yaml and replace UNKNOWN state values")
    return 0


def cmd_adopt_prod(args: argparse.Namespace) -> int:
    if args.active_slot not in VALID_SLOTS:
        print("FAIL --active-slot must be blue or green")
        return 2

    inactive = _opposite_slot(args.active_slot)
    blue_url = args.public_url if args.active_slot == "blue" else "TO_BE_PROVISIONED"
    green_url = args.public_url if args.active_slot == "green" else "TO_BE_PROVISIONED"

    ROOT.mkdir(exist_ok=True)
    (ROOT / "history").mkdir(exist_ok=True)

    config = ROOT / "config.yaml"
    state = ROOT / "state.prod.yaml"
    if (config.exists() or state.exists()) and not args.force:
        print("FAIL .bluegreenpilot config/state already exists; pass --force to overwrite")
        return 2

    config.write_text(f"""version: 1
app: {args.app}
strategy: blue-green

branches:
  prod: {args.source}

environments:
  prod:
    deploy_mode: {args.deploy_mode}
    strategy: blue-green

slots:
  prod:
    blue_url: {blue_url}
    green_url: {green_url}
    public_url: {args.public_url}

database:
  homolog_data_mode: manual
  prod_snapshot_required: true
  migration_policy: require_snapshot

state:
  backend: manual
  path: .bluegreenpilot/state.{{environment}}.yaml

adoption:
  mode: brownfield
  current_prod_slot: {args.active_slot}
  inactive_slot_status: not-provisioned

checks:
  healthcheck_path: {args.healthcheck_path}
  smoke_commands: []

switch:
  method: manual
  command: ""

rollback:
  method: manual
  command: ""
""", encoding="utf-8")

    state.write_text(f"""version: 1
environment: prod
active_slot: {args.active_slot}
inactive_slot: {inactive}
last_successful_release: {args.source}
last_switch_at: ""
last_snapshot: ""
adoption_status: brownfield
inactive_slot_status: not-provisioned
""", encoding="utf-8")

    print(f"created {config}")
    print(f"created {state}")
    print(f"production mapped as stable {args.active_slot}; {inactive} must be provisioned before switch")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    config = _read(ROOT / "config.yaml")
    if not config:
        print("missing .bluegreenpilot/config.yaml; run init first", file=sys.stderr)
        return 2

    state_path = ROOT / f"state.{args.env}.yaml"
    state = _read(state_path)
    if not state:
        print(f"missing {state_path}; create or retrieve environment state", file=sys.stderr)
        return 2

    active = _extract_scalar(state, "active_slot") or "UNKNOWN"
    inactive = _extract_scalar(state, "inactive_slot") or "UNKNOWN"
    inactive_status = _extract_scalar(state, "inactive_slot_status") or ""
    release = _extract_scalar(state, "last_successful_release") or ""
    switch = _extract_section_scalar(config, "switch", "method") or "UNKNOWN"

    print(f"environment: {args.env}")
    print(f"active_slot: {active}")
    print(f"inactive_slot: {inactive}")
    if inactive_status:
        print(f"inactive_slot_status: {inactive_status}")
    print(f"last_successful_release: {release or '(none recorded)'}")
    print(f"switch_method: {switch}")

    if active == "UNKNOWN" or inactive == "UNKNOWN":
        print("blocker: slot state is unknown; do not deploy or switch yet")
        return 1

    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    config = _read(ROOT / "config.yaml")
    if not config:
        print("missing .bluegreenpilot/config.yaml; run init first", file=sys.stderr)
        return 2

    state = _read(ROOT / f"state.{args.env}.yaml")
    active = _extract_scalar(state, "active_slot") or "UNKNOWN"
    inactive = _extract_scalar(state, "inactive_slot") or "UNKNOWN"
    inactive_status = _extract_scalar(state, "inactive_slot_status") or ""
    health = _extract_scalar(config, "healthcheck_path") or "/health"
    switch = _extract_section_scalar(config, "switch", "method") or "manual"
    rollback = _extract_section_scalar(config, "rollback", "method") or "manual"
    stamp = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    print(f"BlueGreenPilot deploy plan ({stamp})")
    print(f"Target: {args.env}")
    print(f"Current active slot: {active}")
    print(f"Deploy target: {inactive}")
    if inactive_status:
        print(f"Inactive slot status: {inactive_status}")
    print(f"Healthcheck: {health}")
    print(f"Switch method: {switch}")
    print(f"Rollback: {rollback}")
    print("")
    print("Steps:")
    print("1. Confirm source branch/tag/commit.")
    print("2. Confirm database snapshot/migration policy.")
    print("3. Deploy only to the inactive slot.")
    print("4. Run healthcheck and smoke commands.")
    if args.env == "prod":
        print("5. Request final confirmation before production switch.")
    else:
        print("5. Ask before switching target environment traffic.")
    print("6. Switch traffic and record state/history.")

    if active == "UNKNOWN" or inactive == "UNKNOWN":
        print("")
        print("BLOCKER: active/inactive slot is unknown.")
        return 1

    if args.env == "prod" and inactive_status == "not-provisioned":
        print("")
        print("BLOCKER: adoption inactive slot is not provisioned.")
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bluegreenpilot")
    sub = parser.add_subparsers(required=True)

    init = sub.add_parser("init")
    init.set_defaults(func=cmd_init)

    adopt = sub.add_parser("adopt-prod")
    adopt.add_argument("--app", required=True)
    adopt.add_argument("--public-url", required=True)
    adopt.add_argument("--deploy-mode", default="manual")
    adopt.add_argument("--active-slot", default="blue")
    adopt.add_argument("--source", default="CURRENT_PRODUCTION")
    adopt.add_argument("--healthcheck-path", default="/health")
    adopt.add_argument("--force", action="store_true")
    adopt.set_defaults(func=cmd_adopt_prod)

    status = sub.add_parser("status")
    status.add_argument("--env", default="prod")
    status.set_defaults(func=cmd_status)

    plan = sub.add_parser("plan")
    plan.add_argument("--env", default="prod")
    plan.set_defaults(func=cmd_plan)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
