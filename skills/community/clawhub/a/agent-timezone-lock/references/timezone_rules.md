# Timezone Conversion Rules & Edge Cases

## The Core Rule

**Every time value from a non-human source is UTC until proven otherwise.**

Sources that give UTC by default:
- System clock via `datetime.utcnow()` or `time.time()`
- API responses (GitHub, Stripe, Google APIs, etc.) — usually ISO 8601 with `Z` suffix
- Cron job timestamps
- OpenClaw heartbeat/cron trigger times
- Log files (server logs are almost always UTC)
- Database timestamps (unless explicitly stored with timezone)

Sources that give local time:
- USER.md (human-written)
- User chat messages ("remind me at 3pm")
- Calendar apps when properly configured
- The output of `now.py` (already converted)

## Conversion Patterns

### Pattern 1: API timestamp to local
```
Input:  "2026-03-30T19:05:00Z"  (UTC)
Step 1: Recognize the Z suffix = UTC
Step 2: Run now.py or use pytz/zoneinfo to convert
Output: "3:05 PM ET" (US Eastern, UTC-4 in DST)
```

### Pattern 2: User says "remind me at 3pm"
```
Input:  "3pm" from user
Rule:   User messages are always local time
Output: Schedule at 3pm in user's configured timezone
        DO NOT schedule at 3pm UTC
```

### Pattern 3: Cron trigger fires
```
Cron fires: 2026-03-30T13:00:00 (system time, likely UTC)
Local time: 9:00 AM ET (UTC-4)
Report as: "Good morning, 9:00 AM ET"
```

## DST Rules (US Eastern — Mario's timezone)

- Standard time (EST): UTC-5  (Nov first Sunday → Mar second Sunday)
- Daylight time (EDT): UTC-4  (Mar second Sunday → Nov first Sunday)
- Mario's timezone: `America/New_York` handles DST automatically via IANA database

**Never hardcode UTC-5 for Eastern.** Always use `America/New_York` and let the library handle DST.

## Red Flags — Signs of UTC Confusion

These are warning signs that an LLM is confusing UTC with local time:

1. User is in US Eastern, and the agent reports a time 4-5 hours ahead of expected
2. Times end in `:00Z` or include `+00:00` in the output to the user
3. Agent says "6:29 PM ET" when user's watch says 2:29 PM
4. Scheduled event fires at the wrong hour
5. "I'll remind you at 3 PM" executes at 7 PM

When you detect this: correct immediately, run `now.py`, apologize briefly, and move on.

## Python: Correct vs Incorrect

```python
# ❌ WRONG — returns naive UTC disguised as local
from datetime import datetime
now = datetime.now()  # naive, system timezone (often UTC on servers)
print(f"It's {now.strftime('%I:%M %p')}")  # Might say 7:05 PM when it's 3:05 PM ET

# ✅ CORRECT — use zoneinfo with explicit timezone
from datetime import datetime
from zoneinfo import ZoneInfo
tz = ZoneInfo("America/New_York")
now = datetime.now(tz)
print(f"It's {now.strftime('%I:%M %p %Z')}")  # "3:05 PM EDT"

# ✅ ALSO CORRECT — always use now.py script to avoid dependencies
import subprocess
result = subprocess.run(["python3", "skills/timezone/scripts/now.py"], capture_output=True, text=True)
print(result.stdout)
```

## When `zoneinfo` Is Not Available

Fallback chain:
1. Try `from zoneinfo import ZoneInfo` (Python 3.9+)
2. Try `from backports.zoneinfo import ZoneInfo` (pip install backports.zoneinfo)
3. Try `import pytz` (pip install pytz)
4. If all fail: report system local time with a warning, recommend installing `pytz`

## Common IANA Timezone Names

| User says | IANA name | Notes |
|-----------|-----------|-------|
| ET / Eastern | America/New_York | Handles EST/EDT automatically |
| CT / Central | America/Chicago | Handles CST/CDT |
| MT / Mountain | America/Denver | Handles MST/MDT |
| PT / Pacific | America/Los_Angeles | Handles PST/PDT |
| Arizona | America/Phoenix | No DST |
| UK | Europe/London | Handles GMT/BST |
| Paris / CET | Europe/Paris | Handles CET/CEST |
| IST / India | Asia/Kolkata | UTC+5:30, no DST |
| JST / Japan | Asia/Tokyo | UTC+9, no DST |
| AEST / Sydney | Australia/Sydney | Handles AEST/AEDT |
