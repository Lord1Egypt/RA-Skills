#!/usr/bin/env python3
"""Validate a Chitin Trust Channels configuration file."""

import sys
import yaml
from pathlib import Path

VALID_LEVELS = {"sovereign", "trusted", "guarded", "observer", "silent"}
REQUIRED_FIELDS = ["version", "owner", "channels", "defaults"]


def validate(config_path: str) -> list[str]:
    errors = []
    path = Path(config_path)

    if not path.exists():
        return [f"Config file not found: {config_path}"]

    try:
        with open(path) as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"Invalid YAML: {e}"]

    if not isinstance(config, dict):
        return ["Config must be a YAML mapping"]

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in config:
            errors.append(f"Missing required field: '{field}'")

    # Validate version
    version = config.get("version")
    if version and str(version) not in ("0.1",):
        errors.append(f"Unsupported version: {version} (supported: 0.1)")

    # Validate owner
    owner = config.get("owner", {})
    if not isinstance(owner, dict) or len(owner) == 0:
        errors.append("'owner' must contain at least one identity (e.g., telegram, discord)")

    # Validate channels
    channels = config.get("channels", [])
    if not isinstance(channels, list):
        errors.append("'channels' must be a list")
    else:
        for i, ch in enumerate(channels):
            if not isinstance(ch, dict):
                errors.append(f"channels[{i}]: must be a mapping")
                continue
            if "id" not in ch:
                errors.append(f"channels[{i}]: missing 'id'")
            if "level" not in ch:
                errors.append(f"channels[{i}]: missing 'level'")
            elif ch["level"] not in VALID_LEVELS:
                errors.append(f"channels[{i}]: invalid level '{ch['level']}' (valid: {VALID_LEVELS})")

            # Validate overrides
            for j, ov in enumerate(ch.get("overrides", [])):
                if "channel" not in ov:
                    errors.append(f"channels[{i}].overrides[{j}]: missing 'channel'")
                if "level" not in ov:
                    errors.append(f"channels[{i}].overrides[{j}]: missing 'level'")
                elif ov["level"] not in VALID_LEVELS:
                    errors.append(f"channels[{i}].overrides[{j}]: invalid level '{ov['level']}'")

    # Validate defaults
    defaults = config.get("defaults", {})
    if isinstance(defaults, dict):
        for key in ("unknown_channel", "unknown_dm"):
            val = defaults.get(key)
            if val and val not in VALID_LEVELS:
                errors.append(f"defaults.{key}: invalid level '{val}'")
    else:
        errors.append("'defaults' must be a mapping")

    # Security check: warn if any default is sovereign
    if defaults.get("unknown_channel") == "sovereign" or defaults.get("unknown_dm") == "sovereign":
        errors.append("SECURITY: defaults should never be 'sovereign' — this grants full access to unknown channels")

    return errors


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <config.yaml>")
        sys.exit(1)

    errors = validate(sys.argv[1])
    if errors:
        print(f"❌ Validation failed ({len(errors)} error(s)):\n")
        for e in errors:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("✅ Configuration is valid.")
        sys.exit(0)


if __name__ == "__main__":
    main()
