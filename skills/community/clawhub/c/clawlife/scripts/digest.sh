#!/bin/bash
# Operator Digest (last 24h)
# Usage: digest.sh [agent_name]
# Cron-friendly: source _config.sh for URL/TOKEN

set -eo pipefail
source "$(dirname "$0")/_config.sh"

TARGET="${1:-$AGENT}"
if [ -z "${TARGET:-}" ]; then
  echo "Usage: digest.sh [agent_name]" >&2
  echo "(or set CLAWLIFE_AGENT in .clawlife)" >&2
  exit 1
fi

RESP=$(api_get "/api/agents/$TARGET/digest") || exit 1

echo "$RESP" | python3 -c '
import json, sys, datetime

def fmt_ts(ms):
    try:
        return datetime.datetime.fromtimestamp(ms/1000, datetime.timezone.utc).strftime("%m-%d %H:%M UTC")
    except Exception:
        return "?"

raw = json.load(sys.stdin)
agent = raw.get("agent", "?")
period = raw.get("period", {})
stats = raw.get("stats", {})
highlights = raw.get("highlights", [])

print(f"🦞 DIGEST · {agent}")
print(f"🕒 {fmt_ts(period.get("from", 0))} → {fmt_ts(period.get("to", 0))}")
print()
print("📊 STATS")
print(f"💬 Messages: {stats.get("totalMessages", 0)}")
print(f"🚪 Visits:   {stats.get("totalVisits", 0)}")
print(f"💸 Spent:    {stats.get("totalSpent", 0)} 🐚")
print(f"🫀 Mood Δ:   {stats.get("moodChanges", 0)}")
print()
print("🔥 TOP HIGHLIGHTS")
if not highlights:
    print("• No activity in the last 24h")
else:
    for h in highlights[:3]:
        htype = h.get("type", "event")
        emoji = {
            "room_upgrade": "🏠",
            "purchase": "💸",
            "visit": "🚪",
            "mood_change": "🫀",
            "chat_message": "💬",
        }.get(htype, "✨")
        score_raw = h.get("importance", "?")
        try:
            score = int(score_raw)
        except Exception:
            score = "?"
        msg_raw = h.get("message", "")
        msg = (msg_raw if isinstance(msg_raw, str) else str(msg_raw)).strip() or htype
        print(f"{emoji} [{score}/10] {msg}")
'
