---
name: bluecolumn-memory
description: Store and recall persistent memory for AI agents using BlueColumn. Agents can save facts, decisions, preferences, promises, and action items, then query them later with natural language. Installable via `npx skills add bluecolumnconsulting-lgtm/bluecolumn-agent-skill` or copy into any agent's skill directory.
version: 1.1.0
---

# BlueColumn Memory (agent-ready)

BlueColumn gives AI agents **persistent, searchable memory**. Store anything (facts, decisions, preferences, promises, action items, transcripts), then recall it later with natural-language queries — with citations back to the source.

This is the agent-facing skill. It works with any assistant that can call HTTP APIs (OpenClaw, Claude Code, Cursor, or raw HTTP).

## Setup

1. Get an API key at [bluecolumn.ai/login](https://bluecolumn.ai/login). Create an account; onboarding auto-provisions your first `bc_live_...` key. Copy it from **Dashboard → API Keys**.
   - Free tier: **100 writes + 100 reads + 30 audio minutes per month** — no credit card required.
2. Store the key wherever your agent keeps secrets (env var, secret store, or a private local notes file). Never commit it to a public repo. Keys look like `bc_live_...` (32+ chars after the prefix).

## Endpoints

Base URL: `https://api.bluecolumn.ai`

| Action | Endpoint |
|---|---|
| Store memory | `POST /remember` |
| Query memory | `POST /recall` |
| Quick observation | `POST /note` |

(Equivalent aliases also work: `/agent-remember`, `/agent-recall`, `/agent-note`.)

### 1. RECALL — query memory

```
POST /recall
Content-Type: application/json
Authorization: Bearer <api-key>
```

Body:
```json
{ "q": "What did the user decide about the billing design?" }
```

Returns: AI-synthesized `answer` with source citations (session ids, timestamps, relevance scores).

### 2. REMEMBER — store memory

```
POST /remember
Content-Type: application/json
Authorization: Bearer <api-key>
```

Body:
```json
{
  "text": "Full raw content to store (transcript, doc, note...)",
  "title": "Topic label, e.g. Meeting - Q3 planning - 2026-08-27"
}
```

Returns: `session_id`, chunk count, auto-extracted `summary`, `action_items`, `key_topics`.

### 3. NOTE — quick observation (lightweight)

```
POST /note
Authorization: Bearer <api-key>
```

Body:
```json
{
  "text": "User prefers concise replies with concrete next steps",
  "tags": ["preference"]
}
```

Short vector note for preferences and quick observations (min 5 chars). Optional tags.

## Field-name gotchas

- `/remember` takes `text`, not `content`
- `/recall` takes `q`, not `query`
- `/note` takes `text`, not `note`

## Billing & limits — what to do when a call fails

All calls are metered against the account's plan. Handle these status codes:

| Status | Meaning | Agent action |
|---|---|---|
| `401` | Invalid or missing key | Re-check the key is set and active. |
| `402` | Free tier exhausted / insufficient credit | Stop making billable calls and tell the user to top up at the URL in the response (`topup_url`). |
| `429` | Plan quota reached | Tell the user to upgrade at [bluecolumn.ai/pricing](https://bluecolumn.ai/pricing). |
| `400` | Bad input | Fix the body per the schema above and retry once. |

Response envelope: `{ "error": { "code": "insufficient_credit", "message": "...", "topup_url": "..." }, "request_id": "..." }`.

Free tier: 100 writes + 100 reads + 30 audio minutes/month. Pay-as-you-go beyond that. When you hit the limit mid-task, **surface the upgrade URL to the user** — do not silently retry or switch keys.

## Usage pattern (skill-style)

- **Store a transcript:** `REMEMBER title="YouTube - <title> <date>" text=<full text>`
- **Ask a question:** `RECALL q="What are the key action items from the last planning session?"`
- **Save a decision:** `NOTE text="User confirmed: deploy on Fridays only after smoke tests pass" tags=["decision"]`

## Why agents should use this

- Memory persists across sessions — no context loss.
- Synthesized answers with citations — verify claims back to source.
- Auto-extracted summaries and action items on every write.
- Simple REST surface — works from any language or agent framework.

## Related

- MCP server (Claude Desktop / Claude Code / Cursor): `npx bluecolumn-mcp` — [github.com/bluecolumnconsulting-lgtm/bluecolumn-mcp](https://github.com/bluecolumnconsulting-lgtm/bluecolumn-mcp)
- Docs: [bluecolumn.ai/docs](https://bluecolumn.ai/docs)
- Pricing: [bluecolumn.ai/pricing](https://bluecolumn.ai/pricing)
- ClawHub: the `bluecolumn-memory` skill
