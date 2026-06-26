#!/usr/bin/env python3
"""
gap_detector.py — Detect research gaps using LLM analysis (not just keyword matching)
Falls back to keyword matching if no API key available.
Usage: python3 gap_detector.py [notes_file] [api_key]
"""

import os
import sys
import re
import json
import requests
import json as _json

# ── Config ──────────────────────────────────────────────────────────────────
def _get_api_config():
    """Use PetClaw built-in API first, fall back to env vars."""
    settings_path = os.path.expanduser("~/.petclaw/petclaw-settings.json")
    try:
        with open(settings_path) as f:
            d = json.load(f)
        key = d.get("brainApiKey", "")
        if key:
            return {
                "key":   key,
                "base":  d.get("brainApiUrl", "https://petclaw.ai/api/v1"),
                "model": os.environ.get("GAP_MODEL", d.get("brainModel", "petclaw-1.0"))
            }
    except Exception:
        pass
    return {
        "key":   os.environ.get("OPENAI_API_KEY", ""),
        "base":  os.environ.get("OPENAI_BASE_URL", "https://api.openai-hk.com/v1"),
        "model": os.environ.get("GAP_MODEL", "gpt-4o")
    }

_cfg        = _get_api_config()
OPENAI_BASE = _cfg["base"]
OPENAI_KEY  = _cfg["key"]
MODEL       = _cfg["model"]

GAP_KEYWORDS = [
    "however", "but", "limited", "limitation", "lack", "challenge",
    "future work", "not addressed", "open problem", "remains unclear",
    "to our knowledge", "no existing", "insufficient", "gap", "drawback",
    "unable to", "fails to", "does not handle", "beyond the scope"
]

def detect_gaps_llm(text_chunk, api_key):
    """Use LLM to intelligently detect research gaps."""
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
                    "You are a research assistant. Given text extracted from research papers, "
                    "identify concrete research gaps, limitations, and unsolved problems. "
                    "Return a JSON array of gap strings. Be specific and concise. "
                    "Example: [\"No benchmark exists for X\", \"Method fails under Y conditions\"]"
                )
            },
            {
                "role": "user",
                "content": f"Extract research gaps from this text:\n\n{text_chunk[:3000]}"
            }
        ],
        "temperature": 0.3,
        "max_tokens": 800
    }
    try:
        r = requests.post(f"{OPENAI_BASE}/chat/completions", headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"].strip()
        # Parse JSON array from response
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            return json.loads(match.group())
        return [content]
    except Exception as e:
        print(f"  ⚠️  LLM call failed: {e}. Falling back to keyword matching.")
        return None


def detect_gaps_keywords(text):
    """Fallback: simple keyword-based gap detection."""
    gaps = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for s in sentences:
        s = s.strip()
        if len(s) < 20:
            continue
        for kw in GAP_KEYWORDS:
            if kw in s.lower():
                gaps.append(s)
                break
    return list(set(gaps))


def detect_gaps(notes_file="notes.md", api_key=None):
    if not os.path.exists(notes_file):
        print(f"❌ {notes_file} not found. Run pdf_parser.py first.")
        sys.exit(1)

    with open(notes_file) as f:
        text = f.read()

    print(f"🔬 Detecting research gaps from {notes_file}...")

    gaps = []

    # Try LLM first
    key = api_key or OPENAI_KEY
    if key:
        print("  Using LLM-based gap detection...")
        # Process in chunks (notes can be large)
        chunk_size = 3000
        chunks = [text[i:i+chunk_size] for i in range(0, min(len(text), 15000), chunk_size)]
        for chunk in chunks:
            result = detect_gaps_llm(chunk, key)
            if result:
                gaps.extend(result)
    
    # Fallback or supplement with keywords
    if not gaps:
        print("  Using keyword-based gap detection (fallback)...")
        gaps = detect_gaps_keywords(text)

    # Deduplicate
    gaps = list(dict.fromkeys(gaps))

    with open("gaps.md", "w") as f:
        f.write("# Detected Research Gaps\n\n")
        for i, g in enumerate(gaps, 1):
            f.write(f"{i}. {g}\n\n")

    print(f"\n✅ Detected {len(gaps)} research gaps → gaps.md")
    return gaps


if __name__ == "__main__":
    notes_file = sys.argv[1] if len(sys.argv) > 1 else "notes.md"
    api_key    = sys.argv[2] if len(sys.argv) > 2 else None
    detect_gaps(notes_file, api_key)
