"""
🛠️ axiom-iban-validator — IBAN Validator (ISO 13616, mod-97)
==============================================================

⚠️ LIMITATIONS CONNUES :
- ~40 pays principaux supportés (pas la liste ISO 13616 complète)
- Pas de validation BIC/SWIFT associé
- Pas de conversion BBAN ↔ IBAN

VALIDATEUR IBAN AVEC ALGORITHME MOD-97
"""

import re
import sys


# IBAN length by country (ISO 13616)
IBAN_LENGTHS = {
    "AD": 24, "AE": 23, "AL": 28, "AO": 25, "AT": 20, "AZ": 28,
    "BA": 20, "BE": 16, "BF": 27, "BG": 22, "BH": 22, "BI": 16,
    "BJ": 28, "BR": 29, "BY": 28, "CG": 24, "CH": 21, "CI": 28,
    "CM": 27, "CR": 22, "CV": 25, "CY": 28, "CZ": 24, "DE": 22,
    "DK": 18, "DO": 28, "DZ": 24, "EE": 20, "EG": 29, "ES": 24,
    "FI": 18, "FO": 18, "FR": 27, "GA": 27, "GB": 22, "GE": 22,
    "GI": 23, "GL": 18, "GR": 27, "GT": 28, "GW": 25, "HN": 28,
    "HR": 21, "HU": 28, "IE": 22, "IL": 23, "IQ": 23, "IR": 26,
    "IS": 26, "IT": 27, "JO": 30, "KM": 27, "KW": 30, "KZ": 20,
    "LB": 28, "LC": 32, "LI": 21, "LT": 20, "LU": 20, "LV": 21,
    "LY": 25, "MA": 28, "MC": 27, "MD": 24, "ME": 22, "MG": 27,
    "MK": 19, "ML": 28, "MR": 27, "MT": 31, "MU": 30, "MZ": 25,
    "NE": 28, "NI": 28, "NL": 18, "NO": 15, "OM": 23, "PK": 24,
    "PL": 28, "PS": 29, "PT": 25, "QA": 29, "RO": 24, "RS": 22,
    "RU": 33, "SA": 24, "SD": 18, "SE": 24, "SI": 19, "SK": 24,
    "SM": 27, "SN": 28, "SO": 23, "ST": 25, "SV": 28, "TD": 27,
    "TG": 28, "TL": 23, "TN": 24, "TR": 26, "UA": 29, "VA": 22,
    "VG": 24, "XK": 20, "YE": 30,
}


def _mod97(iban_str: str) -> bool:
    """Apply the mod-97 algorithm to an IBAN string (already rearranged)."""
    # Rearrange: move first 4 chars to end
    rearranged = iban_str[4:] + iban_str[:4]

    # Convert letters to numbers (A=10, B=11, ..., Z=35)
    numeric = ""
    for ch in rearranged:
        if ch.isdigit():
            numeric += ch
        elif ch.isalpha():
            numeric += str(ord(ch.upper()) - ord("A") + 10)
        else:
            return False  # invalid char

    # Compute mod 97 on the numeric string
    try:
        return int(numeric) % 97 == 1
    except ValueError:
        return False


def _format_iban(iban_str: str) -> str:
    """Format IBAN with spaces every 4 chars."""
    return " ".join(iban_str[i:i+4] for i in range(0, len(iban_str), 4))


def validate(iban: str) -> dict:
    """
    Validate an IBAN.

    Returns dict with: valid, country, length, check_passed, formatted, error
    """
    if not isinstance(iban, str):
        return {"valid": False, "error": "IBAN must be a string"}

    # Strip whitespace and dashes
    cleaned = re.sub(r"\s+|-", "", iban).upper()

    if len(cleaned) < 5:
        return {"valid": False, "error": "IBAN too short", "original": iban}

    if not re.match(r"^[A-Z]{2}\d{2}[A-Z0-9]+$", cleaned):
        return {"valid": False, "error": "Invalid format", "original": iban}

    country = cleaned[:2]
    expected_length = IBAN_LENGTHS.get(country)

    if expected_length is None:
        return {
            "valid": False,
            "country": country,
            "error": f"Unknown country code: {country}",
            "original": iban,
        }

    if len(cleaned) != expected_length:
        return {
            "valid": False,
            "country": country,
            "length": len(cleaned),
            "expected_length": expected_length,
            "error": f"Wrong length: {len(cleaned)} (expected {expected_length})",
            "original": iban,
        }

    check_ok = _mod97(cleaned)

    return {
        "valid": check_ok,
        "country": country,
        "length": len(cleaned),
        "check_passed": check_ok,
        "formatted": _format_iban(cleaned),
        "bban": cleaned[4:],
        "original": iban,
    }


# Test IBANs (from Wikipedia, all valid)
TEST_IBANS = [
    ("GB82 WEST 1234 5698 7654 32", "GB", True),
    ("DE89370400440532013000", "DE", True),
    ("FR7630006000011234567890189", "FR", True),
    ("BE68539007547034", "BE", True),
]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="axiom-iban-validator ")
    parser.add_argument("iban", nargs="?", help="IBAN to validate")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if not args.iban:
        for iban, country, _ in TEST_IBANS:
            result = validate(iban)
            icon = "✅" if result["valid"] else "❌"
            print(f"{icon} {result.get('formatted', iban)}  [{country}]")
        return 0

    result = validate(args.iban)
    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        if result["valid"]:
            print(f"✅ Valid IBAN: {result['formatted']}")
            print(f"   Country: {result['country']}")
        else:
            print(f"❌ Invalid: {result.get('error', 'unknown')}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
