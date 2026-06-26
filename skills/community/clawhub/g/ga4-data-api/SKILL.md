---
name: ga4-data-api
description: Query Google Analytics 4 (GA4) data through the Google Analytics Data API for trends, countries, sources, pages, and conversion analysis. Use when a user wants GA/GA4 metrics inside OpenClaw, wants to set up GA4 access, or needs GA4 reports such as activeUsers, sessions, country/source breakdowns, page trends, or key event analysis. For enterprise/internal GA data, first verify which Google account actually has permission before proposing service accounts or extra cloud setup.
---

# GA4 Data API

Use this skill to set up and query GA4 through OAuth user authorization.

## Default approach

Prefer **OAuth user authorization first**.

Use `scripts/install_ga4_openclaw.sh` + `scripts/ga4_query.py` for the normal path.

Only suggest **service accounts** later, when there is a clear need for headless/server-side access.

## Hard rules

1. **Check account + permission before setup**
   - Ask which Google account can actually log into GA and has property/account access.
   - Do not start with service-account setup by default for enterprise/internal data.

2. **Be honest about blockers**
   - If the user cannot add users, say it is a permission blocker.
   - If the OAuth app is still in Testing, say the account must be added to test users.
   - If the user can see the property but lacks admin controls, say it is an access-level issue instead of pretending the button is hidden.

## Setup flow

### Step 1 — Verify access model

Ask/confirm:
- Which Google account has GA access?
- Can the user log into that account?
- What is the GA4 Property ID?
- Is Google Analytics Data API already enabled?
- Is there already a Desktop OAuth client JSON?

### Step 2 — Install and wire credentials

Run:

```bash
bash ~/.openclaw/workspace/skills/ga4-data-api/scripts/install_ga4_openclaw.sh <GA4_PROPERTY_ID> <PATH_TO_CLIENT_SECRET_JSON>
```

This installs Python deps, copies the OAuth client JSON into `~/.config/openclaw/ga4-client.json`, and writes `GA4_PROPERTY_ID` into shell config.

### Step 3 — First authorization

Run:

```bash
python3 ~/.openclaw/workspace/skills/ga4-data-api/scripts/ga4_query.py \
  --metrics activeUsers,sessions \
  --dimensions date \
  --start 7daysAgo \
  --end today \
  --pretty
```

The browser will open. The user must choose the **same Google account that actually has GA access**.

Successful authorization creates:
- `~/.config/openclaw/ga4-token.json`

### Step 4 — Query examples

Recent trend:

```bash
python3 ~/.openclaw/workspace/skills/ga4-data-api/scripts/ga4_query.py \
  --metrics activeUsers,sessions \
  --dimensions date \
  --start 7daysAgo \
  --end yesterday \
  --pretty
```

Country split:

```bash
python3 ~/.openclaw/workspace/skills/ga4-data-api/scripts/ga4_query.py \
  --metrics activeUsers \
  --dimensions country \
  --start 7daysAgo \
  --end yesterday \
  --limit 50 \
  --pretty
```

Source split:

```bash
python3 ~/.openclaw/workspace/skills/ga4-data-api/scripts/ga4_query.py \
  --metrics sessions \
  --dimensions sessionSourceMedium \
  --start 7daysAgo \
  --end yesterday \
  --limit 50 \
  --pretty
```

## Analysis guidance

For trend questions:
- Prefer full days (`end=yesterday`) unless the user explicitly wants intraday.
- Call out whether a same-day drop is just partial-day data.

For conversion questions:
- Separate **traffic events** from **true conversion events**.
- If key events look too broad, recommend narrowing the event set before drawing product conclusions.

## References

- Read `references/setup.md` when the user needs the shareable setup process.
- Use `scripts/ga4_query.py` instead of hand-writing fresh GA SDK samples each time.
