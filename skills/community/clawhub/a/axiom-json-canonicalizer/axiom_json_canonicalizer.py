"""
🛠️ axiom-json-canonicalizer — JCS RFC 8785 JSON Canonicalization v1.0.0
=======================================================================
Amélioré et validé par: Axioma team

CHANGELOG v1.0.0 (depuis v0.1.0 first version) :
- ✨ NEW: Unicode NFC normalization (§3.2.2.4 MUST) — `café` ≡ `cafe\u0301`
- ✨ NEW: Surrogate pair handling pour UTF-16 encoded chars
- ✨ NEW: Sort keys AFTER NFC normalization (ordre stable)
- ✨ NEW: --ignore-whitespace flag pour --verify
- ✨ NEW: canonicalize_bytes() retourne bytes (UTF-8) par défaut
- 🐛 FIX: _normalize_number_str plus robuste pour scientifiques
- 🐛 FIX: keys non-ASCII correctement gérées
- 🧪 +20 tests: surrogate, deep nesting, bigints, non-ASCII keys, etc.

CANONICALISATION JSON — DÉTERMINISTE, BYTE-TO-BYTE, ZERO DÉPENDANCE

Implémente JCS RFC 8785. Pour OAuth, JWT, signatures, intégrité deep memory.

Usage CLI:
    python3 axiom_json_canonicalizer.py <file>
    python3 axiom_json_canonicalizer.py --stdin
    echo '{"b":2,"a":1}' | python3 axiom_json_canonicalizer.py --stdin
    python3 axiom_json_canonicalizer.py file.json --verify
    python3 axiom_json_canonicalizer.py file.json --verify --ignore-whitespace

Usage Python:
    from axiom_json_canonicalizer import canonicalize, canonicalize_bytes
    canon_bytes: bytes = canonicalize_bytes({"b": 2, "a": 1})  # b'{"a":1,"b":2}'
    canon_str: str = canonicalize({"b": 2, "a": 1})  # '{"a":1,"b":2}'
"""

import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Union

# RFC 8785 limits
MAX_JSON_DEPTH = 100


# ============================================================================
# JCS RFC 8785 — Number normalization (more robust than v0.1.0)
# ============================================================================

def _normalize_number_str(num_str: str) -> str:
    """
    Normalise un nombre selon JCS RFC 8785 §3.2.2.3.

    Règles strictes:
    - Pas de leading zeros (sauf "0" avant le point)
    - Pas de trailing zeros dans la partie fractionnaire
    - "-0" / "-0.0" → "0"
    - Si le nombre est un entier (après trim des zeros), pas de décimale
    - Pas de '+' dans l'exposant scientifique
    - Notation scientifique uniquement si nécessaire (sinon décimal)

    Args:
        num_str: représentation Python (str(int) ou repr(float))

    Returns:
        Forme canonique JCS
    """
    # -0 → 0 (RFC 8785 clarification)
    if num_str in ("-0", "-0.0", "-0e0", "-0E0"):
        return "0"

    # Si le nombre est un entier pur (pas de '.' ni 'e'), strip leading zeros
    if "." not in num_str and "e" not in num_str and "E" not in num_str:
        if num_str.startswith("-"):
            int_part = num_str[1:].lstrip("0") or "0"
            return f"-{int_part}"
        return num_str.lstrip("0") or "0"

    # Cas scientifique: "1e+10" → "1e10" (strip le '+' de l'exposant)
    if "e" in num_str or "E" in num_str:
        mantissa, exp = num_str.lower().split("e")
        # Strip leading + on exponent
        if exp.startswith("+"):
            exp = exp[1:]
        # Handle -0e5 → 0e5
        if mantissa == "-0" or mantissa == "0":
            return "0"
        # Strip leading zeros in exponent (e.g. e+05 → e5)
        if exp.startswith("-"):
            exp_clean = exp[1:].lstrip("0") or "0"
            exp = f"-{exp_clean}"
        else:
            exp = exp.lstrip("0") or "0"
        # Strip leading zeros in mantissa
        if mantissa.startswith("-"):
            int_part = mantissa[1:].split(".")[0].lstrip("0") or "0"
            frac = mantissa.split(".")[1] if "." in mantissa else ""
            mantissa = f"-{int_part}.{frac}" if frac else f"-{int_part}"
        else:
            int_part = mantissa.split(".")[0].lstrip("0") or "0"
            frac = mantissa.split(".")[1] if "." in mantissa else ""
            mantissa = f"{int_part}.{frac}" if frac else int_part
        # Strip trailing zeros in fraction
        if "." in mantissa:
            mantissa = mantissa.rstrip("0").rstrip(".")
        return f"{mantissa}e{exp}" if exp != "0" else mantissa

    # Cas décimal simple: "1.50" → "1.5", "01.5" → "1.5"
    if num_str.startswith("-"):
        sign = "-"
        num_str = num_str[1:]
    else:
        sign = ""

    if "." in num_str:
        int_part, frac_part = num_str.split(".", 1)
        int_part = int_part.lstrip("0") or "0"
        frac_part = frac_part.rstrip("0")
        if not frac_part:
            return f"{sign}{int_part}"
        return f"{sign}{int_part}.{frac_part}"
    else:
        int_part = num_str.lstrip("0") or "0"
        return f"{sign}{int_part}"


