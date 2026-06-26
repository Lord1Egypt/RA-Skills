---
name: football-transfer-intel
description: Football transfer intelligence — real-time rumour tracking, AI Truth Meter credibility scores, and multi-source verification across 137,000+ transfer events
version: "1.0.0"
homepage: https://github.com/LeoandLeon/rising-transfers-clawhub-skills
metadata:
  clawdbot:
    emoji: "📡"
    requires:
      env: ["RT_API_KEY"]
    primaryEnv: "RT_API_KEY"
---

# Football Transfer Intel — Real-Time Rumour Intelligence

Track football transfer rumours in real time. Aggregated from **3 independent data sources** (Transfermarkt, Sportmonks, and social signals), with an AI **Truth Meter** that scores each rumour from 0–100 for credibility. No more guessing which transfer stories are real.

Free tier includes trending hot topics with no API key required.

---

## External Endpoints

| Endpoint | Method | Data Sent | Purpose |
|----------|--------|-----------|---------|
| `https://api.risingtransfers.com/api/v1/intelligence/hot-topics` | GET | None | Trending football transfers (free, 0 credits) |
| `https://api.risingtransfers.com/api/v1/intelligence/transfer` | POST | `{ "name": "<player_name>" }` | Player transfer rumour detail (3 credits) |
| `https://api.risingtransfers.com/api/v1/intel/verify` | GET | `?q=<player>+to+<club>` | Truth Meter credibility score (1–5 credits) |

No data is sent to any other endpoint. No conversation history is transmitted.

---

## Security & Privacy

- **What leaves your machine**: Player name and/or club name from your query only
- **What does NOT leave your machine**: Conversation history, other skills, local files, or your API key value (sent as HTTP header only)
- **Authentication**: `RT_API_KEY` is sent as `X-RT-API-Key` header to `api.risingtransfers.com` only
- **Hot topics** (trending list) can be fetched without any API key at 0 credits
- **Data retention**: Query logs kept for rate limiting (max 24 hours). No personal data stored

---

## Model Invocation Note

This skill may be invoked autonomously when you ask about football transfer news, rumours, or whether a specific deal is likely to happen. To disable autonomous invocation: `claw config set skill.auto-discover false`. Credit consumption applies only to authenticated calls for detailed intelligence.

---

## Trust Statement

By using this skill, player and club names from your queries are sent to Rising Transfers (`api.risingtransfers.com`). Rising Transfers aggregates public football transfer rumour data — no sensitive or personal information is involved. Only install this skill if you trust Rising Transfers with those search terms.

---

## Trigger

When the user asks about:
- Football transfer rumours for a specific player or club
- Whether a football transfer deal is likely or credible
- Latest hot football transfer topics or trending deals
- Verifying if a football transfer story is genuine or fake
- Truth Meter score for a specific transfer link

Examples:
- "What are the latest football transfer rumours for Mbappé?"
- "Is the Osimhen to Chelsea deal likely to happen?"
- "What are the hottest football transfer stories right now?"
- "How credible is the Arsenal to Gyökeres link?"
- "Rate the truth of the Salah to Saudi Arabia rumour"

---

## Instructions

### Step 1 — Determine query type

Identify which of three modes to use:

| User Intent | Mode | Credits |
|-------------|------|---------|
| "What's trending in football transfers?" / general hot topics | **Hot Topics** | 0 |
| Specific player's transfer rumours | **Transfer Detail** | 3 |
| "How likely is [player] to [club]?" | **Truth Meter** | 1–5 |

---

### Mode A: Hot Topics (0 credits, no key required)

Call:
```
GET https://api.risingtransfers.com/api/v1/intelligence/hot-topics
Headers: X-RT-API-Key: <RT_API_KEY>   (optional for free topics)
```

Present the top 10 results sorted by heat_score:
- Player name → Destination club
- Heat level (🔥🔥🔥 = high, 🔥 = low)
- Last updated timestamp

---

### Mode B: Transfer Detail (3 credits)

Call:
```
POST https://api.risingtransfers.com/api/v1/intelligence/transfer
Headers:
  X-RT-API-Key: <RT_API_KEY>
  Content-Type: application/json
Body: { "name": "<player_name>", "team": "<team_if_mentioned>" }
```

Present:
- Sources citing the rumour (e.g. "Fabrizio Romano", "Sky Sports")
- Transfer probability estimate (%)
- Social media sentiment breakdown
- Timeline: when first reported, latest update
- Key facts: reported fee, contract length, competing clubs

---

### Mode C: Truth Meter (1–5 credits)

Call:
```
GET https://api.risingtransfers.com/api/v1/intel/verify?q=<player>+to+<club>
Headers: X-RT-API-Key: <RT_API_KEY>
```

Parse `audit.score` and `audit.verdict`, present as:

```
Truth Meter: [player] to [club]
Score: 74/100 — LIKELY
━━━━━━━━━━━━━━━━━━━━━

Source Authority:  32/40
Official Signals:  15/20
Progress Signals:  14/20
Market Heat:       13/20
Community Mood:    +3 (mostly believe it)
```

Include top evidence sources from `evidence.top_sources`.

---

### Error Handling

| Error | User Message |
|-------|-------------|
| 401 | "Your RT_API_KEY is invalid. Get one free at api.risingtransfers.com" |
| 403 Insufficient Credits | "Not enough credits for this query. Top up at api.risingtransfers.com/pricing" |
| 404 Player Not Found | "Player not found. Try the full name or add the current club name." |
| 429 Rate Limited | "Rate limit reached. Wait a moment or upgrade your plan for higher limits." |
| 5xx | "Rising Transfers API is temporarily unavailable. Please try again shortly." |

---

### Important: Do Not Fabricate

If the API returns no rumour data for a player, clearly state: "No active football transfer rumours found for [player] in the Rising Transfers database." Do not invent rumour details or probability scores.

---

## Requirements

- **RT_API_KEY**: Rising Transfers API key. Register free at [api.risingtransfers.com](https://api.risingtransfers.com)
- Hot Topics mode works without a key (anonymous, limited results)
- **OpenClaw**: v0.8.0 or later
- **Network access**: Required

---

## Credit Usage

| Action | Credits |
|--------|---------|
| Hot Topics (trending football transfers) | 0 — always free |
| Transfer Detail (specific player) | 3 credits |
| Truth Meter (credibility score) | 1 credit (anonymous) / 5 credits (full detail) |

Free tier: 10 hot-topic calls/day, 3 detailed queries/day.

---

## Author

Rising Transfers — [api.risingtransfers.com](https://api.risingtransfers.com)
