---
name: duolingo-tracker
version: 1.0.0
description: >
  Fetch and display Duolingo learning stats: streak, XP, league, level,
  course progress, and daily/weekly summaries. Use this skill whenever the
  user asks about their Duolingo progress, streak, how much XP they've
  earned, what league they're in, or wants a learning summary. Trigger on
  phrases like "check my Duolingo", "what's my streak", "Duolingo stats",
  "how am I doing on Duolingo", or "my language learning progress".
metadata:
  clawdbot:
    requires:
      bins: ["curl", "python3"]
      env:
        - name: DUOLINGO_JWT
          description: "Duolingo JWT auth token (see setup below)"
          optional: true
---

# Duolingo Tracker Skill

Fetch Duolingo user stats via the unofficial Duolingo API. No official API key required — uses the same endpoints the Duolingo web app uses.

---

## Authentication setup

Duolingo does not offer an official public API. The tracker uses the cookie-based session token from an active browser session.

**One-time setup:**

1. Log in to duolingo.com in your browser
2. Open DevTools → Application → Cookies → `duolingo.com`
3. Copy the value of the `jwt_token` cookie
4. Save it: `export DUOLINGO_JWT="your_token_here"`

Alternatively the user can provide their **username** only — a subset of public stats is available without auth.

---

## Base URL

```
https://www.duolingo.com/2017-06-30
```

All requests should include:
```
Accept: application/json
Content-Type: application/json
Authorization: Bearer $DUOLINGO_JWT   # omit if unauthenticated
```

---

## Fetch user profile and streak

```bash
curl -s "https://www.duolingo.com/2017-06-30/users?username=USERNAME&fields=streak,xpGoal,xpGoalMetToday,lingots,totalXp,currentCourse,courses,streakData" \
  -H "Authorization: Bearer $DUOLINGO_JWT" \
  -H "Accept: application/json"
```

Key fields to surface:

| Field | Meaning |
|---|---|
| `streak` | Current day streak |
| `streakData.currentStreak.length` | Days in current streak |
| `streakData.longestStreak.length` | All-time longest streak |
| `totalXp` | Lifetime XP |
| `xpGoal` | Daily XP goal |
| `xpGoalMetToday` | Whether today's goal is met (bool) |
| `courses[].xp` | XP per language course |
| `courses[].crowns` | Crowns earned per course |
| `courses[].title` | Language name |

---

## Fetch leaderboard / league info

```bash
# Get user ID first from profile, then:
curl -s "https://duolingo-leaderboards-prod.duolingo.com/leaderboards/7d9f5dd1-8423-491a-91f2-2532052038d8/users/USER_ID?get_users_only=true" \
  -H "Authorization: Bearer $DUOLINGO_JWT"
```

League tiers (low → high): Bronze, Silver, Gold, Sapphire, Ruby, Emerald, Amethyst, Pearl, Obsidian, Diamond.

---

## Fetch XP summary (last 7 days)

```bash
curl -s "https://www.duolingo.com/2017-06-30/users/USER_ID/xp_summaries?startDate=YYYY-MM-DD" \
  -H "Authorization: Bearer $DUOLINGO_JWT"
```

Set `startDate` to 7 days ago. Returns daily XP totals — use these to show a mini chart or bar summary.

---

## Displaying results

Present stats in this format:

```
🔥 Streak: 47 days  (longest: 93 days)
⭐ Today: 150 XP / 100 XP goal ✓
📚 Active course: Spanish (es) — 3,420 XP, 42 crowns
🏆 League: Gold  |  Weekly XP: 892

Weekly XP:
Mon ████████ 180
Tue ██████   120
Wed █████    100
Thu ████████ 160
Fri ██████   132
Sat ███      60 
Sun ████████ 140
```

If the daily goal is not yet met, flag it clearly so the user knows to practice today.

---

## Public stats (no auth required)

For users who don't want to share their JWT, these endpoints work without auth for public profiles:

```bash
curl -s "https://www.duolingo.com/users/USERNAME" \
  -H "Accept: application/json"
```

Returns `streak`, `learning_language`, `level`, `totalXp`, `courses`. Fewer fields but sufficient for a quick summary.

---

## Common issues

| Problem | Fix |
|---|---|
| 401 Unauthorized | JWT expired — user needs to re-copy token from browser |
| Empty streak data | User hasn't practiced in 7+ days (streak likely 0) |
| Username not found | Check exact username (case-sensitive) on duolingo.com/profile |
| Rate limited (429) | Wait 60 seconds before retrying |

---

## Privacy note

Always remind the user that their JWT token is sensitive — treat it like a password. Never log it or include it in outputs.
