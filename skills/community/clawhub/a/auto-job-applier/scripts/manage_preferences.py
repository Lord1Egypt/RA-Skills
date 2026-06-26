#!/usr/bin/env python3
"""
manage_preferences.py — Persistent user preferences for the Auto Job Applier skill.

Stores and retrieves user answers to application questions that are not present
in their ResumeX resume (salary expectations, visa status, screening question
answers, etc.). Saves to a local JSON file so the user is never asked the same
question twice.

Usage:
    # List all saved preferences
    python3 manage_preferences.py list

    # Get a specific preference
    python3 manage_preferences.py get salary_expectation

    # Set a preference
    python3 manage_preferences.py set salary_expectation "8-12 LPA"
    python3 manage_preferences.py set notice_period "30 days"
    python3 manage_preferences.py set willing_to_relocate true

    # Set a screening question answer
    python3 manage_preferences.py set-screening "authorized_to_work_india" "Yes"
    python3 manage_preferences.py set-screening "require_sponsorship" "No"

    # Find a screening answer by fuzzy question text
    python3 manage_preferences.py find-screening "Are you authorized to work"

    # Delete a preference
    python3 manage_preferences.py delete notice_period

    # Reset all preferences
    python3 manage_preferences.py reset

Output:
    JSON to stdout. Errors and messages to stderr.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Preferences file location ────────────────────────────────────────────────
# Store in the skill's data directory, adjacent to scripts/
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
PREFS_FILE = DATA_DIR / "user_preferences.json"

# ── Known preference keys with descriptions ──────────────────────────────────
KNOWN_KEYS = {
    "salary_expectation": "Expected salary range (e.g. '8-12 LPA' or '$80,000-$100,000')",
    "currency": "Preferred currency for salary (e.g. 'INR', 'USD')",
    "notice_period": "Current notice period (e.g. '30 days', 'Immediate')",
    "visa_status": "Visa/citizenship status (e.g. 'Indian citizen', 'H1B holder')",
    "work_authorization": "Work authorization (e.g. 'Authorized to work in India')",
    "willing_to_relocate": "Whether willing to relocate (true/false)",
    "preferred_work_type": "Preferred work arrangement ('remote', 'hybrid', 'onsite')",
    "gender": "Gender identity (for diversity forms)",
    "ethnicity": "Ethnicity (for diversity forms, optional)",
    "disability_status": "Disability status (for compliance forms)",
    "veteran_status": "Veteran status (for compliance forms)",
    "highest_education": "Highest education level (e.g. 'B.Tech', 'M.S.')",
    "graduation_year": "Year of graduation",
    "date_of_birth": "Date of birth (for forms that require it)",
    "current_ctc": "Current CTC/compensation",
    "expected_ctc": "Expected CTC/compensation",
    "linkedin_url": "LinkedIn profile URL (backup if not in resume)",
    "portfolio_url": "Portfolio URL (backup if not in resume)",
    "github_url": "GitHub URL (backup if not in resume)",
    "address_line1": "Street address line 1",
    "address_line2": "Street address line 2",
    "city": "City",
    "state": "State/Province",
    "zip_code": "ZIP/Postal code",
    "country": "Country",
}


def _load_preferences() -> dict:
    """Load preferences from disk, return empty dict if not found."""
    if not PREFS_FILE.exists():
        return {
            "screening_answers": {},
            "saved_at": None,
        }
    try:
        with open(PREFS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"WARNING: Could not read preferences file: {e}", file=sys.stderr)
        return {"screening_answers": {}, "saved_at": None}


def _save_preferences(prefs: dict) -> None:
    """Save preferences to disk, creating the data directory if needed."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    prefs["saved_at"] = datetime.now(timezone.utc).isoformat()
    with open(PREFS_FILE, "w") as f:
        json.dump(prefs, f, indent=2, ensure_ascii=False)
    print(f"Preferences saved to {PREFS_FILE}", file=sys.stderr)


def _parse_value(value: str):
    """Parse a string value into the appropriate Python type."""
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _fuzzy_match(query: str, candidates: dict, threshold: float = 0.4) -> list:
    """Simple fuzzy matching: find keys whose words overlap with the query."""
    query_words = set(query.lower().split())
    matches = []
    for key, value in candidates.items():
        key_words = set(key.lower().replace("_", " ").split())
        overlap = len(query_words & key_words)
        total = len(query_words | key_words)
        if total > 0:
            similarity = overlap / total
            if similarity >= threshold:
                matches.append((key, value, similarity))
    return sorted(matches, key=lambda x: x[2], reverse=True)


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_list(args):
    prefs = _load_preferences()
    if not prefs or (len(prefs) <= 2 and not prefs.get("screening_answers")):
        print(json.dumps({"message": "No preferences saved yet."}, indent=2))
    else:
        print(json.dumps(prefs, indent=2, ensure_ascii=False))


