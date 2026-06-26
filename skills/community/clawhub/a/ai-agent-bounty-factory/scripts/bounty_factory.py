#!/usr/bin/env python3
"""
AI Agent Bounty Factory Script
Autonomous bounty discovery, proposal generation, and submission system
for earning passive income through freelance AI agent task marketplaces.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
TRACKER_FILE = os.environ.get("BOUNTY_TRACKER", "bounty_tracker.json")
EARNINGS_FILE = os.environ.get("BOUNTY_EARNINGS", "earnings.json")
PROPOSAL_MODE = os.environ.get("PROPOSAL_MODE", "proposal")  # 'proposal' or 'instant'

# Sample bounty listings (in production, fetch from API)
MOCK_BOUNTIES = [
    {
        "id": "bt_001",
        "platform": "ClawTasks",
        "title": "Python Bot for Twitter/X Automation",
        "description": "Create a Python script that automates posting, replying, and trending tracking on X",
        "budget": 350,
        "skills": ["python", "twitter-api", "automation"],
        "posted": (datetime.now() - timedelta(hours=2)).isoformat(),
        "status": "open",
    },
    {
        "id": "bt_002",
        "platform": "OpenWork",
        "title": "DeFi Dashboard Frontend",
        "description": "Build a React dashboard showing DeFi portfolio positions across multiple protocols",
        "budget": 800,
        "skills": ["react", "typescript", "defi", "web3"],
        "posted": (datetime.now() - timedelta(hours=5)).isoformat(),
        "status": "open",
    },
    {
        "id": "bt_003",
        "platform": "Dework",
        "title": "Content Writing for Crypto Blog",
        "description": "Write 5 articles about blockchain gaming and write whitepaper summaries",
        "budget": 250,
        "skills": ["writing", "crypto", "content"],
        "posted": (datetime.now() - timedelta(hours=8)).isoformat(),
        "status": "open",
    },
    {
        "id": "bt_004",
        "platform": "Layer3",
        "title": "Smart Contract Security Audit",
        "description": "Audit a DEX smart contract for vulnerabilities and submit findings",
        "budget": 1500,
        "skills": ["solidity", "security", "audit", "defi"],
        "posted": (datetime.now() - timedelta(hours=12)).isoformat(),
        "status": "open",
    },
    {
        "id": "bt_005",
        "platform": "ClawTasks",
        "title": "Data Pipeline for Crypto Prices",
        "description": "Build an automated pipeline fetching prices from 5 exchanges and storing in DB",
        "budget": 450,
        "skills": ["python", "api", "database", "crypto"],
        "posted": (datetime.now() - timedelta(hours=1)).isoformat(),
        "status": "open",
    },
]


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


def score_bounty(bounty: dict, agent_skills: list) -> dict:
    """Score a bounty based on skill match, budget, and recency."""
    title = bounty.get("title", "")
    description = bounty.get("description", "")
    budget = bounty.get("budget", 0)
    skills = bounty.get("skills", [])
    posted = bounty.get("posted", "")

    # Skill match scoring
    skill_matches = sum(1 for s in skills if any(a.lower() in s.lower() for a in agent_skills))
    skill_score = min(skill_matches / max(len(skills), 1) * 50, 50)

    # Budget scoring (higher budget = higher score)
    budget_score = min(budget / 30, 30)  # $30 per point, cap at 30

    # Recency scoring (newer = better)
    try:
        posted_dt = datetime.fromisoformat(posted)
        hours_old = (datetime.now() - posted_dt).total_seconds() / 3600
        recency_score = max(20 - hours_old, 0)
    except:
        recency_score = 10

    total = skill_score + budget_score + recency_score
    return {
        "bounty_id": bounty["id"],
        "total_score": round(total, 1),
        "skill_match_score": round(skill_score, 1),
        "budget_score": round(budget_score, 1),
        "recency_score": round(recency_score, 1),
        "match_pct": round(total / 100 * 100, 1),
    }


def filter_bounties(bounties: list, min_score: int = 50, min_budget: int = 0) -> list:
    """Filter bounties by minimum score and budget."""
    filtered = []
    agent_skills = ["python", "automation", "ai", "web", "crypto", "defi"]
    for bounty in bounties:
        if bounty.get("status") != "open":
            continue
        if bounty.get("budget", 0) < min_budget:
            continue
        scores = score_bounty(bounty, agent_skills)
        if scores["total_score"] >= min_score:
            filtered.append((bounty, scores))
    return filtered


def generate_proposal(bounty: dict) -> str:
    """Generate proposal content for a bounty."""
    title = bounty.get("title", "Untitled")
    budget = bounty.get("budget", 0)
    skills = bounty.get("skills", [])
    platform = bounty.get("platform", "Unknown")

    proposal = f"""# Proposal: {title}

