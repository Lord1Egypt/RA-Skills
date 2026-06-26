---
name: "BytesAgain X Manager"
description: "Manage X (Twitter) account: auto-post AI-generated tweets, monitor brand mentions, auto-like relevant posts, and send Telegram approval requests for replies."
version: "1.5.0"
author: "BytesAgain"
tags: ["twitter", "x", "social-media", "automation", "ai-content", "engagement"]
credentials:
  - name: X_API_KEY
    description: X (Twitter) API Key from developer.x.com
    required: true
  - name: X_API_SECRET
    description: X API Key Secret
    required: true
  - name: X_ACCESS_TOKEN
    description: X Access Token (account-specific, Read+Write)
    required: true
  - name: X_ACCESS_TOKEN_SECRET
    description: X Access Token Secret
    required: true
  - name: X_USER_ID
    description: Your X account user ID (numeric)
    required: true
  - name: XAI_API_KEY
    description: xAI API key for tweet draft generation via Grok
    required: true
  - name: TG_TOKEN
    description: Telegram bot token for approval notifications
    required: true
  - name: TG_CHAT
    description: Telegram chat ID to receive notifications
    required: true
---

# BytesAgain X Manager

Manage your X (Twitter) account with automated posting, monitoring, and engagement. Generates tweet drafts via xAI, validates content before posting, and routes mention replies through human approval.

## Setup

This skill requires the following environment variables to be configured before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `X_API_KEY` | ✅ | X API Key from developer.x.com (Read+Write app) |
| `X_API_SECRET` | ✅ | X API Key Secret |
| `X_ACCESS_TOKEN` | ✅ | X Access Token (account-specific) |
| `X_ACCESS_TOKEN_SECRET` | ✅ | X Access Token Secret |
| `X_USER_ID` | ✅ | Your X account numeric user ID |
| `XAI_API_KEY` | ✅ | xAI API key for Grok tweet generation |
| `TG_TOKEN` | ✅ | Telegram bot token for approval notifications |
| `TG_CHAT` | ✅ | Telegram chat ID to receive notifications |

No credentials are stored or transmitted by this skill. All values are read from environment variables at runtime only.

## What This Skill Owns
- Tweet posting and replies: publish content via X API OAuth 1.0a with pre-post validation
- Daily content generation: create 3 tweet drafts/day using xAI trend analysis
- Brand monitoring: scan @bytesagain mentions every 2 hours, draft replies for approval
- Auto-like: like AI/skill related tweets to grow visibility
- Competitor tracking: monitor @openclaw and related accounts
- Telegram approval workflow: route all mention replies through human confirmation

## What This Skill Does Not Cover
- Sending DMs (requires additional OAuth scope not currently enabled)
- Deleting tweets (requires explicit human authorization per tweet)
- Deep analytics (follower growth trends, engagement rate analysis)
- Posting images or videos (text-only)
- Accessing private or protected accounts
- Publishing skills to ClawHub (use skill-manager for that)

## Commands

### draft
Generate 3 tweet drafts for the day using xAI trend analysis. Saves to `/tmp/x-drafts-YYYY-MM-DD.json`.
```bash
bash scripts/script.sh draft
```

### post
Post a tweet from today's saved drafts. Use `--index` to select which draft (0=first, 1=second, 2=third).
```bash
bash scripts/script.sh post --index 0
bash scripts/script.sh post --index 1
bash scripts/script.sh post --index 2
```

### monitor
Run brand and competitor monitoring report. Tracks @bytesagain mentions, @openclaw activity, and AI skill trends. Sends Telegram report with Chinese summary.
```bash
bash scripts/script.sh monitor
```

### like
Auto-like recent tweets matching AI agent / skill keywords. Skips own tweets and already-liked posts.
```bash
bash scripts/script.sh like
```

### scan-mentions
Scan recent @bytesagain mentions, draft replies via xAI, and send Telegram approval requests to operator.
```bash
bash scripts/script.sh scan-mentions
```

### send-reply
Send a pre-approved reply to one or more tweets. Multiple IDs are staggered 30–90 seconds apart to appear natural.
```bash
bash scripts/script.sh send-reply <tweet_id>
bash scripts/script.sh send-reply <tweet_id1> <tweet_id2> <tweet_id3>
```

### status
Show pending approval queue and today's saved drafts.
```bash
bash scripts/script.sh status
```

## Approval Workflow

1. `scan-mentions` detects new @bytesagain mentions
2. xAI drafts a reply for each mention
3. Telegram message sent to operator: original tweet + draft reply + tweet ID
4. Operator replies **发 \<tweet_id\>** to approve, **跳过 \<tweet_id\>** to skip
5. Agent calls `send-reply <tweet_id>` to post the approved reply

## Validation Rules (pre-post checks)

All tweets are validated before posting:

| Check | Result |
|-------|--------|
| Link in tweet body | ❌ Blocked (X penalizes -40%) |
| More than 2 hashtags | ❌ Blocked |
| Specific large numbers (e.g. 10000, 500K) | ❌ Blocked (may be inaccurate) |
| Banned words (guaranteed, make money…) | ❌ Blocked |
| No question mark | ⚠️ Warning only |
| Tweet under 50 characters | ⚠️ Warning only |

Blocked tweets trigger a Telegram notification with the reason. Fallback preset templates are used if xAI times out.

## Recommended Cron Schedule

```
30 8  * * *     monitor          # Daily brand report
0  9  * * *     draft            # Generate daily drafts (1 xAI call/day)
0  9,13,17,21 * * *  like        # Auto-like 4x daily
5  10 * * *     post --index 0   # Post tweet #1
5  15 * * *     post --index 1   # Post tweet #2
5  20 * * *     post --index 2   # Post tweet #3
0  */2 * * *    scan-mentions    # Check mentions every 2 hours
```

## State Files

| File | Purpose |
|------|---------|
| `/tmp/x-drafts-YYYY-MM-DD.json` | Daily tweet drafts |
| `/tmp/x-liked-ids.json` | Dedup: already-liked IDs (last 500) |
| `/tmp/x-seen-mentions.json` | Dedup: processed mention IDs (last 200) |
| `/tmp/x-pending-replies.json` | Pending approval queue |

## Requirements

- Python 3.8+
- `requests` — HTTP client
- `requests-oauthlib` — OAuth 1.0a for X API

```bash
pip install requests requests-oauthlib
```

## References
- [Command Boundary](references/command-boundary.md) — full in/out-of-scope rules and safety constraints
- [API Notes](references/api-notes.md) — X API v2 rate limits, auth, and cost estimates

## Evals
Trigger boundary test cases: [evals/trigger_cases.json](evals/trigger_cases.json) — 12 cases (6 positive + 6 negative)

## Feedback
https://bytesagain.com/feedback/
Powered by BytesAgain | bytesagain.com