def cmd_get(args):
    prefs = _load_preferences()
    key = args.key

    # Check top-level
    if key in prefs:
        result = {"key": key, "value": prefs[key]}
        print(json.dumps(result, indent=2))
        return

    # Check screening answers
    screening = prefs.get("screening_answers", {})
    if key in screening:
        result = {"key": key, "value": screening[key], "source": "screening_answers"}
        print(json.dumps(result, indent=2))
        return

    # Not found
    print(json.dumps({"key": key, "value": None, "found": False}, indent=2))


def cmd_set(args):
    prefs = _load_preferences()
    key = args.key
    value = _parse_value(args.value)

    old_value = prefs.get(key)
    prefs[key] = value
    _save_preferences(prefs)

    result = {"key": key, "value": value, "previous": old_value}
    if key in KNOWN_KEYS:
        result["description"] = KNOWN_KEYS[key]
    print(json.dumps(result, indent=2))


def cmd_set_screening(args):
    prefs = _load_preferences()
    if "screening_answers" not in prefs:
        prefs["screening_answers"] = {}

    key = args.key
    value = _parse_value(args.value)

    old_value = prefs["screening_answers"].get(key)
    prefs["screening_answers"][key] = value
    _save_preferences(prefs)

    result = {
        "key": key,
        "value": value,
        "previous": old_value,
        "source": "screening_answers",
    }
    print(json.dumps(result, indent=2))


def cmd_find_screening(args):
    prefs = _load_preferences()
    screening = prefs.get("screening_answers", {})

    if not screening:
        print(json.dumps({
            "query": args.question,
            "found": False,
            "message": "No screening answers saved yet.",
        }, indent=2))
        return

    matches = _fuzzy_match(args.question, screening)
    if matches:
        best_key, best_value, confidence = matches[0]
        result = {
            "query": args.question,
            "found": True,
            "key": best_key,
            "value": best_value,
            "confidence": round(confidence, 2),
            "all_matches": [
                {"key": k, "value": v, "confidence": round(c, 2)}
                for k, v, c in matches[:5]
            ],
        }
    else:
        result = {
            "query": args.question,
            "found": False,
            "message": "No matching screening answer found. Ask the user.",
        }
    print(json.dumps(result, indent=2))


def cmd_delete(args):
    prefs = _load_preferences()
    key = args.key

    deleted = False
    if key in prefs:
        del prefs[key]
        deleted = True
    elif key in prefs.get("screening_answers", {}):
        del prefs["screening_answers"][key]
        deleted = True

    if deleted:
        _save_preferences(prefs)
        print(json.dumps({"key": key, "deleted": True}, indent=2))
    else:
        print(json.dumps({"key": key, "deleted": False, "message": "Key not found"}, indent=2))


def cmd_reset(args):
    if PREFS_FILE.exists():
        os.remove(PREFS_FILE)
        print(json.dumps({"reset": True, "message": "All preferences cleared."}, indent=2))
    else:
        print(json.dumps({"reset": False, "message": "No preferences file to reset."}, indent=2))


def cmd_known_keys(args):
    """List all known preference keys with descriptions."""
    print(json.dumps(KNOWN_KEYS, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Manage persistent user preferences for the Auto Job Applier skill"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    subparsers.add_parser("list", help="List all saved preferences")

    # get
    g = subparsers.add_parser("get", help="Get a specific preference")
    g.add_argument("key", help="Preference key to retrieve")

    # set
    s = subparsers.add_parser("set", help="Set a preference")
    s.add_argument("key", help="Preference key")
    s.add_argument("value", help="Preference value")

    # set-screening
    ss = subparsers.add_parser("set-screening", help="Set a screening question answer")
    ss.add_argument("key", help="Screening question key (snake_case)")
    ss.add_argument("value", help="Answer value")

    # find-screening
    fs = subparsers.add_parser("find-screening", help="Find a screening answer by question text")
    fs.add_argument("question", help="Question text to search for")

    # delete
    d = subparsers.add_parser("delete", help="Delete a preference")
    d.add_argument("key", help="Preference key to delete")

    # reset
    subparsers.add_parser("reset", help="Reset all preferences")

    # known-keys
    subparsers.add_parser("known-keys", help="List all known preference keys")

    args = parser.parse_args()

    commands = {
        "list": cmd_list,
        "get": cmd_get,
        "set": cmd_set,
        "set-screening": cmd_set_screening,
        "find-screening": cmd_find_screening,
        "delete": cmd_delete,
        "reset": cmd_reset,
        "known-keys": cmd_known_keys,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