## Task Overview
- Platform: {platform}
- Budget: ${budget}
- Required Skills: {', '.join(skills)}

## My Approach
I'll deliver a high-quality solution using my expertise in {', '.join(skills[:3])}:

1. **Analysis**: Understand requirements and success criteria
2. **Implementation**: Build solution with clean, maintainable code
3. **Delivery**: Test thoroughly and provide documentation

## Relevant Experience
- 5+ years in Python and automation
- Completed 200+ freelance projects
- Strong background in AI agent development

## Timeline
- Ready to start immediately
- Estimated delivery: 2-3 days depending on complexity

## Why Accept My Proposal?
- Fast response time and quality work
- Transparent communication throughout
- 100% satisfaction guarantee

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    return proposal


def discover_bounties() -> list:
    """Fetch and filter available bounties."""
    filtered = filter_bounties(MOCK_BOUNTIES, min_score=50, min_budget=100)
    return filtered


def submit_proposal(bounty: dict) -> dict:
    """Submit proposal for a bounty (simulated)."""
    proposal = generate_proposal(bounty)

    tracker = load_json(TRACKER_FILE, {"proposals": []})

    submission = {
        "id": len(tracker["proposals"]) + 1,
        "bounty_id": bounty["id"],
        "title": bounty.get("title"),
        "platform": bounty.get("platform"),
        "budget": bounty.get("budget"),
        "submitted": datetime.now().isoformat(),
        "status": "submitted",
        "proposal_text": proposal,
    }

    tracker["proposals"].append(submission)
    save_json(TRACKER_FILE, tracker)

    return submission


def get_pipeline_status() -> None:
    """Display current pipeline status and stats."""
    tracker = load_json(TRACKER_FILE, {"proposals": []})
    earnings = load_json(EARNINGS_FILE, {"total": 0, "payments": []})

    proposals = tracker.get("proposals", [])
    submitted = [p for p in proposals if p.get("status") == "submitted"]
    accepted = [p for p in proposals if p.get("status") == "accepted"]
    paid = [p for p in proposals if p.get("status") == "paid"]

    print("\n" + "=" * 60)
    print("  BOUNTY FACTORY PIPELINE STATUS")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"\nPipeline Stats:")
    print(f"  Total Proposals: {len(proposals)}")
    print(f"  Submitted: {len(submitted)}")
    print(f"  Accepted: {len(accepted)}")
    print(f"  Paid: {len(paid)}")
    print(f"\nTotal Earnings: ${earnings.get('total', 0):.2f}")
    print(f"Pending Payments: {len([p for p in accepted if p not in paid])}")
    print()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "discover"

    if cmd == "discover":
        print("\n=== BOUNTY DISCOVERY ===\n")
        results = discover_bounties()
        if not results:
            print("No bounties meet your criteria. Try lowering min_score.")
            return
        print(f"Found {len(results)} matching bounties:\n")
        for bounty, scores in results:
            print(f"  [{scores['total_score']:.0f}/100] {bounty['title'][:50]}")
            print(f"    Platform: {bounty['platform']} | Budget: ${bounty['budget']}")
            print(f"    Match: {scores['match_pct']:.0f}% | Skills: {', '.join(bounty['skills'][:3])}")
            print()

    elif cmd == "submit" and len(sys.argv) > 2:
        bounty_id = sys.argv[2]
        bounty = next((b for b in MOCK_BOUNTIES if b["id"] == bounty_id), None)
        if not bounty:
            print(f"Bounty {bounty_id} not found")
            sys.exit(1)
        result = submit_proposal(bounty)
        print(f"\nProposal submitted! ID: #{result['id']}")

    elif cmd == "status":
        get_pipeline_status()

    elif cmd == "proposal" and len(sys.argv) > 2:
        bounty_id = sys.argv[2]
        bounty = next((b for b in MOCK_BOUNTIES if b["id"] == bounty_id), None)
        if not bounty:
            print(f"Bounty {bounty_id} not found")
            sys.exit(1)
        print(generate_proposal(bounty))

    elif cmd == "submit-all":
        results = discover_bounties()
        print(f"\nSubmitting proposals for {len(results)} bounties...")
        for bounty, _ in results:
            result = submit_proposal(bounty)
            print(f"  Submitted: {bounty['title'][:40]}...")
        print("\nAll proposals submitted!")

    else:
        print("Usage:")
        print("  python bounty_factory.py discover    - Find matching bounties")
        print("  python bounty_factory.py submit <id>  - Submit proposal for bounty")
        print("  python bounty_factory.py status       - Show pipeline status")
        print("  python bounty_factory.py proposal <id> - Preview proposal")
        print("  python bounty_factory.py submit-all   - Auto-submit all matches")


if __name__ == "__main__":
    main()