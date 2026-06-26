#!/usr/bin/env python3
"""Resolve the trust level for a specific channel ID."""

import sys
import fnmatch
import yaml
from pathlib import Path


def resolve(config_path: str, channel_id: str) -> dict:
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Check explicit channel matches
    for ch in config.get("channels", []):
        pattern = ch["id"]

        # Direct match or glob match
        if channel_id == pattern or fnmatch.fnmatch(channel_id, pattern):
            level = ch["level"]

            # Check overrides (for Discord-style server:channel patterns)
            # channel_id format: "discord:server_id:channel_name" or "discord:server_id"
            parts = channel_id.split(":")
            if len(parts) >= 3:
                channel_name = parts[-1]
                for ov in ch.get("overrides", []):
                    if fnmatch.fnmatch(channel_name, ov["channel"]):
                        return {
                            "channel_id": channel_id,
                            "level": ov["channel"],
                            "resolved_level": ov["level"],
                            "source": f"override '{ov['channel']}' in {pattern}",
                        }

            return {
                "channel_id": channel_id,
                "resolved_level": level,
                "source": f"channel rule '{pattern}'",
            }

    # Fall back to defaults
    defaults = config.get("defaults", {})
    is_dm = ":group:" not in channel_id and channel_id.count(":") == 1
    default_key = "unknown_dm" if is_dm else "unknown_channel"
    level = defaults.get(default_key, "observer")

    return {
        "channel_id": channel_id,
        "resolved_level": level,
        "source": f"default ({default_key})",
    }


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <config.yaml> <channel_id>")
        sys.exit(1)

    result = resolve(sys.argv[1], sys.argv[2])
    print(f"Channel:  {result['channel_id']}")
    print(f"Level:    {result['resolved_level']}")
    print(f"Source:   {result['source']}")


if __name__ == "__main__":
    main()
