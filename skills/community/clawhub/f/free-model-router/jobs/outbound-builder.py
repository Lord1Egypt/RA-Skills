#!/usr/bin/env python3
"""Job 2: Outbound Builder — generate personalized outbound DM drafts for targets."""

import json
from datetime import datetime
from pathlib import Path

from helpers import call_free_model, notify, parse_json_response, save_output

TARGETS_PATH = Path.home() / "rick-vault" / "projects" / "outreach" / "targets.json"
DRAFTS_DIR = Path.home() / "rick-vault" / "projects" / "outreach"
RADAR_DIR = Path.home() / "rick-vault" / "brain" / "free-jobs" / "radar"

DM_PROMPT = """You are Rick, an AI CEO product (meetrick.ai). Write a highly personalized 3-sentence DM for a potential customer.

Target: {name} at {company}
What we know: {context}
Rick's products: AI CEO Playbook ($29), Agency AI Automation Toolkit ($97), Managed AI CEO ($499/mo)

Rules: No pitch in opener. Lead with specific observation about their situation. One soft CTA. Under 300 chars. No em dashes.

Return JSON: {{"opener": "...", "offer_suggested": "...", "confidence": 0-10}}"""


def load_targets():
    """Load target list, creating empty file if missing."""
    if not TARGETS_PATH.exists():
        TARGETS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TARGETS_PATH, "w") as f:
            json.dump([], f, indent=2)
        print(f"[outbound] Created empty targets file: {TARGETS_PATH}")
        return []
    with open(TARGETS_PATH) as f:
        return json.load(f)


def load_radar_leads():
    """Load today's hot leads from the buyer intent radar."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    leads_path = RADAR_DIR / f"leads-{date_str}.json"
    if not leads_path.exists():
        return []
    try:
        with open(leads_path) as f:
            leads = json.load(f)
        # Convert leads to target format
        targets = []
        for lead in leads:
            if lead.get("score", 0) >= 7:
                targets.append({
                    "name": lead.get("username", "unknown"),
                    "company": "X/Twitter",
                    "context": f"Tweeted: {lead.get('tweet_text', '')[:200]}. "
                               f"Suggested tier: {lead.get('offer_tier', 'unknown')}. "
                               f"Followers: {lead.get('followers', 0)}",
                    "source": "radar",
                    "status": "new",
                })
        return targets
    except (json.JSONDecodeError, Exception) as e:
        print(f"[outbound] Error loading radar leads: {e}")
        return []


def main():
    print(f"[outbound] Starting outbound builder — {datetime.now().isoformat()}")

    # Load targets from file
    targets = load_targets()
    print(f"[outbound] {len(targets)} targets from targets.json")

    # Add radar leads
    radar_leads = load_radar_leads()
    if radar_leads:
        print(f"[outbound] {len(radar_leads)} hot leads from today's radar")
        targets.extend(radar_leads)

    # Filter to uncontacted only
    pending = [t for t in targets if t.get("status") != "contacted"]
    print(f"[outbound] {len(pending)} uncontacted targets to process")

    if not pending:
        print("[outbound] No targets to process. Done.")
        return

    drafts = []
    for i, target in enumerate(pending):
        name = target.get("name", "Unknown")
        company = target.get("company", "Unknown")
        context = target.get("context", "No additional context")

        print(f"[outbound] Drafting {i+1}/{len(pending)}: {name} at {company}")
        prompt = DM_PROMPT.format(name=name, company=company, context=context)
        response = call_free_model(prompt)
        result = parse_json_response(response)

        if not result:
            continue

        result["target_name"] = name
        result["target_company"] = company
        result["source"] = target.get("source", "manual")
        result["generated_at"] = datetime.now().isoformat()
        drafts.append(result)

    # Save drafts
    if drafts:
        date_str = datetime.now().strftime("%Y-%m-%d")
        drafts_path = DRAFTS_DIR / f"drafts-{date_str}.json"
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

        # Merge with existing drafts for today if any
        existing = []
        if drafts_path.exists():
            try:
                with open(drafts_path) as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, Exception):
                pass

        all_drafts = existing + drafts
        with open(drafts_path, "w") as f:
            json.dump(all_drafts, f, indent=2)
        print(f"[outbound] Saved {len(drafts)} new drafts to {drafts_path}")

        save_output("outbound", {
            "run_time": datetime.now().isoformat(),
            "targets_processed": len(pending),
            "drafts_generated": len(drafts),
            "drafts": drafts,
        })

        notify(f"Outbound: {len(drafts)} new DM drafts ready in {drafts_path.name}")
    else:
        print("[outbound] No drafts generated.")
        save_output("outbound", {
            "run_time": datetime.now().isoformat(),
            "targets_processed": len(pending),
            "drafts_generated": 0,
        })

    print("[outbound] Done.")


if __name__ == "__main__":
    main()
