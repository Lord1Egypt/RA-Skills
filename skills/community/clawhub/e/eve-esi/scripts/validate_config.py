#!/usr/bin/env python3
"""EVE Dashboard Config Validator.

Validates a config file against the schema and checks:
- JSON syntax
- Schema conformity (required fields, types, allowed values)
- Scope coverage (does the character have the scopes for its alert rules?)
- Env references ($ENV:VAR) — warns if variables are not set

Usage:
    python validate_config.py <config.json>
    python validate_config.py --example    # Show example config
    python validate_config.py --schema     # Show JSON schema

Requires: Python 3.8+ (uses only stdlib)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = SCRIPT_DIR.parent / "config" / "schema.json"
EXAMPLE_PATH = SCRIPT_DIR.parent / "config" / "example-config.json"

# Which ESI scopes does each alert type require?
ALERT_SCOPE_MAP: dict[str, list[str]] = {
    "war_declared": ["esi-characters.read_notifications.v1"],
    "war_surrendered": ["esi-characters.read_notifications.v1"],
    "structure_fuel_low": ["esi-characters.read_notifications.v1"],
    "structure_under_attack": ["esi-characters.read_notifications.v1"],
    "skill_complete": ["esi-skills.read_skillqueue.v1"],
    "wallet_large_deposit": ["esi-wallet.read_character_wallet.v1"],
    "wallet_large_withdrawal": ["esi-wallet.read_character_wallet.v1"],
    "contract_expired": ["esi-contracts.read_character_contracts.v1"],
    "industry_job_complete": ["esi-industry.read_character_jobs.v1"],
    "pi_extractor_expired": ["esi-planets.manage_planets.v1"],
    "clone_jump_available": ["esi-characters.read_fatigue.v1"],
    "mail_received": ["esi-mail.read_mail.v1"],
    "killmail": ["esi-killmails.read_killmails.v1"],
}

# Which ESI scopes does each report type require?
REPORT_SCOPE_MAP: dict[str, list[str]] = {
    "net_worth": ["esi-wallet.read_character_wallet.v1", "esi-assets.read_assets.v1"],
    "skill_queue": ["esi-skills.read_skillqueue.v1"],
    "industry_jobs": ["esi-industry.read_character_jobs.v1"],
    "market_orders": ["esi-markets.read_character_orders.v1"],
    "wallet_summary": ["esi-wallet.read_character_wallet.v1"],
    "assets_summary": ["esi-assets.read_assets.v1"],
}

ENV_PATTERN = re.compile(r"^\$ENV:(.+)$")
INTERVAL_PATTERN = re.compile(r"^[0-9]+(s|m|h)$")
TREND_WINDOW_PATTERN = re.compile(r"^[0-9]+(m|h|d)$")


class ValidationResult:
    """Collects errors and warnings during validation."""

    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def print_summary(self):
        if self.warnings:
            print(f"\n⚠ {len(self.warnings)} warning(s):", file=sys.stderr)
            for w in self.warnings:
                print(f"  - {w}", file=sys.stderr)

        if self.errors:
            print(f"\n✗ {len(self.errors)} error(s):", file=sys.stderr)
            for e in self.errors:
                print(f"  - {e}", file=sys.stderr)
        else:
            print("\n✓ Config is valid.", file=sys.stderr)


def load_schema() -> dict:
    """Load the bundled JSON schema."""
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def format_path(path: str, key: str) -> str:
    """Join object paths while keeping root keys readable."""
    return f"{path}.{key}" if path else key


def validate_type(value, expected_type: str) -> bool:
    """Validate a JSON-schema primitive type."""
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    return True


def validate_against_schema(schema: dict, value, result: ValidationResult, path: str = ""):
    """Validate the config against the subset of JSON Schema used by this repo."""
    expected_type = schema.get("type")
    if expected_type and not validate_type(value, expected_type):
        current_path = path or "config"
        result.error(
            f"{current_path}: expected {expected_type}, got {type(value).__name__}"
        )
        return

    if "enum" in schema and value not in schema["enum"]:
        current_path = path or "config"
        allowed = ", ".join(repr(item) for item in schema["enum"])
        result.error(f"{current_path}: invalid value {value!r} (allowed: {allowed})")

    if isinstance(value, str) and "pattern" in schema:
        if not re.match(schema["pattern"], value):
            current_path = path or "config"
            result.error(
                f"{current_path}: value {value!r} does not match pattern {schema['pattern']!r}"
            )

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        for field in required_fields:
            if field not in value:
                result.error(f"{format_path(path, field)}: required field is missing")

        if schema.get("additionalProperties", True) is False:
            for key in value:
                if key not in properties:
                    result.error(
                        f"{format_path(path, key)}: additional property is not allowed"
                    )

        for key, subschema in properties.items():
            if key in value:
                validate_against_schema(subschema, value[key], result, format_path(path, key))

    elif isinstance(value, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            current_path = path or "config"
            result.error(
                f"{current_path}: expected at least {min_items} item(s), got {len(value)}"
            )

        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate_against_schema(item_schema, item, result, f"{path}[{index}]")


def resolve_env_value(value: str) -> tuple[str | None, bool]:
    """Resolve $ENV:VAR references. Returns (resolved_value, is_env_ref)."""
    if not isinstance(value, str):
        return value, False

    match = ENV_PATTERN.match(value)
    if not match:
        return value, False

    var_name = match.group(1)
    env_val = os.environ.get(var_name)
    return env_val, True


def check_env_refs(config: dict, result: ValidationResult, path: str = ""):
    """Recursively scan config for $ENV: references and check if they are set."""
    if isinstance(config, dict):
        for key, value in config.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, str):
                resolved, is_env = resolve_env_value(value)
                if is_env and resolved is None:
                    var_name = ENV_PATTERN.match(value).group(1)
                    result.warn(f"{current_path}: env variable '{var_name}' is not set")
            elif isinstance(value, (dict, list)):
                check_env_refs(value, result, current_path)
    elif isinstance(config, list):
        for i, item in enumerate(config):
            check_env_refs(item, result, f"{path}[{i}]")


def validate_required_fields(config: dict, result: ValidationResult):
    """Check that all required fields are present."""
    # Top-level
    if "schema_version" not in config:
        result.error("Required field 'schema_version' is missing")
    elif config["schema_version"] != "1.0":
        result.error(f"Unknown schema_version: '{config['schema_version']}' (expected: '1.0')")

    if "notification_channels" not in config:
        result.error("Required field 'notification_channels' is missing")
    else:
        channels = config["notification_channels"]
        if not isinstance(channels, dict) or len(channels) == 0:
            result.error("'notification_channels' must define at least one channel")

    if "characters" not in config:
        result.error("Required field 'characters' is missing")
    elif not isinstance(config["characters"], list) or len(config["characters"]) == 0:
        result.error("'characters' must contain at least one character")
    else:
        for i, char in enumerate(config["characters"]):
            prefix = f"characters[{i}]"
            if "scopes" in char and (not isinstance(char["scopes"], list) or len(char["scopes"]) == 0):
                result.warn(f"{prefix}: 'scopes' is empty — no authenticated endpoint will work")


def validate_intervals(config: dict, result: ValidationResult):
    """Check that interval strings have the correct format."""
    # alerts.check_interval
    alerts = config.get("alerts", {})
    if "check_interval" in alerts:
        if not INTERVAL_PATTERN.match(alerts["check_interval"]):
            result.error(f"alerts.check_interval: invalid format '{alerts['check_interval']}' (expected e.g. '5m', '1h')")

    # alerts.rules[].cooldown
    for i, rule in enumerate(alerts.get("rules", [])):
        if "cooldown" in rule and not INTERVAL_PATTERN.match(rule["cooldown"]):
            result.error(f"alerts.rules[{i}].cooldown: invalid format '{rule['cooldown']}'")

    # market.check_interval
    market = config.get("market", {})
    if "check_interval" in market:
        if not INTERVAL_PATTERN.match(market["check_interval"]):
            result.error(f"market.check_interval: invalid format '{market['check_interval']}'")

    # market.items[].cooldown, trend_alert.time_window
    for i, item in enumerate(market.get("items", [])):
        if "cooldown" in item and not INTERVAL_PATTERN.match(item["cooldown"]):
            result.error(f"market.items[{i}].cooldown: invalid format '{item['cooldown']}'")
        trend = item.get("trend_alert", {})
        if "time_window" in trend and not TREND_WINDOW_PATTERN.match(trend["time_window"]):
            result.error(f"market.items[{i}].trend_alert.time_window: invalid format '{trend['time_window']}'")


def validate_alert_types(config: dict, result: ValidationResult):
    """Check that alert types are valid."""
    valid_types = set(ALERT_SCOPE_MAP.keys())
    for i, rule in enumerate(config.get("alerts", {}).get("rules", [])):
        alert_type = rule.get("type")
        if alert_type and alert_type not in valid_types:
            result.error(f"alerts.rules[{i}].type: unknown alert type '{alert_type}'")

        severity = rule.get("severity")
        if severity and severity not in ("info", "warning", "critical"):
            result.error(f"alerts.rules[{i}].severity: invalid '{severity}' (allowed: info, warning, critical)")


def validate_report_templates(config: dict, result: ValidationResult):
    """Check that report templates are valid."""
    valid_templates = set(REPORT_SCOPE_MAP.keys())
    for i, tpl in enumerate(config.get("reports", {}).get("templates", [])):
        name = tpl.get("name")
        if name and name not in valid_templates:
            result.error(f"reports.templates[{i}].name: unknown template '{name}'")

        fmt = tpl.get("format")
        if fmt and fmt not in ("short", "detailed"):
            result.error(f"reports.templates[{i}].format: invalid '{fmt}' (allowed: short, detailed)")


def validate_scope_coverage(config: dict, result: ValidationResult):
    """Check that characters have the scopes required by their alerts and reports."""
    characters = config.get("characters", [])
    if not characters:
        return

    # Check each character
    for char in characters:
        if not char.get("enabled", True):
            continue

        char_scopes = set(char.get("scopes", []))
        char_name = char.get("name", f"ID {char.get('id', '?')}")
        char_id = char.get("id")
        needed_scopes: dict[str, list[str]] = {}

        for rule in config.get("alerts", {}).get("rules", []):
            filter_ids = set(rule.get("character_filter", []))
            if filter_ids and char_id not in filter_ids:
                continue
            alert_type = rule.get("type", "")
            for scope in ALERT_SCOPE_MAP.get(alert_type, []):
                needed_scopes.setdefault(scope, []).append(f"alert:{alert_type}")

        for tpl in config.get("reports", {}).get("templates", []):
            filter_ids = set(tpl.get("character_filter", []))
            if filter_ids and char_id not in filter_ids:
                continue
            tpl_name = tpl.get("name", "")
            for scope in REPORT_SCOPE_MAP.get(tpl_name, []):
                needed_scopes.setdefault(scope, []).append(f"report:{tpl_name}")

        for scope, reasons in needed_scopes.items():
            if scope not in char_scopes:
                reasons_str = ", ".join(sorted(set(reasons)))
                result.warn(
                    f"Character '{char_name}': scope '{scope}' is missing "
                    f"(required for: {reasons_str})"
                )


def validate_channel_refs(config: dict, result: ValidationResult):
    """Check that referenced channels are defined in notification_channels."""
    defined = set(config.get("notification_channels", {}).keys())

    # alerts.channels
    for ch in config.get("alerts", {}).get("channels", []):
        if ch not in defined:
            result.error(f"alerts.channels: channel '{ch}' not defined in notification_channels")

    # reports.channels
    for ch in config.get("reports", {}).get("channels", []):
        if ch not in defined:
            result.error(f"reports.channels: channel '{ch}' not defined in notification_channels")

    # market.channels
    for ch in config.get("market", {}).get("channels", []):
        if ch not in defined:
            result.error(f"market.channels: channel '{ch}' not defined in notification_channels")


def validate_config(config: dict) -> ValidationResult:
    """Run all validations and return the result."""
    result = ValidationResult()

    validate_against_schema(load_schema(), config, result)
    validate_required_fields(config, result)
    validate_intervals(config, result)
    validate_alert_types(config, result)
    validate_report_templates(config, result)
    validate_scope_coverage(config, result)
    validate_channel_refs(config, result)
    check_env_refs(config, result)

    return result


def main():
    parser = argparse.ArgumentParser(description="EVE Dashboard Config Validator")
    parser.add_argument("config_file", nargs="?", help="Path to config JSON file")
    parser.add_argument("--example", action="store_true", help="Show example config")
    parser.add_argument("--schema", action="store_true", help="Show JSON schema")
    args = parser.parse_args()

    if args.example:
        if not EXAMPLE_PATH.exists():
            print(f"Example config not found: {EXAMPLE_PATH}", file=sys.stderr)
            sys.exit(1)
        print(EXAMPLE_PATH.read_text(encoding="utf-8"))
        return

    if args.schema:
        if not SCHEMA_PATH.exists():
            print(f"Schema not found: {SCHEMA_PATH}", file=sys.stderr)
            sys.exit(1)
        print(SCHEMA_PATH.read_text(encoding="utf-8"))
        return

    if not args.config_file:
        parser.print_help()
        sys.exit(1)

    config_path = Path(args.config_file)
    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    # Load JSON
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"JSON syntax error in {config_path}:", file=sys.stderr)
        print(f"  Line {e.lineno}, column {e.colno}: {e.msg}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(config, dict):
        print("Config must be a JSON object (not array/string/etc.)", file=sys.stderr)
        sys.exit(1)

    # Validate
    print(f"Validating: {config_path}", file=sys.stderr)
    result = validate_config(config)
    result.print_summary()

    sys.exit(0 if result.ok else 1)


if __name__ == "__main__":
    main()
