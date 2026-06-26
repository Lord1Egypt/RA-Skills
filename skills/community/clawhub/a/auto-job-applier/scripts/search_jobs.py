#!/usr/bin/env python3
"""
search_jobs.py — Constructs job search queries and parses results into structured JSON.

Part of the Auto Job Applier OpenClaw Skill. This script helps the agent build
optimized search queries from a job-match profile and structure raw search results
into a consistent format for scoring.

Usage:
    # Generate search queries from a profile
    python3 search_jobs.py generate-queries \
        --roles "Software Engineer,Backend Developer" \
        --skills "Python,Django,React,PostgreSQL" \
        --location "Pune, India" \
        --seniority "mid" \
        --job-type "full-time"

    # Parse a raw job posting into structured JSON
    python3 search_jobs.py parse-job \
        --url "https://example.com/job/123" \
        --title "Software Engineer" \
        --company "Acme Corp" \
        --raw-text "We are looking for a Software Engineer..."

    # Score a job against a profile
    python3 search_jobs.py score \
        --profile '{"roles":["SWE"],"skills":["Python"],...}' \
        --job '{"title":"SWE","required_skills":["Python"],...}'

Environment variables:
    JOB_SEARCH_LOCATION   (optional) Override location
    JOB_TYPE              (optional) full-time | part-time | contract | internship
    REMOTE_ONLY           (optional) true | false
"""

import argparse
import json
import os
import sys
from datetime import datetime


# ── Job board search templates ────────────────────────────────────────────────

SEARCH_TEMPLATES = [
    # General multi-board search
    '"{role}" "{skill1}" jobs "{location}" site:linkedin.com OR site:naukri.com OR site:indeed.com',
    # Skill-focused search
    '"{role}" "{skill1}" "{skill2}" hiring {year}',
    # Remote-focused
    '"{role}" remote jobs "{skill1}" "{seniority}"',
    # India-specific startup boards
    '"{role}" "{skill1}" jobs "{location}" "apply now" site:wellfound.com OR site:internshala.com',
    # Direct career pages
    '"{role}" "{skill1}" "{skill2}" careers "apply" "{location}" {year}',
]

SENIORITY_MAP = {
    0: "entry-level",
    1: "junior",
    2: "junior",
    3: "mid-level",
    4: "mid-level",
    5: "mid-level",
    6: "mid-level",
    7: "senior",
    8: "senior",
    9: "senior",
    10: "lead",
}

APPLICATION_METHODS = {
    "linkedin.com": "easy-apply",
    "naukri.com": "form",
    "indeed.com": "form",
    "wellfound.com": "form",
    "internshala.com": "form",
    "glassdoor.com": "redirect",
    "angel.co": "form",
    "remoteok.com": "redirect",
}


def generate_queries(roles: list, skills: list, location: str,
                     seniority: str, job_type: str, remote: bool) -> list:
    """Generate 3-5 search queries from a job-match profile."""
    queries = []
    year = datetime.now().year

    # Override from env
    location = os.environ.get("JOB_SEARCH_LOCATION", location) or "India"
    job_type = os.environ.get("JOB_TYPE", job_type) or "full-time"
    remote = os.environ.get("REMOTE_ONLY", str(remote)).lower() == "true"

    skill1 = skills[0] if skills else ""
    skill2 = skills[1] if len(skills) > 1 else skills[0] if skills else ""

    for role in roles[:2]:  # Use top 2 roles
        for template in SEARCH_TEMPLATES:
            query = template.format(
                role=role,
                skill1=skill1,
                skill2=skill2,
                location=location if not remote else "remote",
                seniority=seniority,
                year=year,
                job_type=job_type,
            )
            queries.append(query)

    # Deduplicate and limit
    seen = set()
    unique = []
    for q in queries:
        if q not in seen:
            seen.add(q)
            unique.append(q)

    return unique[:8]  # Cap at 8 queries


def parse_job(url: str, title: str, company: str, location: str = "",
              raw_text: str = "", salary: str = "") -> dict:
    """Parse raw job data into a structured posting dict."""
    # Detect application method from URL
    method = "form"
    for domain, m in APPLICATION_METHODS.items():
        if domain in url.lower():
            method = m
            break

    # Detect if remote
    is_remote = any(word in (location + " " + title + " " + raw_text).lower()
                    for word in ["remote", "work from home", "wfh", "anywhere"])

    # Extract required skills from raw text (simple keyword match)
    common_skills = [
        "python", "javascript", "typescript", "react", "node.js", "nodejs",
        "django", "flask", "fastapi", "sql", "postgresql", "mongodb",
        "docker", "kubernetes", "aws", "gcp", "azure", "git", "ci/cd",
        "java", "c++", "go", "rust", "ruby", "php", "swift", "kotlin",
        "html", "css", "tailwind", "next.js", "vue", "angular", "svelte",
        "redis", "kafka", "rabbitmq", "graphql", "rest", "api",
        "machine learning", "deep learning", "nlp", "data science",
        "tensorflow", "pytorch", "pandas", "numpy", "spark",
    ]
    text_lower = raw_text.lower()
    found_skills = [s for s in common_skills if s in text_lower]

    # Extract experience requirements
    exp_required = ""
    import re
    exp_match = re.search(r'(\d+)\s*[-–+]\s*(\d+)\s*years?', text_lower)
    if exp_match:
        exp_required = f"{exp_match.group(1)}-{exp_match.group(2)} years"
    else:
        exp_match = re.search(r'(\d+)\+?\s*years?', text_lower)
        if exp_match:
            exp_required = f"{exp_match.group(1)}+ years"

    return {
        "title": title.strip(),
        "company": company.strip(),
        "location": location.strip() or ("Remote" if is_remote else "Not specified"),
        "url": url.strip(),
        "required_skills": list(set(found_skills)),
        "experience_required": exp_required,
        "salary_range": salary.strip(),
        "application_method": method,
        "is_remote": is_remote,
        "raw_description": raw_text[:2000],  # Cap for context size
    }


