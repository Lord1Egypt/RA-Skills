"""
🛠️ axiom-uuid-analyzer — UUID Inspector & Parser
==================================================

⚠️ LIMITATIONS CONNUES :
- UUID v6, v7, v8 partiellement supportés
- Pas de validation stricte de la variante Microsoft
- Pas de génération de UUID (analyse seulement)

ANALYSE UN UUID — EXTRAIT VERSION, VARIANTE, TIMESTAMP, ETC.

Usage CLI:
    python3 axiom_uuid_analyzer.py "550e8400-e29b-41d4-a716-446655440000"
    python3 axiom_uuid_analyzer.py --validate "..."
    python3 axiom_uuid_analyzer.py --batch file.txt

Usage Python:
    from axiom_uuid_analyzer import analyze, is_valid
    info = analyze("550e8400-e29b-41d4-a716-446655440000")
"""

import re
import sys
import uuid
from typing import Optional

# UUID format: 8-4-4-4-12 hex chars
UUID_PATTERN = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

# Variants (RFC 4122)
VARIANT_NCS = "NCS backward compatibility"
VARIANT_RFC4122 = "RFC 4122"
VARIANT_MICROSOFT = "Microsoft Corporation"
VARIANT_FUTURE = "Future (reserved)"


# ============================================================================
# Validation
# ============================================================================

def is_valid(uuid_str: str) -> bool:
    """Check if a string is a valid UUID format (any version)."""
    if not isinstance(uuid_str, str):
        return False
    return bool(UUID_PATTERN.match(uuid_str))


def parse_uuid(uuid_str: str) -> dict:
    """
    Parse un UUID et retourne ses composants.
    """
    if not is_valid(uuid_str):
        raise ValueError(f"UUID invalide: {uuid_str}")

    # Strip hyphens and normalize
    hex_str = uuid_str.replace("-", "").lower()

    time_low = int(hex_str[0:8], 16)
    time_mid = int(hex_str[8:12], 16)
    time_hi_and_version = int(hex_str[12:16], 16)
    clock_seq_hi_and_reserved = int(hex_str[16:18], 16)
    clock_seq_low = int(hex_str[18:20], 16)
    node = int(hex_str[20:32], 16)

    version = (time_hi_and_version >> 12) & 0xF
    variant_byte = clock_seq_hi_and_reserved

    # Determine variant
    if (variant_byte & 0x80) == 0x00:
        variant = VARIANT_NCS
        variant_code = "ncs"
    elif (variant_byte & 0xC0) == 0x80:
        variant = VARIANT_RFC4122
        variant_code = "rfc4122"
    elif (variant_byte & 0xE0) == 0xC0:
        variant = VARIANT_MICROSOFT
        variant_code = "microsoft"
    elif (variant_byte & 0xF0) == 0xE0:
        variant = VARIANT_FUTURE
        variant_code = "future"
    else:
        variant = "Unknown"
        variant_code = "unknown"

    # Clock sequence
    clock_seq = ((clock_seq_hi_and_reserved & 0x3F) << 8) | clock_seq_low

    # MAC address (for v1)
    mac_hex = ":".join(f"{(node >> (i*8)) & 0xFF:02x}" for i in range(5, -1, -1))
    # Note: node is in big-endian, but the MAC format above is reversed
    mac_bytes = [(node >> (i*8)) & 0xFF for i in range(5, -1, -1)]
    mac_formatted = ":".join(f"{b:02x}" for b in mac_bytes)

    return {
        "uuid": uuid_str,
        "valid": True,
        "version": version,
        "variant": variant,
        "variant_code": variant_code,
        "time_low": time_low,
        "time_mid": time_mid,
        "time_hi_and_version": time_hi_and_version,
        "clock_seq": clock_seq,
        "node": node,
        "mac_address": mac_formatted if version == 1 else None,
    }


# ============================================================================
# Version-specific analysis
# ============================================================================

def _extract_v1_timestamp(parsed: dict) -> Optional[dict]:
    """
    Extract the timestamp from a v1 UUID.

    v1 timestamp = 60 bits = 100-nanosecond intervals since Oct 15, 1582.
    """
    if parsed["version"] != 1:
        return None

    time_low = parsed["time_low"]
    time_mid = parsed["time_mid"]
    time_hi = parsed["time_hi_and_version"] & 0x0FFF

    # Combine into 60-bit timestamp
    timestamp_100ns = (time_hi << 48) | (time_mid << 32) | time_low

    # Convert to Unix timestamp
    # UUID epoch is Oct 15, 1582 = 12219292800 seconds before Unix epoch (Jan 1, 1970)
    GREGORIAN_EPOCH_TO_UNIX = 12219292800
    unix_seconds = (timestamp_100ns / 10_000_000) - GREGORIAN_EPOCH_TO_UNIX
    unix_ms = unix_seconds * 1000

    import datetime
    try:
        dt = datetime.datetime.fromtimestamp(unix_seconds, tz=datetime.timezone.utc)
        iso = dt.isoformat()
    except (ValueError, OSError):
        iso = None

    return {
        "timestamp_100ns": timestamp_100ns,
        "unix_seconds": unix_seconds,
        "unix_ms": unix_ms,
        "iso": iso,
    }