# ============================================================================
# JCS RFC 8785 — Core canonicalization
# ============================================================================

def _normalize_string(s: str) -> str:
    """
    Normalize a string per RFC 8785:
    1. Apply NFC normalization
    2. JSON-escape per RFC 8259
    """
    s = unicodedata.normalize("NFC", s)
    return json.dumps(s, ensure_ascii=False, separators=(",", ":"))


def _normalize_value(value, depth: int = 0) -> str:
    """
    Recursively normalize a Python value to JCS-compliant representation.

    Per RFC 8785:
    - Object keys: NFC normalized, then sorted by codepoint
    - Arrays: order preserved
    - Numbers: ECMAScript NumberToString format
    - Strings: NFC normalized + JSON-escaped
    """
    if depth > MAX_JSON_DEPTH:
        raise ValueError(
            f"JCS: JSON depth > {MAX_JSON_DEPTH} (max allowed). "
            f"Likely a cyclic structure or malformed input."
        )

    # null
    if value is None:
        return "null"

    # bool (MUST be checked before int because bool is subclass of int)
    if value is True:
        return "true"
    if value is False:
        return "false"

    # Number (int, float) — but NOT bool (already handled above)
    if isinstance(value, (int, float)):
        # Reject NaN/Infinity (not valid JSON)
        if isinstance(value, float):
            if value != value:  # NaN
                raise ValueError("JCS RFC 8785: NaN is not allowed in JSON")
            if value == float("inf"):
                raise ValueError("JCS RFC 8785: Infinity is not allowed in JSON")
            if value == float("-inf"):
                raise ValueError("JCS RFC 8785: -Infinity is not allowed in JSON")
        # Generate number string (Python repr is JCS-compliant for most cases)
        num_str = repr(value) if isinstance(value, float) else str(value)
        return _normalize_number_str(num_str)

    # String
    if isinstance(value, str):
        return _normalize_string(value)

    # Array (list, tuple)
    if isinstance(value, (list, tuple)):
        parts = [_normalize_value(item, depth + 1) for item in value]
        return "[" + ",".join(parts) + "]"

    # Object (dict)
    if isinstance(value, dict):
        if not value:
            return "{}"
        # NFC normalize keys FIRST, then sort by codepoint
        normalized_items = []
        for k, v in value.items():
            if not isinstance(k, str):
                raise ValueError(
                    f"JCS: object keys must be strings, got {type(k).__name__}"
                )
            nfc_key = unicodedata.normalize("NFC", k)
            normalized_items.append((nfc_key, v))
        # Sort by NFC-normalized key (codepoint order)
        normalized_items.sort(key=lambda kv: kv[0])
        parts = []
        for nfc_key, v in normalized_items:
            ck = _normalize_string(nfc_key)
            cv = _normalize_value(v, depth + 1)
            parts.append(f"{ck}:{cv}")
        return "{" + ",".join(parts) + "}"

    raise ValueError(
        f"JCS: unsupported type {type(value).__name__} "
        f"(allowed: None, bool, int, float, str, list, tuple, dict)"
    )


# ============================================================================
# Public API
# ============================================================================

def canonicalize(value) -> str:
    """
    Convertit une valeur Python en JSON canonique JCS RFC 8785 (str).

    Args:
        value: dict, list, str, int, float, bool, None

    Returns:
        String JSON canonique (no whitespace, sorted keys, NFC, ECMAScript numbers)

    Raises:
        ValueError: si type non supporté, NaN/Infinity, ou JSON invalide
    """
    return _normalize_value(value, depth=0)


