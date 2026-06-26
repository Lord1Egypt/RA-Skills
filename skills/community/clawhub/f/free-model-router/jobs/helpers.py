"""Shared helpers for free-ride jobs."""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import requests

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OUTPUT_BASE = Path.home() / "rick-vault" / "brain" / "free-jobs"


def call_free_model(prompt, system="", model="google/gemma-3-27b-it:free"):
    """Call OpenRouter free model and return response text."""
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"model": model, "messages": messages},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[helpers] API error: {e}")
        return None


def save_output(job_name, data_dict):
    """Write JSON to ~/rick-vault/brain/free-jobs/{job_name}/{YYYY-MM-DD-HH}.json"""
    out_dir = OUTPUT_BASE / job_name
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d-%H") + ".json"
    path = out_dir / filename
    with open(path, "w") as f:
        json.dump(data_dict, f, indent=2)
    print(f"[helpers] Saved: {path}")
    return path


def notify(text):
    """Send notification via openclaw system event."""
    try:
        subprocess.run(
            ["openclaw", "system", "event", "--text", text, "--mode", "now"],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"[helpers] Notified: {text[:80]}...")
    except Exception as e:
        print(f"[helpers] Notify failed: {e}")


def parse_json_response(text):
    """Extract JSON from model response, handling markdown fences."""
    if not text:
        return None
    # Strip markdown code fences if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first and last fence lines
        lines = [l for l in lines[1:] if not l.strip().startswith("```")]
        cleaned = "\n".join(lines)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find JSON object in the text
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                pass
    print(f"[helpers] Failed to parse JSON from: {text[:200]}")
    return None
