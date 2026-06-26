#!/usr/bin/env python3
"""Audit configured channels and report trust level summary."""

import sys
import yaml
from pathlib import Path

LEVEL_RISK = {
    "sovereign": "🔴 CRITICAL",
    "trusted": "🟡 ELEVATED",
    "guarded": "🟢 NORMAL",
    "observer": "🔵 MINIMAL",
    "silent": "⚪ NONE",
}


def audit(config_path: str):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    print("=" * 60)
    print("  Chitin Trust Channels — Audit Report")
    print("=" * 60)

    # Owner
    owner = config.get("owner", {})
    print(f"\n👤 Owner identities: {len(owner)}")
    for platform, identity in owner.items():
        print(f"   • {platform}: {identity}")

    # Channel rules
    channels = config.get("channels", [])
    print(f"\n📡 Channel rules: {channels.__len__()}")

    level_counts = {}
    for ch in channels:
        level = ch["level"]
        level_counts[level] = level_counts.get(level, 0) + 1
        risk = LEVEL_RISK.get(level, "❓ UNKNOWN")
        print(f"   • {ch['id']} → {level} ({risk})")

        for ov in ch.get("overrides", []):
            ov_risk = LEVEL_RISK.get(ov["level"], "❓ UNKNOWN")
            print(f"     ↳ {ov['channel']} → {ov['level']} ({ov_risk})")
            level_counts[ov["level"]] = level_counts.get(ov["level"], 0) + 1

    # Defaults
    defaults = config.get("defaults", {})
    print(f"\n🔒 Defaults:")
    for key, val in defaults.items():
        risk = LEVEL_RISK.get(val, "❓ UNKNOWN")
        print(f"   • {key} → {val} ({risk})")

    # Summary
    print(f"\n📊 Trust Level Distribution:")
    for level in ["sovereign", "trusted", "guarded", "observer", "silent"]:
        count = level_counts.get(level, 0)
        risk = LEVEL_RISK.get(level, "")
        if count:
            print(f"   • {level}: {count} channel(s) {risk}")

    # Security warnings
    print(f"\n⚠️  Security Checks:")
    sovereign_count = level_counts.get("sovereign", 0)
    if sovereign_count > 2:
        print(f"   🔴 WARNING: {sovereign_count} sovereign channels — minimize these")
    elif sovereign_count > 0:
        print(f"   ✅ {sovereign_count} sovereign channel(s) — acceptable")
    
    if defaults.get("unknown_channel") in ("sovereign", "trusted"):
        print(f"   🔴 CRITICAL: unknown_channel defaults to '{defaults['unknown_channel']}' — should be 'observer' or 'guarded'")
    else:
        print(f"   ✅ unknown_channel defaults to '{defaults.get('unknown_channel', 'observer')}' — safe")

    if defaults.get("unknown_dm") in ("sovereign",):
        print(f"   🔴 CRITICAL: unknown_dm defaults to 'sovereign' — should be 'guarded' or lower")
    else:
        print(f"   ✅ unknown_dm defaults to '{defaults.get('unknown_dm', 'guarded')}' — safe")

    print(f"\n{'=' * 60}")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <config.yaml>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ Config not found: {sys.argv[1]}")
        sys.exit(1)

    audit(sys.argv[1])


if __name__ == "__main__":
    main()
