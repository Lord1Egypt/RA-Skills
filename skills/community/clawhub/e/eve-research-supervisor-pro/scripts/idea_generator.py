#!/usr/bin/env python3
"""
idea_generator.py — Generate real research ideas from detected gaps using LLM
Falls back to structured templates if no API key.
Usage: python3 idea_generator.py [gaps_file] [api_key]
"""

import os
import sys
import re
import json
import requests

# ── Config ──────────────────────────────────────────────────────────────────
def _get_api_config():
    """Use PetClaw built-in API first, fall back to env vars."""
    settings_path = os.path.expanduser("~/.petclaw/petclaw-settings.json")
    try:
        import json as _j
        with open(settings_path) as f:
            d = _j.load(f)
        key = d.get("brainApiKey", "")
        if key:
            return {
                "key":   key,
                "base":  d.get("brainApiUrl", "https://petclaw.ai/api/v1"),
                "model": os.environ.get("IDEA_MODEL", d.get("brainModel", "petclaw-1.0"))
            }
    except Exception:
        pass
    return {
        "key":   os.environ.get("OPENAI_API_KEY", ""),
        "base":  os.environ.get("OPENAI_BASE_URL", "https://api.openai-hk.com/v1"),
        "model": os.environ.get("IDEA_MODEL", "gpt-4o")
    }

_cfg        = _get_api_config()
OPENAI_BASE = _cfg["base"]
OPENAI_KEY  = _cfg["key"]
MODEL       = _cfg["model"]


def generate_ideas_llm(gaps_text, api_key):
    """Use LLM to generate concrete, publishable research ideas."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a senior AI researcher and research supervisor. "
                    "Given a list of research gaps, generate specific, concrete, and publishable research ideas. "
                    "For each idea provide:\n"
                    "- Title: A clear paper title\n"
                    "- Problem: What gap it addresses\n"
                    "- Method: Proposed approach (specific, not vague)\n"
                    "- Baselines: What to compare against\n"
                    "- Metrics: How to evaluate\n"
                    "- Venue: Target conference/journal (e.g. CVPR, NeurIPS, IEEE TIFS)\n"
                    "- Novelty: Why this is new\n\n"
                    "Generate 5 ideas. Be specific and realistic."
                )
            },
            {
                "role": "user",
                "content": f"Generate research ideas from these gaps:\n\n{gaps_text[:3000]}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    try:
        r = requests.post(f"{OPENAI_BASE}/chat/completions", headers=headers, json=payload, timeout=45)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"  ⚠️  LLM call failed: {e}. Using template fallback.")
        return None


def generate_ideas_template(gaps):
    """Fallback: structured template-based ideas."""
    ideas = []
    for i, gap in enumerate(gaps[:5], 1):
        idea = (
            f"## Idea {i}\n"
            f"**Title:** Addressing: {gap[:80]}\n"
            f"**Problem:** {gap}\n"
            f"**Method:** Propose a novel approach to solve this gap using deep learning / LLM-guided methods.\n"
            f"**Baselines:** Compare against existing SOTA methods in this area.\n"
            f"**Metrics:** Accuracy, robustness, computational efficiency.\n"
            f"**Venue:** IEEE Transactions / CVPR / NeurIPS\n"
            f"**Novelty:** First work to directly address this specific limitation.\n"
        )
        ideas.append(idea)
    return "\n\n".join(ideas)


def generate_ideas(gaps_file="gaps.md", api_key=None):
    if not os.path.exists(gaps_file):
        print(f"❌ {gaps_file} not found. Run gap_detector.py first.")
        sys.exit(1)

    with open(gaps_file) as f:
        gaps_text = f.read()

    # Parse individual gaps
    gaps = [line.strip().lstrip("0123456789. ") for line in gaps_text.split("\n")
            if line.strip() and not line.startswith("#")]
    gaps = [g for g in gaps if len(g) > 20]

    print(f"💡 Generating research ideas from {len(gaps)} gaps...")

    key = api_key or OPENAI_KEY
    ideas_text = None

    if key:
        print("  Using LLM-based idea generation...")
        ideas_text = generate_ideas_llm(gaps_text, key)

    if not ideas_text:
        print("  Using template-based idea generation (fallback)...")
        ideas_text = generate_ideas_template(gaps)

    with open("ideas.md", "w") as f:
        f.write("# Generated Research Ideas\n\n")
        f.write(ideas_text)

    print(f"\n✅ Research ideas saved → ideas.md")
    return ideas_text


if __name__ == "__main__":
    gaps_file = sys.argv[1] if len(sys.argv) > 1 else "gaps.md"
    api_key   = sys.argv[2] if len(sys.argv) > 2 else None
    generate_ideas(gaps_file, api_key)