def score_job(profile: dict, job: dict) -> int:
    """Score a job 0-100 against a candidate profile."""
    score = 0

    # ── Skill overlap (max 40) ────────────────────────────────────────────────
    profile_skills = set(s.lower() for s in profile.get("skills", []))
    job_skills = set(s.lower() for s in job.get("required_skills", []))
    if job_skills:
        overlap = len(profile_skills & job_skills)
        score += int((overlap / len(job_skills)) * 40)
    else:
        score += 20  # No skills listed = neutral

    # ── Role title match (max 20) ─────────────────────────────────────────────
    job_title = job.get("title", "").lower()
    profile_roles = [r.lower() for r in profile.get("roles", [])]

    if any(role in job_title or job_title in role for role in profile_roles):
        score += 20  # Exact match
    elif any(
        any(word in job_title for word in role.split())
        for role in profile_roles
    ):
        score += 10  # Adjacent match
    # else: 0

    # ── Seniority match (max 15) ──────────────────────────────────────────────
    profile_seniority = profile.get("seniority", "mid-level").lower()
    job_exp = job.get("experience_required", "").lower()

    if profile_seniority in job_exp or not job_exp:
        score += 15
    elif "senior" in job_exp and profile_seniority in ("mid-level", "senior"):
        score += 8
    elif "junior" in job_exp and profile_seniority in ("junior", "entry-level"):
        score += 12
    elif "entry" in job_exp:
        score += 8

    # ── Location match (max 15) ───────────────────────────────────────────────
    profile_location = profile.get("location", "").lower()
    job_location = job.get("location", "").lower()
    is_remote = job.get("is_remote", False)

    if is_remote:
        score += 12  # Remote is mostly a match
    elif profile_location and any(
        word in job_location for word in profile_location.split(",")
    ):
        score += 15  # Location match
    elif not job_location or job_location == "not specified":
        score += 8  # Unknown = neutral

    # ── Industry match (max 10) ───────────────────────────────────────────────
    # Simple heuristic: check if any profile company/industry keywords appear
    profile_industries = profile.get("industries", [])
    job_desc = job.get("raw_description", "").lower()
    if profile_industries:
        if any(ind.lower() in job_desc for ind in profile_industries):
            score += 10
        else:
            score += 5  # Neutral

    return min(score, 100)


def classify_apply_method(job: dict) -> str:
    """Classify how the agent should apply to this job."""
    method = job.get("application_method", "form")
    url = job.get("url", "").lower()

    if "linkedin.com" in url:
        return "manual-linkedin"  # 🔗 Manual (LinkedIn)
    elif method == "easy-apply":
        return "manual-linkedin"
    elif method == "email" or "mailto:" in url:
        return "email"  # 📧 Email apply
    elif method == "redirect":
        return "manual-redirect"  # 🔗 Manual (redirect)
    else:
        return "auto-apply"  # 🤖 Auto-apply


# ── CLI ───────────────────────────────────────────────────────────────────────

def cmd_generate_queries(args):
    roles = [r.strip() for r in args.roles.split(",") if r.strip()]
    skills = [s.strip() for s in args.skills.split(",") if s.strip()]
    queries = generate_queries(
        roles=roles,
        skills=skills,
        location=args.location or "",
        seniority=args.seniority or "mid-level",
        job_type=args.job_type or "full-time",
        remote=args.remote,
    )
    print(json.dumps(queries, indent=2))


def cmd_parse_job(args):
    result = parse_job(
        url=args.url,
        title=args.title,
        company=args.company,
        location=args.location or "",
        raw_text=args.raw_text or "",
        salary=args.salary or "",
    )
    result["apply_method"] = classify_apply_method(result)
    print(json.dumps(result, indent=2))


def cmd_score(args):
    try:
        profile = json.loads(args.profile)
        job = json.loads(args.job)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    result = {
        "score": score_job(profile, job),
        "apply_method": classify_apply_method(job),
    }
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Job search query generator and result parser for Auto Job Applier"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # generate-queries
    gen = subparsers.add_parser("generate-queries", help="Generate web search queries")
    gen.add_argument("--roles", required=True, help="Comma-separated target roles")
    gen.add_argument("--skills", required=True, help="Comma-separated key skills")
    gen.add_argument("--location", default="", help="Target location")
    gen.add_argument("--seniority", default="mid-level", help="Seniority level")
    gen.add_argument("--job-type", default="full-time", help="Job type")
    gen.add_argument("--remote", action="store_true", help="Remote only")

    # parse-job
    pj = subparsers.add_parser("parse-job", help="Parse raw job data into structured JSON")
    pj.add_argument("--url", required=True, help="Job posting URL")
    pj.add_argument("--title", required=True, help="Job title")
    pj.add_argument("--company", required=True, help="Company name")
    pj.add_argument("--location", default="", help="Job location")
    pj.add_argument("--raw-text", default="", help="Raw job description text")
    pj.add_argument("--salary", default="", help="Salary range")

    # score
    sc = subparsers.add_parser("score", help="Score a job against a profile")
    sc.add_argument("--profile", required=True, help="JSON profile string")
    sc.add_argument("--job", required=True, help="JSON job string")

    args = parser.parse_args()

    if args.command == "generate-queries":
        cmd_generate_queries(args)
    elif args.command == "parse-job":
        cmd_parse_job(args)
    elif args.command == "score":
        cmd_score(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
