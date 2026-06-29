"""
memory_health.py — Memory system chain health check + retrieval freshness

Checks:
  vault→memory:    sync_vault_memory.py last success
  memory→qdrant:   vault_to_qdrant.py last success
  LM Studio:       embedding model availability
  Qdrant:          collection health

Usage:
  python scripts/memory_health.py
  python scripts/memory_health.py --json
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from shared_config import VAULT_DIR, MEMORY_DIR, DATA_DIR, SCRIPTS_DIR, QDRANT_URL, KB_COLLECTION

DEFAULT_STALE_HOURS = 6

STATE_FILES = {
    "vault_to_memory": SCRIPTS_DIR / ".guardian_state.json",
    "memory_to_qdrant": SCRIPTS_DIR / ".vault_sync_state.json",
    "lmstudio": DATA_DIR / ".lmstudio_state.json",
}


def file_age_hours(path):
    if not path or not path.exists():
        return None
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    return (datetime.now() - mtime).total_seconds() / 3600


def count_files(directory, pattern="*.md"):
    if not directory or not directory.exists():
        return 0
    return sum(1 for _ in directory.rglob(pattern))


def check_vault_to_memory(stale_hours):
    age = file_age_hours(STATE_FILES["vault_to_memory"])
    vault_count = count_files(VAULT_DIR)
    memory_count = count_files(MEMORY_DIR)
    return {
        "link": "vault→memory", "script": "vault_guardian.py",
        "last_sync_hours": round(age, 1) if age else None,
        "stale": age is not None and age > stale_hours,
        "vault_files": vault_count, "memory_files": memory_count,
        "file_gap": vault_count - memory_count,
        "health": "ok" if (age and age <= stale_hours) else "stale",
    }


def check_memory_to_qdrant(stale_hours):
    age = file_age_hours(STATE_FILES["memory_to_qdrant"])
    return {
        "link": "memory→qdrant", "script": "vault_to_qdrant.py",
        "last_sync_hours": round(age, 1) if age else None,
        "stale": age is not None and age > stale_hours,
        "health": "ok" if (age and age <= stale_hours) else (None if age is None else "stale"),
    }


def check_lmstudio():
    state_path = STATE_FILES["lmstudio"]
    if state_path and state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            return {
                "link": "embedding (LM Studio)",
                "healthy": state.get("healthy", False),
                "models_loaded": state.get("models_loaded", 0),
                "degraded": state.get("degraded", False),
            }
        except Exception:
            pass
    return {"link": "embedding (LM Studio)", "healthy": None, "models_loaded": 0}


def check_qdrant():
    try:
        import urllib.request
        req = urllib.request.Request(f"{QDRANT_URL}/collections/{KB_COLLECTION}")
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        points = data.get("result", {}).get("points_count", 0)
        return {"link": f"Qdrant ({KB_COLLECTION})", "points": points, "health": "ok"}
    except Exception as e:
        return {"link": f"Qdrant ({KB_COLLECTION})", "points": 0, "health": "error", "error": str(e)[:100]}


def run(stale_hours=DEFAULT_STALE_HOURS, json_output=False):
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stale_threshold_hours": stale_hours,
        "chains": [],
        "alerts": [],
    }

    chains = [
        check_vault_to_memory(stale_hours),
        check_memory_to_qdrant(stale_hours),
        check_lmstudio(),
        check_qdrant(),
    ]
    results["chains"] = chains

    for chain in chains:
        if chain.get("stale"):
            results["alerts"].append(f"WARN: {chain['link']} stale ({chain['last_sync_hours']}h)")
        if chain.get("health") == "error":
            results["alerts"].append(f"ERR: {chain['link']} unavailable: {chain.get('error','?')}")

    score = 100
    for chain in chains:
        if chain.get("health") == "error": score -= 30
        elif chain.get("stale"): score -= 15
        elif chain.get("degraded"): score -= 10
    results["health_score"] = max(0, score)
    results["grade"] = "A" if score >= 90 else ("B" if score >= 70 else ("C" if score >= 50 else "D"))

    if not json_output:
        print(f"=== memory_health {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
        for chain in chains:
            health = chain.get("health", "?")
            icon = "OK" if health == "ok" else ("WARN" if health == "stale" else ("ERR" if health == "error" else "??"))
            detail = ""
            if chain.get("last_sync_hours") is not None:
                detail += f" | sync={chain['last_sync_hours']}h ago"
            if chain.get("points") is not None:
                detail += f" | points={chain['points']}"
            print(f"  [{icon}] {chain['link']:<25s}{detail}")
        if results["alerts"]:
            for a in results["alerts"]:
                print(f"    {a}")
        else:
            print(f"\n  All chains healthy")
        print(f"\n  Health score: {results['health_score']}/100 (Grade {results['grade']})")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))

    return results


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.add_argument("--stale-threshold", type=int, default=DEFAULT_STALE_HOURS)
    args = p.parse_args()
    run(stale_hours=args.stale_threshold, json_output=args.json)
