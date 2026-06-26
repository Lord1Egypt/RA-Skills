import json, os, glob
from datetime import datetime, timezone

sessions_dir = "/home/victor/.openclaw/agents/main/sessions"
all_files = sorted(glob.glob(os.path.join(sessions_dir, "*.jsonl")))

candidates = []
for f in all_files:
    name = os.path.basename(f)
    if any(s in name for s in [".analyzed", ".deleted", ".reset", "trajectory", ".checkpoint"]):
        continue
    try:
        lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
    except Exception:
        continue
    updated_at = None
    session_key = None
    for line in lines:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if obj.get("type") == "session":
                ts = obj.get("timestamp")
                if ts:
                    if isinstance(ts, str):
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        updated_at = dt.timestamp()
                    elif isinstance(ts, (int, float)):
                        updated_at = ts / 1000 if ts > 1e12 else ts
                    session_key = obj.get("key", name)
                break
    if not updated_at:
        try:
            st = os.stat(f).st_mtime
            updated_at = st
        except Exception:
            continue
    candidates.append((updated_at, name, session_key or name, f))

candidates.sort(key=lambda x: x[0], reverse=True)
print(f"Total candidates: {len(candidates)}")
print(f"\nTop 5 most recent sessions:")
for i, (ts, name, sk, fp) in enumerate(candidates[:5]):
    dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(tz=None)
    current_marker = " ← CURRENT SESSION (DO NOT RENAME)" if i == 0 else ""
    print(f"  [{i+1}] {dt.strftime('%Y-%m-%d %H:%M:%S')} | {name}{current_marker}")
    if i == 0:
        print(f"       sessionKey: {sk}")
        print(f"       path: {fp}")