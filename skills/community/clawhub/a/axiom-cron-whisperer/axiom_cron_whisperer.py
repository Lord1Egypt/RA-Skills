"""
🛠️ axiom-cron-whisperer — Cron Expression Explainer
====================================================

- Pas de support des syntaxes étendues (@yearly, @reboot, @hourly Quartz)
- Pas de calcul des N prochaines occurrences (sera ajouté en v0.2)
- Pas de gestion des L/W/# (Quartz)
- Locale unique (français par défaut)
- Pas de support des secondes (cron 6-fields Quartz)

EXPLIQUE UNE EXPRESSION CRON EN LANGAGE HUMAIN

Usage CLI:
    python3 axiom_cron_whisperer.py "0 9 * * 1-5"
    python3 axiom_cron_whisperer.py "*/15 * * * *"

Usage Python:
    from axiom_cron_whisperer import explain
    print(explain("0 9 * * 1-5"))  # "At 09:00, Monday through Friday"
"""

import re
import sys
from typing import List, Tuple

# Names for human output
MIN_NAMES = ["minute", "hour", "day of month", "month", "day of week"]

DAY_NAMES_EN = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
DAY_NAMES_FR = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"]
MONTH_NAMES_EN = ["", "January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
MONTH_NAMES_FR = ["", "janvier", "février", "mars", "avril", "mai", "juin",
                  "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


# ============================================================================
# Cron field parsing
# ============================================================================

def parse_field(field: str, min_val: int, max_val: int) -> List[int]:
    """
    Parse a single cron field into a sorted list of values.

    Supports: *, N, N,M, N-M, */N
    """
    values = set()

    for part in field.split(","):
        # Step
        if "/" in part:
            base, step = part.split("/", 1)
            step = int(step)
            if base == "*":
                start, end = min_val, max_val
            elif "-" in base:
                start, end = map(int, base.split("-", 1))
            else:
                start = int(base)
                end = max_val
            for v in range(start, end + 1, step):
                if min_val <= v <= max_val:
                    values.add(v)
        # Range
        elif "-" in part:
            start, end = map(int, part.split("-", 1))
            for v in range(start, end + 1):
                if min_val <= v <= max_val:
                    values.add(v)
        # Wildcard
        elif part == "*":
            for v in range(min_val, max_val + 1):
                values.add(v)
        # Exact value
        else:
            v = int(part)
            if min_val <= v <= max_val:
                values.add(v)
            else:
                raise ValueError(f"Valeur {v} hors limites [{min_val}-{max_val}]")

    return sorted(values)


def parse_cron(expr: str) -> dict:
    """
    Parse a 5-field cron expression.

    Returns dict with keys: minute, hour, day, month, dow
    Each value is a sorted list of integers.
    """
    expr = expr.strip()
    parts = expr.split()
    if len(parts) != 5:
        raise ValueError(f"Cron doit avoir 5 champs, reçu {len(parts)}: {expr}")

    return {
        "minute": parse_field(parts[0], 0, 59),
        "hour": parse_field(parts[1], 0, 23),
        "day": parse_field(parts[2], 1, 31),
        "month": parse_field(parts[3], 1, 12),
        "dow": parse_field(parts[4], 0, 6),  # 0 = Sunday
    }


# ============================================================================
# Human explanation
# ============================================================================

def _format_value_list(values: List[int], names: List[str] = None) -> str:
    """Format a list of values, using names if available."""
    if names:
        return ", ".join(names[v] if 0 <= v < len(names) else str(v) for v in values)
    if len(values) == 1:
        return str(values[0])
    if len(values) == max(values) - min(values) + 1:
        return f"{min(values)}-{max(values)}"
    return ", ".join(str(v) for v in values)


def explain_minute(minutes: List[int]) -> str:
    """Explain the minute field."""
    if minutes == list(range(0, 60)):
        return "every minute"
    if minutes == [0]:
        return "at minute 0"
    if len(minutes) == 60:
        return "every minute"
    if len(minutes) > 1 and minutes[1] - minutes[0] == minutes[2] - minutes[1] and minutes[0] == 0:
        step = minutes[1] - minutes[0]
        return f"every {step} minutes"
    return f"at minutes {_format_value_list(minutes)}"


def explain_hour(hours: List[int]) -> str:
    """Explain the hour field."""
    if hours == list(range(0, 24)):
        return "every hour"
    if len(hours) == 24:
        return "every hour"
    if len(hours) == 1:
        return f"at {hours[0]:02d}:00"
    return f"at hours {_format_value_list(hours)}"


def explain_day_of_month(days: List[int]) -> str:
    """Explain the day-of-month field."""
    if days == list(range(1, 32)):
        return "every day"
    if len(days) == 31:
        return "every day"
    if len(days) == 1:
        return f"on day {days[0]} of the month"
    return f"on days {_format_value_list(days)} of the month"


def explain_month(months: List[int], lang: str = "en") -> str:
    """Explain the month field."""
    names = MONTH_NAMES_FR if lang == "fr" else MONTH_NAMES_EN
    if months == list(range(1, 13)):
        return "every month"
    if len(months) == 12:
        return "every month"
    if len(months) == 1:
        return f"in {names[months[0]]}"
    return f"in {_format_value_list(months, names)}"


def explain_dow(dows: List[int], lang: str = "en") -> str:
    """Explain the day-of-week field."""
    names = DAY_NAMES_FR if lang == "fr" else DAY_NAMES_EN
    if dows == list(range(0, 7)):
        return "every day of the week"
    if len(dows) == 7:
        return "every day of the week"
    if len(dows) == 1:
        return f"on {names[dows[0]]}"
    # Check if it's a contiguous range
    if len(dows) > 1 and all(dows[i+1] - dows[i] == 1 for i in range(len(dows)-1)):
        return f"{names[dows[0]]} through {names[dows[-1]]}"
    return f"on {_format_value_list(dows, names)}"


def explain(expr: str, lang: str = "en") -> str:
    """
    Explique une expression cron en langage humain.

    Args:
        expr: cron expression (5 fields)
        lang: "en" or "fr"

    Returns:
        Explication humaine de l'expression

    Raises:
        ValueError: si l'expression est invalide
    """
    parsed = parse_cron(expr)
    parts = []
    parts.append(explain_minute(parsed["minute"]))
    parts.append(explain_hour(parsed["hour"]))
    parts.append(explain_day_of_month(parsed["day"]))
    parts.append(explain_month(parsed["month"], lang=lang))
    parts.append(explain_dow(parsed["dow"], lang=lang))
    return ", ".join(parts)


# ============================================================================
# Validation
# ============================================================================

def is_valid(expr: str) -> bool:
    """Check if a cron expression is valid."""
    try:
        parse_cron(expr)
        return True
    except (ValueError, IndexError):
        return False


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="axiom-cron-whisperer — Explain cron in human language"
    )
    parser.add_argument(
        "expression",
        nargs="?",
        help="Cron expression (5 fields)"
    )
    parser.add_argument(
        "--lang", choices=["en", "fr"], default="en",
        help="Language for explanation (en or fr)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Just validate the expression (exit 0/1)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON with parsed fields + explanation"
    )
    args = parser.parse_args()

    if not args.expression:
        parser.print_help()
        return 1

    try:
        if args.validate:
            if is_valid(args.expression):
                print("✅ Valid cron expression")
                return 0
            else:
                print("❌ Invalid cron expression")
                return 1

        if args.json:
            import json
            parsed = parse_cron(args.expression)
            return {
                "expression": args.expression,
                "parsed": parsed,
                "explanation": explain(args.expression, lang=args.lang),
                "valid": True
            }

        # Default: just explain
        print(explain(args.expression, lang=args.lang))
        return 0

    except ValueError as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
