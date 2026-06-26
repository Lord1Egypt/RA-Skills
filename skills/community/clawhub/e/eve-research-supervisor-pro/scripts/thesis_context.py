#!/usr/bin/env python3
"""
thesis_context.py — Feature 4: Thesis Context File
Stores YOUR specific research context so gap detection and idea generation
are targeted to your exact thesis, not generic.
Usage:
  python3 thesis_context.py init                    — interactive setup
  python3 thesis_context.py show                    — show current context
  python3 thesis_context.py update <field> <value>  — update a field
  python3 thesis_context.py export                  — export as context string for LLM
"""

import sys
import os
import json
import datetime

CONTEXT_FILE = os.path.expanduser(
    "~/.openclaw/workspace/research-supervisor-pro/memory/thesis_context.json"
)


def load_context():
    if not os.path.exists(CONTEXT_FILE):
        return {}
    with open(CONTEXT_FILE) as f:
        return json.load(f)


def save_context(data):
    os.makedirs(os.path.dirname(CONTEXT_FILE), exist_ok=True)
    data["last_updated"] = datetime.datetime.now().isoformat()
    with open(CONTEXT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Thesis context saved → {CONTEXT_FILE}")


def interactive_init():
    print("\n🎓 THESIS CONTEXT SETUP")
    print("━" * 50)
    print("I'll remember your exact research context forever.")
    print("This makes gap detection and ideas much more targeted.\n")

    ctx = load_context()

    questions = [
        ("thesis_title",      "Thesis title:"),
        ("your_claim",        "Your main claim / contribution (1-2 sentences):"),
        ("baseline_paper",    "Your key baseline paper (arXiv ID or title):"),
        ("baseline_result",   "Baseline result you're trying to beat (e.g. 41.2% bit accuracy):"),
        ("your_method",       "Your proposed method (brief description):"),
        ("attack_types",      "Attack types you're testing against:"),
        ("watermark_methods", "Watermark methods you're using (e.g. HiDDeN, StegaStamp):"),
        ("datasets",          "Datasets you're using:"),
        ("metrics",           "Evaluation metrics (e.g. BER, PSNR, SSIM):"),
        ("target_venue",      "Target venue (journal/conference):"),
        ("supervisor",        "Supervisor name:"),
        ("deadline",          "Submission deadline:"),
        ("university",        "University / department:"),
    ]

    for key, prompt in questions:
        current = ctx.get(key, "")
        if current:
            val = input(f"{prompt}\n  [current: {current[:60]}] → ").strip()
            if not val:
                val = current
        else:
            val = input(f"{prompt}\n  → ").strip()
        if val:
            ctx[key] = val

    save_context(ctx)
    print("\n✅ Thesis context saved! EVE will now give you targeted suggestions.")
    return ctx


def show_context():
    ctx = load_context()
    if not ctx:
        print("❌ No thesis context found. Run: python3 thesis_context.py init")
        return

    print("\n🎓 YOUR THESIS CONTEXT")
    print("━" * 50)
    fields = [
        ("thesis_title",      "Thesis Title"),
        ("your_claim",        "Your Claim"),
        ("baseline_paper",    "Baseline Paper"),
        ("baseline_result",   "Baseline Result"),
        ("your_method",       "Your Method"),
        ("attack_types",      "Attack Types"),
        ("watermark_methods", "Watermark Methods"),
        ("datasets",          "Datasets"),
        ("metrics",           "Metrics"),
        ("target_venue",      "Target Venue"),
        ("supervisor",        "Supervisor"),
        ("deadline",          "Deadline"),
        ("university",        "University"),
    ]
    for key, label in fields:
        val = ctx.get(key, "—")
        print(f"  {label:<22}: {val}")
    print(f"\n  Last updated: {ctx.get('last_updated','?')[:16]}")
    print("━" * 50)


def export_context():
    """Export as a compact string for injection into LLM prompts."""
    ctx = load_context()
    if not ctx:
        return ""

    lines = [
        "=== USER THESIS CONTEXT (use this to make suggestions specific) ===",
        f"Thesis: {ctx.get('thesis_title', '')}",
        f"Claim: {ctx.get('your_claim', '')}",
        f"Baseline: {ctx.get('baseline_paper', '')} — result: {ctx.get('baseline_result', '')}",
        f"Method: {ctx.get('your_method', '')}",
        f"Attacks tested: {ctx.get('attack_types', '')}",
        f"Watermark methods: {ctx.get('watermark_methods', '')}",
        f"Datasets: {ctx.get('datasets', '')}",
        f"Metrics: {ctx.get('metrics', '')}",
        f"Target venue: {ctx.get('target_venue', '')}",
        f"Deadline: {ctx.get('deadline', '')}",
        "=== END CONTEXT ===",
    ]
    return "\n".join(lines)


def update_field(field, value):
    ctx = load_context()
    ctx[field] = value
    save_context(ctx)
    print(f"✅ Updated {field} → {value}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "init":
        interactive_init()
    elif sys.argv[1] == "show":
        show_context()
    elif sys.argv[1] == "export":
        print(export_context())
    elif sys.argv[1] == "update" and len(sys.argv) >= 4:
        update_field(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
