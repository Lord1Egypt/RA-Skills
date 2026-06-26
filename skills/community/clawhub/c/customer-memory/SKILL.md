---
name: customer-memory
description: Give AI agents persistent memory of customer interactions, preferences, and history using BlueColumn. Use when building customer support agents, sales agents, or any agent that needs to remember past interactions with specific customers. Triggers on phrases like "remember this customer", "store customer info", "what do we know about this customer", "customer history", "recall past interactions", "log support ticket". Requires a BlueColumn API key (bc_live_*).
---

# Customer Memory Skill

Persistent customer context for support, sales, and success agents backed by BlueColumn.

## Setup
Read `TOOLS.md` for the BlueColumn API key (`bc_live_*`). Keys are generated at bluecolumn.ai/dashboard. Store securely — never log or expose them.

Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1` (BlueColumn's official backend — bluecolumn.ai runs on Supabase Edge Functions)

## Store Customer Interaction

```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -d '{
    "text": "Customer: jane@acme.com. Issue: API rate limiting on Developer plan. Resolved by upgrading to Builder. Prefers email communication. Tech stack: Python + LangChain.",
    "title": "Customer: jane@acme.com - 2026-04-14"
  }'
```

## Store Quick Customer Note

```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -d '{
    "text": "jane@acme.com prefers async email over live chat",
    "tags": ["customer", "jane@acme.com", "preference"]
  }'
```

## Recall Customer History

```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -d '{"q": "what do we know about jane@acme.com and her past issues?"}'
```

## Workflow

**New interaction:**
1. Query customer history first: "what do we know about [customer]?"
2. Use context to personalize response
3. After interaction → store summary via `/agent-remember`
4. Store key preferences via `/agent-note` with customer email tag

**Support ticket:**
1. Recall similar past issues: "have we seen this error before?"
2. Resolve using historical context
3. Log resolution with outcome

## Title Convention
`"Customer: <email> - <YYYY-MM-DD>"`

Use consistent email-based naming so recall queries work accurately across all interactions with the same customer.

## Tags to Use
- Customer email (e.g. `jane@acme.com`)
- `support`, `sales`, `onboarding`
- `resolved`, `pending`, `escalated`
- Plan tier: `free`, `developer`, `builder`, `scale`

See [references/api.md](references/api.md) for full API reference.
