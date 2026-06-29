"""
vault_guardian.py — Vault auto-maintenance guardian

Solves:
  1. Stale file detection (e.g., unresolved issues older than 3 days)
  2. Service health check (LM Studio, Qdrant)
  3. Broken link detection
  4. vault → memory incremental sync

Runs in heartbeat, 0 token cost.
"""
import os, sys, re, json, time
import datetime as dt
import subprocess
from pathlib import Path

from shared_config import VAULT_DIR, MEMORY_DIR, SYNC_DIRS, LMSTUDIO_MODELS_URL, LMSTUDIO_KEY

STATE_FILE = Path.home() / ".openclaw" / ".guardian_state.json"

STALE_PATTERNS = [
    (r"#.*blocked|#.*failed|#.*无法", "Title contains blocked/failed, >3 days stale"),
    (r"状态.*未解决|状态.*卡住|状态.*待修复", "Status unresolved/stuck, >3 days"),
]

MAX_STALE_DAYS = 3


def now():
    return dt.datetime.now()


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except:
            pass
    return {"last_guard": None, "alerts": [], "resolved": []}


def save_state(state):
    state["last_guard"] = now().isoformat()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def check_services():
    import urllib.request
    results = {}
    try:
        urllib.request.urlopen("http://127.0.0.1:6333/collections", timeout=3)
        results["qdrant"] = True
    except Exception as e:
        results["qdrant"] = False
        results["qdrant_error"] = str(e)[:100]

    try:
        req = urllib.request.Request(LMSTUDIO_MODELS_URL)
        if LMSTUDIO_KEY:
            req.add_header("Authorization", f"Bearer {LMSTUDIO_KEY}")
        resp = urllib.request.urlopen(req, timeout=5)
        results["lmstudio"] = resp.status == 200
    except Exception as e:
        results["lmstudio"] = False
        results["lmstudio_error"] = str(e)[:100]
    return results


def scan_stale_files():
    alerts = []
    threshold = now() - dt.timedelta(days=MAX_STALE_DAYS)
    for root, dirs, files in os.walk(VAULT_DIR):
        if ".git" in root:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            fp = Path(root) / fn
            mtime = dt.datetime.fromtimestamp(fp.stat().st_mtime)
            if mtime > threshold:
                continue
            try:
                content = fp.read_text(encoding="utf-8")
            except:
                continue
            for pattern, desc in STALE_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    rel = str(fp.relative_to(VAULT_DIR))
                    alerts.append({"file": rel, "days_stale": (now() - mtime).days, "issue": desc})
                    break
    return alerts


def sync_changed_vault_files(state):
    changed = []
    for dir_name in SYNC_DIRS:
        src = VAULT_DIR / dir_name
        if not src.exists():
            continue
        for md in src.rglob("*.md"):
            if md.stat().st_size > 50 * 1024:
                continue
            mtime = dt.datetime.fromtimestamp(md.stat().st_mtime)
            rel = str(md.relative_to(VAULT_DIR))
            key = f"synced:{rel}"
            last_sync = state.get(key)
            if last_sync and dt.datetime.fromisoformat(last_sync) >= mtime:
                continue
            dest = MEMORY_DIR / str(rel).replace(os.sep, "_")
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                dest.write_text(md.read_text(encoding="utf-8"), encoding="utf-8")
                state[key] = now().isoformat()
                changed.append(rel)
            except:
                pass
    return changed


def check_broken_links():
    broken = []
    for root, dirs, files in os.walk(VAULT_DIR):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            fp = Path(root) / fn
            try:
                content = fp.read_text(encoding="utf-8")
            except:
                continue
            refs = re.findall(r"\[\[([^\]]+)\]\]", content)
            for ref in refs[:5]:
                ref_name = ref.split("|")[0].strip()
                found = False
                for r, d, fs in os.walk(VAULT_DIR):
                    if found: break
                    for tf in fs:
                        candidate = ref_name if ref_name.endswith(".md") else ref_name + ".md"
                        if tf == candidate or tf == ref_name:
                            found = True; break
                if not found and len(broken) < 5:
                    broken.append(f"{fp.relative_to(VAULT_DIR)} -> [[{ref_name}]]")
    return broken


def run():
    state = load_state()
    report = []

    services = check_services()
    if not services.get("qdrant"):
        report.append("[CRITICAL] Qdrant offline")
    if not services.get("lmstudio"):
        report.append("[CRITICAL] LM Studio offline")
    if all(services.values()):
        report.append("[OK] All services online")

    stale = scan_stale_files()
    for s in stale:
        report.append(f"[STALE] {s['file']} — {s['issue']} ({s['days_stale']}d)")

    changed = sync_changed_vault_files(state)
    if changed:
        report.append(f"[SYNC] {len(changed)} vault files synced to memory/")

    broken = check_broken_links()
    for b in broken:
        report.append(f"[LINK BROKEN] {b}")

    md_count = sum(1 for r, d, fs in os.walk(VAULT_DIR) for f in fs if f.endswith(".md") and ".git" not in r)
    memory_count = sum(1 for r, d, fs in os.walk(MEMORY_DIR) for f in fs if f.endswith(".md")) if MEMORY_DIR.exists() else 0
    report.append(f"[STATS] vault: {md_count} files, memory: {memory_count} files")

    print(f"=== vault_guardian {now().strftime('%Y-%m-%d %H:%M')} ===")
    for line in report:
        print(f"  {line}")

    save_state(state)
    return report


if __name__ == "__main__":
    run()
