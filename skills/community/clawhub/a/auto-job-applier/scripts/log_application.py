#!/usr/bin/env python3
"""
log_application.py — Logs a job application to the resumex.dev job tracker.

Usage:
    python3 log_application.py \\
        --company "Acme Corp" \\
        --role "Software Engineer" \\
        --url "https://linkedin.com/jobs/view/12345" \\
        --status "applied" \\
        [--method "auto-applied"] \\
        [--cover_letter "path/to/cover.txt"] \\
        [--score 87] \\
        [--notes "Extra notes here"] \\
        [--dry-run]

Environment variables:
    RESUMEX_API_KEY   (required)

Valid status values:
    wishlist | applied | interview | offer | rejected

Valid method values:
    auto-applied | manual | easy-apply | email
"""

import os
import sys
import json
import argparse
from datetime import date

# Import shared HTTP client (handles retries, backoff, error classification)
from http_client import (
    create_session,
    get_api_key,
    ResumeXAPIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)

# Endpoints to try in order — falls back if the first returns 404
LOG_ENDPOINTS = [
    "/api/v1/agent/jobs",
    "/api/v1/agent/logs",
]

VALID_STATUSES = {"wishlist", "applied", "interview", "offer", "rejected"}
VALID_METHODS = {"auto-applied", "manual", "easy-apply", "email"}


def log_application(api_key: str, payload: dict) -> dict:
    """
    Log a job application to the ResumeX job tracker.

    Tries multiple endpoints in order, falling back on 404.
    Uses the shared HTTP client for automatic retry with backoff.

    Args:
        api_key: ResumeX API key
        payload: Application data to log

    Returns:
        Parsed JSON response from the API
    """
    with create_session(api_key) as session:
        try:
            return session.api_post_with_fallback(LOG_ENDPOINTS, payload)
        except AuthenticationError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        except NotFoundError:
            print(
                "ERROR: Job logging endpoint not found (404).\n"
                f"Tried endpoints: {', '.join(LOG_ENDPOINTS)}\n"
                "The ResumeX API may have changed. Check https://resumex.dev/api-docs\n"
                "for the current job logging endpoint.\n\n"
                "TIP: Use --dry-run to print the payload without calling the API.",
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


def main():
    parser = argparse.ArgumentParser(description="Log a job application to resumex.dev")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--role", required=True, help="Job title / position")
    parser.add_argument("--url", required=True, help="Job posting URL")
    parser.add_argument(
        "--status",
        default="applied",
        choices=list(VALID_STATUSES),
        help="Application status (default: applied)",
    )
    parser.add_argument("--cover_letter", help="Path to cover letter text file (optional)")
    parser.add_argument("--score", type=int, help="Match score 0-100 (optional)")
    parser.add_argument(
        "--method",
        default="manual",
        choices=list(VALID_METHODS),
        help="Application method (default: manual)",
    )
    parser.add_argument("--notes", default="", help="Extra notes (optional)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the payload JSON without calling the API (for testing)",
    )
    args = parser.parse_args()

    # Build notes string
    notes_parts = []
    if args.score is not None:
        notes_parts.append(f"Match score: {args.score}/100.")
    notes_parts.append(f"Method: {args.method}.")
    if args.notes:
        notes_parts.append(args.notes)
    notes_parts.append("Applied via Auto Job Applier skill.")
    notes = " ".join(notes_parts)

    # Optionally read cover letter
    cover_letter_text = ""
    if args.cover_letter:
        try:
            with open(args.cover_letter, "r") as f:
                cover_letter_text = f.read().strip()
        except FileNotFoundError:
            print(f"WARNING: Cover letter file not found: {args.cover_letter}", file=sys.stderr)

    payload = {
        "company": args.company,
        "position": args.role,
        "url": args.url,
        "status": args.status,
        "appliedDate": date.today().isoformat(),
        "notes": notes,
    }
    if cover_letter_text:
        payload["coverLetter"] = cover_letter_text

    # Dry-run mode: print payload and exit
    if args.dry_run:
        print("🔍 DRY RUN — Payload that would be sent:", file=sys.stderr)
        print(json.dumps(payload, indent=2))
        print(
            f"\nEndpoints that would be tried: {', '.join(LOG_ENDPOINTS)}",
            file=sys.stderr,
        )
        sys.exit(0)

    api_key = get_api_key()
    print(f"Logging application: {args.role} at {args.company}...", file=sys.stderr)
    result = log_application(api_key, payload)

    print(json.dumps(result, indent=2))
    print(f"\n✅ Logged: {args.role} @ {args.company} — Status: {args.status}", file=sys.stderr)


if __name__ == "__main__":
    main()