def _extract_v7_timestamp(parsed: dict) -> Optional[dict]:
    """
    Extract the timestamp from a v7 UUID.

    v7 timestamp = 48 bits = milliseconds since Unix epoch.
    """
    if parsed["version"] != 7:
        return None

    # First 48 bits = unix_ms
    time_low = parsed["time_low"]
    time_mid = parsed["time_mid"]
    unix_ms = (time_low << 16) | time_mid  # 48 bits

    unix_seconds = unix_ms / 1000
    import datetime
    try:
        dt = datetime.datetime.fromtimestamp(unix_seconds, tz=datetime.timezone.utc)
        iso = dt.isoformat()
    except (ValueError, OSError):
        iso = None

    return {
        "unix_ms": unix_ms,
        "unix_seconds": unix_seconds,
        "iso": iso,
    }


def analyze(uuid_str: str) -> dict:
    """
    Analyse complète d'un UUID.

    Returns:
        dict avec version, variant, timestamp (si applicable), MAC (si v1)
    """
    parsed = parse_uuid(uuid_str)

    result = dict(parsed)
    result["version_name"] = VERSION_NAMES.get(parsed["version"], f"unknown({parsed['version']})")
    result["is_time_based"] = parsed["version"] in (1, 6, 7)
    result["is_random"] = parsed["version"] in (4, 8)

    # Version-specific
    if parsed["version"] == 1:
        result["timestamp"] = _extract_v1_timestamp(parsed)
    elif parsed["version"] == 7:
        result["timestamp"] = _extract_v7_timestamp(parsed)
    elif parsed["version"] == 4:
        result["random"] = True

    return result


VERSION_NAMES = {
    1: "v1 (time-based, MAC address)",
    2: "v2 (DCE security)",
    3: "v3 (MD5 hash of name)",
    4: "v4 (random)",
    5: "v5 (SHA-1 hash of name)",
    6: "v6 (reordered time-based)",
    7: "v7 (time-ordered, random)",
    8: "v8 (custom)",
}


# ============================================================================
# Batch processing
# ============================================================================

def analyze_batch(uuid_strings):
    """Analyze a list of UUIDs."""
    results = []
    for u in uuid_strings:
        u = u.strip()
        if not u:
            continue
        try:
            results.append(analyze(u))
        except ValueError as e:
            results.append({"uuid": u, "valid": False, "error": str(e)})
    return results


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="axiom-uuid-analyzer — UUID inspector "
    )
    parser.add_argument("uuid", nargs="?", help="UUID à analyser")
    parser.add_argument("--validate", action="store_true", help="Valide seulement (exit 0/1)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--batch", metavar="FILE", help="Fichier avec un UUID par ligne")
    args = parser.parse_args()

    try:
        if args.batch:
            with open(args.batch, "r") as f:
                uuids = f.readlines()
            results = analyze_batch(uuids)
            if args.json:
                import json
                print(json.dumps(results, indent=2, default=str))
            else:
                for r in results:
                    if r.get("valid"):
                        print(f"✅ {r['uuid']}  v{r['version']}  {r['variant_code']}")
                    else:
                        print(f"❌ {r['uuid']}  {r.get('error', 'invalid')}")
            return 0

        if not args.uuid:
            parser.print_help()
            return 1

        if args.validate:
            if is_valid(args.uuid):
                print("✅ Valid UUID format")
                return 0
            else:
                print("❌ Invalid UUID format")
                return 1

        if args.json:
            import json
            print(json.dumps(analyze(args.uuid), indent=2, default=str))
        else:
            info = analyze(args.uuid)
            print(f"UUID:        {info['uuid']}")
            print(f"Version:     {info['version']} ({info['version_name']})")
            print(f"Variant:     {info['variant']} ({info['variant_code']})")
            if info.get("timestamp"):
                print(f"Timestamp:   {info['timestamp']['iso']} (Unix ms: {info['timestamp']['unix_ms']:.0f})")
            if info.get("mac_address"):
                print(f"MAC:         {info['mac_address']}")
            print(f"Type:        {'time-based' if info['is_time_based'] else 'random' if info['is_random'] else 'hash-based'}")
        return 0

    except ValueError as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
