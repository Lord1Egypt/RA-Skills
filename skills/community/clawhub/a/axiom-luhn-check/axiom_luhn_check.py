"""
🛠️ axiom-luhn-check — Luhn Algorithm Validator
================================================

⚠️ LIMITATIONS CONNUES :
- Détection limitée du type de carte (Visa/MC/Amex) — binaire
- Pas de validation du préfixe IIN pour chaque réseau
- Pas de support des BIN ranges en temps réel

VALIDATEUR LUHN — CB, SIRET, IMEI, ISBN-10

Usage CLI:
    python3 axiom_luhn_check.py "4532015112830366"
    python3 axiom_luhn_check.py "4532 0151 1283 0366" --type credit_card
"""

import re
import sys
from typing import Optional


# ============================================================================
# Luhn algorithm
# ============================================================================

def luhn_check(number_str: str) -> bool:
    """
    Apply the Luhn algorithm to a number string.

    Returns True if the number passes the Luhn check.
    """
    # Strip non-digits
    digits = re.sub(r"\D", "", number_str)
    if not digits:
        return False

    # Luhn: from right, double every second digit. If > 9, sum digits.
    total = 0
    for i, digit in enumerate(reversed(digits)):
        d = int(digit)
        if i % 2 == 1:  # Every second from right (0-indexed)
            d *= 2
            if d > 9:
                d = d - 9
        total += d

    return total % 10 == 0


# ============================================================================
# Type detection
# ============================================================================

def detect_type(number_str: str) -> str:
    """
    Detect what kind of number this is (best guess).
    """
    digits = re.sub(r"\D", "", number_str)
    length = len(digits)

    # Amex: 15 digits, starts with 34/37
    if length == 15 and digits[:2] in ("34", "37"):
        return "credit_card_amex"

    # IMEI: 15 digits (default for 15-digit, before generic CC)
    if length == 15:
        return "imei"

    # Credit card (other): 13-19 digits, starts with 2-6
    if 13 <= length <= 19 and digits[0] in "23456":
        # Try to detect specific card type
        if digits.startswith("4"):
            return "credit_card_visa"
        if digits[:2] in ("51", "52", "53", "54", "55"):
            return "credit_card_mastercard"
        if digits[:4] == "6011" or digits[:2] == "65":
            return "credit_card_discover"
        return "credit_card"

    # ISBN-10: 10 digits (last can be X)
    if length == 10:
        return "isbn_10"

    # ISBN-13: 13 digits, starts with 978 or 979
    if length == 13 and digits[:3] in ("978", "979"):
        return "isbn_13"

    # SIRET: 14 digits (French company ID)
    if length == 14:
        return "siret"

    # SIREN: 9 digits
    if length == 9:
        return "siren"

    # FrenchRIB: 23 digits
    if length == 23:
        return "rib"

    return "unknown"


# ============================================================================
# Public API
# ============================================================================

def validate(number_str: str, expected_type: str = None) -> dict:
    """
    Valide un numéro avec l'algo Luhn + détection de type.

    Args:
        number_str: le numéro à valider (peut contenir espaces/tirets)
        expected_type: force un type ('credit_card', 'imei', etc.) — optionnel

    Returns:
        dict avec valid, luhn_ok, type, detected_type, etc.
    """
    if not isinstance(number_str, str):
        raise TypeError(f"number_str doit être str, reçu {type(number_str).__name__}")

    digits = re.sub(r"\D", "", number_str)
    if not digits:
        return {
            "valid": False,
            "luhn_ok": False,
            "type": "unknown",
            "error": "no digits found",
            "original": number_str,
        }

    detected = detect_type(number_str)
    luhn_ok = luhn_check(digits)

    if expected_type:
        # Force type and check if matches
        type_match = detected == expected_type
    else:
        expected_type = detected
        type_match = True

    return {
        "valid": luhn_ok and type_match and detected != "unknown",
        "luhn_ok": luhn_ok,
        "type": expected_type,
        "detected_type": detected,
        "type_match": type_match,
        "length": len(digits),
        "digits": digits,
        "original": number_str,
    }


def format_credit_card(number_str: str) -> str:
    """Format credit card with spaces (4-4-4-4 for Visa/MC, 4-6-5 for Amex)."""
    digits = re.sub(r"\D", "", number_str)
    detected = detect_type(number_str)
    if "amex" in detected:
        return f"{digits[:4]} {digits[4:10]} {digits[10:]}"
    # Standard 4-4-4-4
    parts = [digits[i:i+4] for i in range(0, len(digits), 4)]
    return " ".join(parts)


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="axiom-luhn-check — Luhn validator "
    )
    parser.add_argument("number", nargs="?", help="Number to validate")
    parser.add_argument("--type", help="Force a specific type (credit_card, imei, isbn, siret)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--format", action="store_true", help="Reformat credit card with spaces")
    args = parser.parse_args()

    if not args.number:
        parser.print_help()
        return 1

    try:
        result = validate(args.number, expected_type=args.type)

        if args.json:
            import json
            print(json.dumps(result, indent=2))
        else:
            icon = "✅" if result["valid"] else "❌"
            print(f"{icon} {result['type']}")
            print(f"   Luhn check: {'OK' if result['luhn_ok'] else 'FAIL'}")
            print(f"   Length:     {result['length']} digits")
            print(f"   Detected:   {result['detected_type']}")
            if not result["type_match"]:
                print(f"   ⚠️  Type mismatch: expected {result['type']}, got {result['detected_type']}")
            if args.format and "credit_card" in result["type"]:
                print(f"   Formatted:  {format_credit_card(args.number)}")

        return 0 if result["valid"] else 1

    except Exception as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
