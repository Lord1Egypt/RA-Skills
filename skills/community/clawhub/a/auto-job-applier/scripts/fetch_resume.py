#!/usr/bin/env python3
"""
fetch_resume.py — Fetches and pretty-prints resume data from resumex.dev API.

Usage:
    python3 fetch_resume.py                          # Full resume JSON
    python3 fetch_resume.py --field email             # Extract a single field
    python3 fetch_resume.py --json-path profile.phone # Nested field access
    python3 fetch_resume.py --save /tmp/resume.json   # Save to file

Environment variables:
    RESUMEX_API_KEY   (required) API key from resumex.dev → Dashboard → Resumex API

Output:
    Prints JSON resume data to stdout. Exits with code 1 on failure.
"""

import argparse
import os
import re
import sys
import json
from datetime import datetime

# Import shared HTTP client (handles retries, backoff, error classification)
from http_client import (
    create_session,
    get_api_key,
    ResumeXAPIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)

RESUME_ENDPOINT = "/api/v1/agent"

# ── Quick field aliases for --field flag ──────────────────────────────────────
FIELD_ALIASES = {
    "name": "profile.fullName",
    "fullname": "profile.fullName",
    "full_name": "profile.fullName",
    "first_name": "profile.fullName",  # will be split later
    "last_name": "profile.fullName",   # will be split later
    "email": "profile.email",
    "phone": "profile.phone",
    "location": "profile.location",
    "summary": "profile.summary",
    "linkedin": "profile.linkedin",
    "github": "profile.github",
    "website": "profile.website",
    "skills": "skills",
    "experience": "experience",
    "education": "education",
    "projects": "projects",
    "achievements": "achievements",
    "current_company": "experience[0].company",
    "current_role": "experience[0].role",
    "current_title": "experience[0].role",
}


def fetch_resume(api_key: str) -> dict:
    """
    Fetch resume data from the ResumeX API.

    Uses the shared HTTP client which automatically handles:
    - Retry with exponential backoff on 429/5xx/network errors
    - Retry-After header support for rate limits
    - Structured error messages for auth, 404, etc.

    Args:
        api_key: ResumeX API key

    Returns:
        Parsed JSON response from the API
    """
    with create_session(api_key) as session:
        try:
            return session.api_get(RESUME_ENDPOINT)
        except AuthenticationError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        except NotFoundError:
            print(
                "ERROR: 404 Not Found. Make sure your resume is set up at resumex.dev.",
                file=sys.stderr,
            )
            sys.exit(1)
        except RateLimitError as e:
            print(
                f"ERROR: {e}\n"
                f"Rate limit exceeded after retries. Please wait and try again.",
                file=sys.stderr,
            )
            sys.exit(1)
        except ResumeXAPIError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)


def summarize_profile(resume: dict) -> str:
    """Return a plain-text job-match profile summary from resume data."""
    # Support both old format (basics.name) and new format (profile.fullName)
    profile = resume.get("profile", resume.get("basics", {}))
    skills_data = resume.get("skills", [])
    experience = resume.get("experience", [])

    name = profile.get("fullName", profile.get("name", "Unknown"))
    location = profile.get("location", "Not specified")

    # Flatten skills (handle both flat list and categorized format)
    flat_skills = []
    if isinstance(skills_data, list):
        for item in skills_data:
            if isinstance(item, dict) and "skills" in item:
                flat_skills.extend(item["skills"])
            elif isinstance(item, str):
                flat_skills.append(item)

    # Calculate years of experience
    years = 0
    if experience:
        try:
            dates = [e.get("startDate", "") for e in experience if e.get("startDate")]
            year_nums = []
            for d in dates:
                match = re.search(r'(\d{4})', d)
                if match:
                    year_nums.append(int(match.group(1)))
            if year_nums:
                years = datetime.now().year - min(year_nums)
        except (ValueError, KeyError):
            pass

    seniority = "Entry-level"
    if years >= 7:
        seniority = "Senior"
    elif years >= 3:
        seniority = "Mid-level"
    elif years >= 1:
        seniority = "Junior"

    # Get most recent title
    latest_title = ""
    if experience:
        latest_title = experience[0].get("role", experience[0].get("title", ""))

    summary = f"""
=== Job Match Profile for {name} ===
Location    : {location}
Latest Role : {latest_title}
Experience  : {years} years ({seniority})
Top Skills  : {", ".join(flat_skills[:8]) if flat_skills else "None listed"}
"""
    return summary.strip()


def resolve_json_path(data: dict, path: str):
    """Resolve a dotted JSON path with array index support."""
    parts = re.split(r'\.|(\d+)', path.replace("[", ".").replace("]", ""))
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


def extract_active_resume(data: dict) -> dict:
    """Extract the active resume data from the API response."""
    # Full workspace format: {success, data: {activeResumeId, resumes: [...]}}
    if isinstance(data, dict) and data.get("success") and "data" in data:
        workspace = data["data"]
        active_id = workspace.get("activeResumeId")
        for r in workspace.get("resumes", []):
            if r.get("id") == active_id:
                return r.get("data", {})
        if workspace.get("resumes"):
            return workspace["resumes"][0].get("data", {})
    # Already resume data
    if "profile" in data or "basics" in data:
        return data
    # Wrapped: {resume: {...}}
    if "resume" in data:
        return data["resume"]
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch resume data from resumex.dev API"
    )
    parser.add_argument(
        "--field", "-f",
        help="Extract a specific field by alias (e.g., email, phone, name, current_company)"
    )
    parser.add_argument(
        "--json-path", "-p",
        help="Extract a value by JSON path (e.g., profile.email, experience[0].company)"
    )
    parser.add_argument(
        "--save", "-s",
        help="Save the full resume JSON to a file (for use with other scripts)"
    )
    args = parser.parse_args()

    api_key = get_api_key()
    print("Fetching resume from resumex.dev...", file=sys.stderr)
    data = fetch_resume(api_key)
    resume = extract_active_resume(data)

    # --save: write full resume to file
    if args.save:
        with open(args.save, "w") as f:
            json.dump(resume, f, indent=2)
        print(f"Resume saved to {args.save}", file=sys.stderr)

    # --field: extract by alias
    if args.field:
        alias = args.field.lower().strip()
        json_path = FIELD_ALIASES.get(alias)
        if not json_path:
            print(f"ERROR: Unknown field alias '{alias}'.", file=sys.stderr)
            print(f"Available aliases: {', '.join(sorted(FIELD_ALIASES.keys()))}", file=sys.stderr)
            sys.exit(1)
        value = resolve_json_path(resume, json_path)
        if alias == "first_name" and isinstance(value, str):
            value = value.split()[0] if value.split() else value
        elif alias == "last_name" and isinstance(value, str):
            parts = value.split()
            value = parts[-1] if len(parts) > 1 else ""
        if value is not None:
            if isinstance(value, (dict, list)):
                print(json.dumps(value, indent=2))
            else:
                print(value)
        else:
            print(f"Field '{alias}' not found in resume.", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    # --json-path: extract by path
    if args.json_path:
        value = resolve_json_path(resume, args.json_path)
        if value is not None:
            if isinstance(value, (dict, list)):
                print(json.dumps(value, indent=2))
            else:
                print(value)
        else:
            print(f"Path '{args.json_path}' not found in resume.", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    # Default: print full JSON
    print(json.dumps(resume, indent=2))

    # Also print human-readable summary to stderr
    print("\n" + summarize_profile(resume), file=sys.stderr)