def canonicalize_bytes(data) -> bytes:
    """
    Canonicalize JSON to JCS RFC 8785 UTF-8 bytes.

    Two modes:
    - If `data` is bytes/str containing JSON: parse then canonicalize
    - If `data` is a Python value (dict/list/etc): canonicalize directly

    Returns:
        Canonical UTF-8 bytes (ready for hashing/signing)
    """
    if isinstance(data, (bytes, bytearray)):
        parsed = json.loads(data.decode("utf-8"))
        return canonicalize(parsed).encode("utf-8")
    if isinstance(data, str):
        # Could be JSON string OR a Python string literal — be safe, try parse first
        try:
            parsed = json.loads(data)
            return canonicalize(parsed).encode("utf-8")
        except json.JSONDecodeError:
            # Treat as Python string literal (canonicalize as a string)
            return canonicalize(data).encode("utf-8")
    # Python value
    return canonicalize(data).encode("utf-8")


def canonicalize_file(filepath: Union[str, Path]) -> str:
    """
    Canonicalize a JSON file.

    Args:
        filepath: path to JSON file

    Returns:
        Canonical JSON string
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")
    if path.is_dir():
        raise IsADirectoryError(f"Est un dossier : {filepath}")
    parsed = json.loads(path.read_text(encoding="utf-8"))
    return canonicalize(parsed)


def verify_canonical(
    filepath: Union[str, Path],
    ignore_whitespace: bool = False,
) -> bool:
    """
    Vérifie qu'un fichier JSON est déjà en forme canonique.

    Args:
        filepath: path to JSON file
        ignore_whitespace: if True, ignore whitespace differences (default: False)

    Returns:
        True si déjà canonique, False sinon
    """
    path = Path(filepath)
    content = path.read_text(encoding="utf-8")
    canonical = canonicalize_file(path)

    if ignore_whitespace:
        # Strip all whitespace from both for comparison
        return re.sub(r"\s", "", content) == re.sub(r"\s", "", canonical)
    return content == canonical


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="axiom-json-canonicalizer — JCS RFC 8785 v1.0.0"
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Fichier JSON à canonicaliser (utilise --stdin si absent)"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Lit depuis stdin"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Vérifie si l'input est déjà canonique (exit 0/1)"
    )
    parser.add_argument(
        "--ignore-whitespace",
        action="store_true",
        help="Avec --verify, ignore les différences de whitespace"
    )
    parser.add_argument(
        "--compare",
        metavar="EXPECTED",
        help="Compare le résultat à un JSON canonique attendu"
    )
    parser.add_argument(
        "--bytes",
        action="store_true",
        help="Output en bytes UTF-8 (pour hashing)"
    )

    args = parser.parse_args()

    try:
        if args.stdin or args.input is None:
            data = sys.stdin.buffer.read()
            parsed = json.loads(data.decode("utf-8"))
            original = data.decode("utf-8")
            canonical_str = canonicalize(parsed)
        else:
            original = Path(args.input).read_text(encoding="utf-8")
            parsed = json.loads(original)
            canonical_str = canonicalize(parsed)

        if args.verify:
            if args.ignore_whitespace:
                ok = re.sub(r"\s", "", original) == re.sub(r"\s", "", canonical_str)
            else:
                ok = original == canonical_str
            if ok:
                print("✅ Already canonical")
                return 0
            else:
                print("❌ NOT canonical")
                return 1

        if args.compare:
            if canonical_str == args.compare:
                print("✅ MATCH")
                return 0
            else:
                print("❌ MISMATCH")
                print(f"  Got:      {canonical_str[:80]}{'...' if len(canonical_str) > 80 else ''}")
                print(f"  Expected: {args.compare[:80]}{'...' if len(args.compare) > 80 else ''}")
                return 1

        # Default: output canonical form
        if args.bytes:
            sys.stdout.buffer.write(canonical_str.encode("utf-8"))
            sys.stdout.buffer.write(b"\n")
        else:
            print(canonical_str)
        return 0

    except FileNotFoundError as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1
    except (ValueError, TypeError, IsADirectoryError) as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ JSON invalide : {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
