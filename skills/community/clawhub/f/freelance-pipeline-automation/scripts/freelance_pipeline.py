#!/usr/bin/env python3
"""
Freelance Pipeline Automation Script
Automates freelance client discovery, lead scoring, proposal drafting,
and pipeline tracking for independent professionals and AI agents.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

PIPELINE_FILE = os.environ.get("FREELANCE_PIPELINE", "pipeline.json")
PROFILE_FILE = os.environ.get("FREELANCE_PROFILE", "profile.json")


def load_json(path: str, default: dict) -> dict:
    """Load JSON file or return default."""
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def save_json(path: str, data: dict) -> None:
    """Save data to JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def generate_proposal(job: dict, profile: dict) -> str:
    """Generate personalized proposal for a job posting."""
    title = job.get("title", "Untitled")
    client = job.get("client", "Client")
    budget = job.get("budget", "TBD")
    skills = job.get("skills", [])

    # Match relevant skills from profile
    matched = [s for s in skills if s.lower() in [ps.lower() for ps in profile.get("skills", [])]]
    unmatched = [s for s in skills if s.lower() not in [ps.lower() for ps in profile.get("skills", [])]]

    proposal = f"""# Proposal: {title}

## Client
- Name: {client}
- Budget: {budget}

## Match Analysis
- Strong Matches ({len(matched)}): {', '.join(matched) if matched else 'None'}
- Growth Areas ({len(unmatched)}): {', '.join(unmatched) if unmatched else 'None'}

## Proposed Solution
Based on your expertise in {', '.join(profile.get('skills', [])[:3])}, I can deliver
high-quality work that meets your requirements. Here's my approach:

1. **Understanding**: I'll start by clarifying the key goals and success criteria
2. **Execution**: Deliver milestones with regular updates
3. **Quality**: Thorough testing and revisions included

## Pricing
- Hourly Rate: ${profile.get('hourly_rate', 50)}/hour
- Estimated Timeline: {job.get('timeline', 'To be discussed')}

## Why Me
- {profile.get('experience', 'Experienced professional')}
- Available to start immediately
- Committed to exceeding expectations

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    return proposal


def add_lead(job_data: dict, score: int, source: str) -> None:
    """Add a new lead to the pipeline."""
    pipeline = load_json(PIPELINE_FILE, {"leads": [], "stats": {}})

    lead = {
        "id": len(pipeline["leads"]) + 1,
        "added": datetime.now().isoformat(),
        "status": "new",
        "score": score,
        "source": source,
        "proposal_sent": False,
        **job_data,
    }

    pipeline["leads"].append(lead)
    save_json(PIPELINE_FILE, pipeline)
    print(f"Added lead: {job_data.get('title', 'Unknown')} (Score: {score})")


def update_lead_status(lead_id: int, new_status: str) -> None:
    """Update the status of a lead."""
    pipeline = load_json(PIPELINE_FILE, {"leads": []})

    for lead in pipeline["leads"]:
        if lead["id"] == lead_id:
            old_status = lead.get("status")
            lead["status"] = new_status
            if new_status == "proposal_sent":
                lead["proposal_sent"] = True
                lead["proposal_date"] = datetime.now().isoformat()
            save_json(PIPELINE_FILE, pipeline)
            print(f"Lead #{lead_id}: {old_status} -> {new_status}")
            return

    print(f"Lead #{lead_id} not found")


def get_digest() -> None:
    """Generate morning digest of qualified leads."""
    pipeline = load_json(PIPELINE_FILE, {"leads": []})

    new_leads = [l for l in pipeline["leads"] if l.get("status") == "new"]
    qualified = [l for l in new_leads if l.get("score", 0) >= 70]

    print("\n" + "=" * 60)
    print("  FREELANCE PIPELINE DIGEST")
    print(f"  {datetime.now().strftime('%Y-%m-%d %A')}")
    print("=" * 60)
    print(f"\nTotal Leads: {len(pipeline['leads'])}")
    print(f"New: {len(new_leads)} | Qualified: {len(qualified)}\n")

    if qualified:
        print("TOP QUALIFIED LEADS:\n")
        for lead in sorted(qualified, key=lambda x: x.get("score", 0), reverse=True)[:5]:
            print(f"  [{lead.get('score')}] {lead.get('title', 'N/A')}")
            print(f"    Budget: {lead.get('budget', 'TBD')} | Source: {lead.get('source', 'N/A')}")
            print(f"    Skills: {', '.join(lead.get('skills', [])[:3])}")
            print()

    # Stats
    proposal_sent = len([l for l in pipeline["leads"] if l.get("proposal_sent")])
    print(f"Proposals Sent: {proposal_sent}")
    print()


def score_lead(title: str, budget: str, skills: list, profile: dict) -> int:
    """Score a lead based on match quality, budget, and recency."""
    score = 50  # Base

    # Budget scoring
    budget_str = str(budget).lower()
    if any(k in budget_str for k in ["500", "1000", "2000", "fixed"]):
        score += 20
    elif any(k in budget_str for k in ["50", "100", "hourly"]):
        score += 5

    # Skills match
    profile_skills = [s.lower() for s in profile.get("skills", [])]
    matched = sum(1 for s in skills if any(ps in s.lower() for ps in profile_skills))
    score += min(matched * 10, 30)

    return min(score, 100)


def main():
    profile = load_json(PROFILE_FILE, {
        "skills": ["python", "web development", "automation"],
        "hourly_rate": 75,
        "experience": "5+ years in Python and web development"
    })

    if len(sys.argv) < 2:
        print("Usage: python freelance_pipeline.py <command> [args]")
        print("Commands:")
        print("  add <title> <budget> <skills>   Add a new lead")
        print("  score <title> <budget> <skills> Score a lead without adding")
        print("  digest                            Morning digest of qualified leads")
        print("  status <id> <new_status>         Update lead status")
        print("  list                              Show all leads")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "add" and len(sys.argv) > 3:
        title = sys.argv[2]
        budget = sys.argv[3]
        skills = sys.argv[4].split(",") if len(sys.argv) > 4 else []
        score = score_lead(title, budget, skills, profile)
        add_lead({"title": title, "budget": budget, "skills": skills}, score, "manual")

    elif cmd == "score" and len(sys.argv) > 3:
        title = sys.argv[2]
        budget = sys.argv[3]
        skills = sys.argv[4].split(",") if len(sys.argv) > 4 else []
        score = score_lead(title, budget, skills, profile)
        print(f"\nLead Score: {score}/100")

    elif cmd == "digest":
        get_digest()

    elif cmd == "status" and len(sys.argv) > 3:
        update_lead_status(int(sys.argv[2]), sys.argv[3])

    elif cmd == "list":
        pipeline = load_json(PIPELINE_FILE, {"leads": []})
        for lead in pipeline["leads"]:
            status = lead.get("status", "?")
            score = lead.get("score", 0)
            print(f"  [{status:12s}] #{lead['id']:3d} | Score: {score:3d} | {lead.get('title', 'N/A')[:50]}")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()