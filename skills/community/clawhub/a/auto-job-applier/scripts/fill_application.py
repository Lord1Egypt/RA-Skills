#!/usr/bin/env python3
"""
fill_application.py — Maps job application form fields to resume data and outputs
                       browser automation instructions.

Part of the Auto Job Applier OpenClaw Skill. This script takes resume data and
a description of form fields, then produces structured JSON instructions for
the agent's browser tool to fill in each field.

Usage:
    # Generate fill instructions from resume + form fields
    python3 fill_application.py map-fields \
        --resume path/to/resume.json \
        --fields '[{"label":"First Name","type":"text","selector":"#first_name"},...]'

    # Get the value for a specific field from resume data
    python3 fill_application.py get-value \
        --resume path/to/resume.json \
        --field-label "Email Address"

    # Check which fields can be auto-filled vs need user input
    python3 fill_application.py check-coverage \
        --resume path/to/resume.json \
        --prefs path/to/user_preferences.json \
        --fields '[{"label":"First Name"},{"label":"Salary Expectation"},...]'

Environment variables:
    RESUMEX_API_KEY   (optional) If set and --resume not provided, fetches live
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── Field label → resume JSON path mapping ────────────────────────────────────

FIELD_MAPPINGS = {
    # ── Personal Info ──
    "first name": {"source": "resume", "path": "profile.fullName", "transform": "first_name"},
    "first_name": {"source": "resume", "path": "profile.fullName", "transform": "first_name"},
    "fname": {"source": "resume", "path": "profile.fullName", "transform": "first_name"},
    "last name": {"source": "resume", "path": "profile.fullName", "transform": "last_name"},
    "last_name": {"source": "resume", "path": "profile.fullName", "transform": "last_name"},
    "lname": {"source": "resume", "path": "profile.fullName", "transform": "last_name"},
    "full name": {"source": "resume", "path": "profile.fullName"},
    "name": {"source": "resume", "path": "profile.fullName"},
    "email": {"source": "resume", "path": "profile.email"},
    "email address": {"source": "resume", "path": "profile.email"},
    "e-mail": {"source": "resume", "path": "profile.email"},
    "phone": {"source": "resume", "path": "profile.phone"},
    "phone number": {"source": "resume", "path": "profile.phone"},
    "mobile": {"source": "resume", "path": "profile.phone"},
    "mobile number": {"source": "resume", "path": "profile.phone"},
    "contact number": {"source": "resume", "path": "profile.phone"},

    # ── Location ──
    "location": {"source": "resume", "path": "profile.location"},
    "city": {"source": "preferences", "key": "city", "fallback_path": "profile.location", "transform": "extract_city"},
    "state": {"source": "preferences", "key": "state"},
    "country": {"source": "preferences", "key": "country"},
    "zip code": {"source": "preferences", "key": "zip_code"},
    "postal code": {"source": "preferences", "key": "zip_code"},
    "address": {"source": "preferences", "key": "address_line1"},
    "street address": {"source": "preferences", "key": "address_line1"},
    "current location": {"source": "resume", "path": "profile.location"},

    # ── Professional Links ──
    "linkedin": {"source": "resume", "path": "profile.linkedin"},
    "linkedin url": {"source": "resume", "path": "profile.linkedin"},
    "linkedin profile": {"source": "resume", "path": "profile.linkedin"},
    "github": {"source": "resume", "path": "profile.github"},
    "github url": {"source": "resume", "path": "profile.github"},
    "website": {"source": "resume", "path": "profile.website"},
    "portfolio": {"source": "resume", "path": "profile.website"},
    "portfolio url": {"source": "resume", "path": "profile.website"},

    # ── Current Role ──
    "current company": {"source": "resume", "path": "experience[0].company"},
    "current employer": {"source": "resume", "path": "experience[0].company"},
    "current title": {"source": "resume", "path": "experience[0].role"},
    "current job title": {"source": "resume", "path": "experience[0].role"},
    "current role": {"source": "resume", "path": "experience[0].role"},
    "current position": {"source": "resume", "path": "experience[0].role"},

    # ── Experience ──
    "years of experience": {"source": "derived", "derive": "years_of_experience"},
    "total experience": {"source": "derived", "derive": "years_of_experience"},
    "work experience": {"source": "derived", "derive": "years_of_experience"},

    # ── Education ──
    "highest education": {"source": "preferences", "key": "highest_education", "fallback_path": "education[0].degree"},
    "degree": {"source": "resume", "path": "education[0].degree"},
    "university": {"source": "resume", "path": "education[0].institution"},
    "college": {"source": "resume", "path": "education[0].institution"},
    "institution": {"source": "resume", "path": "education[0].institution"},
    "graduation year": {"source": "preferences", "key": "graduation_year", "fallback_path": "education[0].endDate"},

    # ── Preferences (not in resume) ──
    "salary expectation": {"source": "preferences", "key": "salary_expectation"},
    "expected salary": {"source": "preferences", "key": "salary_expectation"},
    "salary": {"source": "preferences", "key": "salary_expectation"},
    "expected ctc": {"source": "preferences", "key": "expected_ctc"},
    "current ctc": {"source": "preferences", "key": "current_ctc"},
    "notice period": {"source": "preferences", "key": "notice_period"},
    "visa status": {"source": "preferences", "key": "visa_status"},
    "work authorization": {"source": "preferences", "key": "work_authorization"},
    "willing to relocate": {"source": "preferences", "key": "willing_to_relocate"},
    "gender": {"source": "preferences", "key": "gender"},
    "date of birth": {"source": "preferences", "key": "date_of_birth"},
    "dob": {"source": "preferences", "key": "date_of_birth"},

    # ── Cover letter ──
    "cover letter": {"source": "generated", "type": "cover_letter"},
    "additional information": {"source": "generated", "type": "cover_letter"},
    "why interested": {"source": "generated", "type": "interest_statement"},
    "why are you interested": {"source": "generated", "type": "interest_statement"},

    # ── File uploads ──
    "resume": {"source": "skip", "reason": "File upload — user must upload manually"},
    "cv": {"source": "skip", "reason": "File upload — user must upload manually"},
    "upload resume": {"source": "skip", "reason": "File upload — user must upload manually"},
    "upload cv": {"source": "skip", "reason": "File upload — user must upload manually"},
    "resume/cv": {"source": "skip", "reason": "File upload — user must upload manually"},
}


def _resolve_path(data: dict, path: str):
    """Resolve a dotted path with array indices against a data dict."""
    parts = re.split(r'\.|\[(\d+)\]', path)
    parts = [p for p in parts if p is not None and p != '']

    current = data
    for part in parts:
        if part.isdigit():
            idx = int(part)
            if isinstance(current, list) and idx < len(current):
                current = current[idx]
            else:
                return None
        elif isinstance(current, dict):
            current = current.get(part)
            if current is None:
                return None
        else:
            return None
    return current


def _apply_transform(value, transform: str) -> str:
    """Apply a named transform to a value."""
    if value is None:
        return None

    s = str(value).strip()
    if not s:
        return None

    if transform == "first_name":
        parts = s.split()
        return parts[0] if parts else s
    elif transform == "last_name":
        parts = s.split()
        return parts[-1] if len(parts) > 1 else ""
    elif transform == "extract_city":
        # "Pune, India" → "Pune"
        return s.split(",")[0].strip()
    return s


def _derive_value(resume: dict, derive_key: str):
    """Calculate derived values from resume data."""
    if derive_key == "years_of_experience":
        experience = resume.get("experience", [])
        if not experience:
            return "0"
        from datetime import datetime
        try:
            dates = [e.get("startDate", "") for e in experience if e.get("startDate")]
            if dates:
                # Extract year from various formats
                years = []
                for d in dates:
                    match = re.search(r'(\d{4})', d)
                    if match:
                        years.append(int(match.group(1)))
                if years:
                    earliest = min(years)
                    return str(datetime.now().year - earliest)
        except (ValueError, TypeError):
            pass
        return "0"
    return None


def resolve_field(label: str, resume: dict, preferences: dict,
                  cover_letter: str = "") -> dict:
    """
    Resolve a form field label to a value from resume, preferences, or derived data.

    Returns:
        {
            "label": str,
            "value": str or None,
            "source": "resume" | "preferences" | "derived" | "generated" | "skip" | "ask_user",
            "reason": str (for skip/ask_user)
        }
    """
    label_lower = label.lower().strip()

    # Try exact match first
    mapping = FIELD_MAPPINGS.get(label_lower)

    # Try partial match
    if not mapping:
        for key, m in FIELD_MAPPINGS.items():
            if key in label_lower or label_lower in key:
                mapping = m
                break

    if not mapping:
        return {
            "label": label,
            "value": None,
            "source": "ask_user",
            "reason": f"Unknown field '{label}'. Ask the user what to enter.",
        }

    source = mapping["source"]

    if source == "skip":
        return {
            "label": label,
            "value": None,
            "source": "skip",
            "reason": mapping.get("reason", "Skipped"),
        }

    if source == "resume":
        path = mapping.get("path", "")
        value = _resolve_path(resume, path)
        transform = mapping.get("transform")
        if transform and value:
            value = _apply_transform(value, transform)
        if value:
            return {"label": label, "value": str(value), "source": "resume"}
        # Fallback to preferences
        fallback_key = mapping.get("fallback_key")
        if fallback_key and fallback_key in preferences:
            return {"label": label, "value": str(preferences[fallback_key]), "source": "preferences"}
        return {
            "label": label,
            "value": None,
            "source": "ask_user",
            "reason": f"'{label}' not found in resume at path '{path}'. Ask the user.",
        }

    if source == "preferences":
        key = mapping.get("key", "")
        value = preferences.get(key)
        if value is not None:
            return {"label": label, "value": str(value), "source": "preferences"}
        # Try fallback path in resume
        fallback_path = mapping.get("fallback_path")
        if fallback_path:
            value = _resolve_path(resume, fallback_path)
            transform = mapping.get("transform")
            if transform and value:
                value = _apply_transform(value, transform)
            if value:
                return {"label": label, "value": str(value), "source": "resume"}
        return {
            "label": label,
            "value": None,
            "source": "ask_user",
            "reason": f"'{key}' not found in preferences. Ask the user and save with: "
                      f"manage_preferences.py set {key} \"<answer>\"",
        }

    if source == "derived":
        derive_key = mapping.get("derive", "")
        value = _derive_value(resume, derive_key)
        if value:
            return {"label": label, "value": str(value), "source": "derived"}
        return {
            "label": label,
            "value": None,
            "source": "ask_user",
            "reason": f"Could not derive '{derive_key}' from resume. Ask the user.",
        }

    if source == "generated":
        gen_type = mapping.get("type", "")
        if gen_type == "cover_letter" and cover_letter:
            return {"label": label, "value": cover_letter, "source": "generated"}
        return {
            "label": label,
            "value": None,
            "source": "ask_user",
            "reason": f"Generate {gen_type} using draft_cover_letter.py or LLM.",
        }

    return {"label": label, "value": None, "source": "ask_user", "reason": "Unknown source"}


def load_resume_file(path: str) -> dict:
    """Load a resume JSON file and extract the active resume data."""
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Could not load resume file: {e}", file=sys.stderr)
        sys.exit(1)

    # Handle both raw resume data and full workspace format
    if "data" in data and "resumes" in data.get("data", {}):
        workspace = data["data"]
        active_id = workspace.get("activeResumeId")
        for r in workspace.get("resumes", []):
            if r.get("id") == active_id:
                return r.get("data", {})
        if workspace.get("resumes"):
            return workspace["resumes"][0].get("data", {})
    elif "profile" in data:
        return data
    elif "resume" in data:
        return data["resume"]

    return data


def load_preferences_file(path: str) -> dict:
    """Load preferences JSON file."""
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


# ── CLI Commands ──────────────────────────────────────────────────────────────

def cmd_map_fields(args):
    resume = load_resume_file(args.resume)
    prefs = load_preferences_file(args.prefs) if args.prefs else {}

    try:
        fields = json.loads(args.fields)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid --fields JSON: {e}", file=sys.stderr)
        sys.exit(1)

    results = []
    for field in fields:
        label = field.get("label", "")
        result = resolve_field(label, resume, prefs, args.cover_letter or "")
        result["selector"] = field.get("selector", "")
        result["field_type"] = field.get("type", "text")
        result["required"] = field.get("required", False)
        results.append(result)

    # Summary
    auto_fill = [r for r in results if r["source"] in ("resume", "preferences", "derived", "generated")]
    needs_input = [r for r in results if r["source"] == "ask_user"]
    skipped = [r for r in results if r["source"] == "skip"]

    output = {
        "fields": results,
        "summary": {
            "total": len(results),
            "auto_fillable": len(auto_fill),
            "needs_user_input": len(needs_input),
            "skipped": len(skipped),
            "needs_input_fields": [r["label"] for r in needs_input],
            "skipped_fields": [r["label"] for r in skipped],
        },
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


def cmd_get_value(args):
    resume = load_resume_file(args.resume)
    prefs = load_preferences_file(args.prefs) if args.prefs else {}
    result = resolve_field(args.field_label, resume, prefs)
    print(json.dumps(result, indent=2))


def cmd_check_coverage(args):
    resume = load_resume_file(args.resume)
    prefs = load_preferences_file(args.prefs) if args.prefs else {}

    try:
        fields = json.loads(args.fields)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid --fields JSON: {e}", file=sys.stderr)
        sys.exit(1)

    results = []
    for field in fields:
        label = field.get("label", "")
        result = resolve_field(label, resume, prefs)
        results.append({
            "label": label,
            "fillable": result["source"] in ("resume", "preferences", "derived"),
            "source": result["source"],
        })

    fillable = sum(1 for r in results if r["fillable"])
    total = len(results)
    coverage = round((fillable / total) * 100) if total > 0 else 0

    output = {
        "coverage_percent": coverage,
        "fillable": fillable,
        "total": total,
        "fields": results,
    }
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Map job application form fields to resume data"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # map-fields
    mf = subparsers.add_parser("map-fields", help="Map form fields to resume values")
    mf.add_argument("--resume", required=True, help="Path to resume JSON")
    mf.add_argument("--fields", required=True, help="JSON array of form fields")
    mf.add_argument("--prefs", help="Path to user_preferences.json")
    mf.add_argument("--cover-letter", help="Cover letter text to use for cover letter fields")

    # get-value
    gv = subparsers.add_parser("get-value", help="Get value for a specific field label")
    gv.add_argument("--resume", required=True, help="Path to resume JSON")
    gv.add_argument("--field-label", required=True, help="Form field label")
    gv.add_argument("--prefs", help="Path to user_preferences.json")

    # check-coverage
    cc = subparsers.add_parser("check-coverage", help="Check form field coverage")
    cc.add_argument("--resume", required=True, help="Path to resume JSON")
    cc.add_argument("--fields", required=True, help="JSON array of form fields")
    cc.add_argument("--prefs", help="Path to user_preferences.json")

    args = parser.parse_args()

    commands = {
        "map-fields": cmd_map_fields,
        "get-value": cmd_get_value,
        "check-coverage": cmd_check_coverage,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
