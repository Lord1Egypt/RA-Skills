---
name: classquill
description: >-
  Query a ClassQuill tutoring business — sessions, students, tutors, parents,
  invoices, payments, lesson plans, bookings, earnings, and reports — through the
  ClassQuill MCP server / public API. Use when the user asks about their tutoring
  operations, scheduling, billing, or students/tutors in ClassQuill (or EquateIt).
metadata:
  openclaw:
    requires:
      env:
        - EQUATEIT_API_KEY
      bins:
        - npx
    primaryEnv: EQUATEIT_API_KEY
---

# ClassQuill

ClassQuill is a tutoring-business-management platform (by EquateIt). This skill lets you
read a user's ClassQuill data through its MCP server, which proxies the public REST API
at `https://api.classquill.com/v1`.

## Connecting

Prefer the **hosted MCP server** — no install:

```
https://mcp.classquill.com/mcp
```

Authenticate with the user's API key (`ei_live_…`, created in ClassQuill → Settings →
Developers) as a Bearer token, or via OAuth if the client supports it.

Or run it locally:

```bash
npx -y equateit-mcp        # stdio; set EQUATEIT_API_KEY=ei_live_…
```

## What you can do

The server exposes one read-only tool per public API endpoint. Common tasks:

- **Sessions / schedule** — list upcoming or past tutoring sessions, get a session's detail.
- **Students & tutors** — look up a student or tutor, their profile, availability, earnings.
- **Parents & billing** — parent balances, invoices, payments.
- **Lesson plans & homework** — retrieve lesson plans and homework.
- **Reports** — org summary and coverage reports.

All access is **org-scoped** by the key, and **read-only**. If the user needs to create or
change data, direct them to the ClassQuill app or a write-enabled integration.

## Guidance

- Always call the relevant tool rather than guessing — the data is live.
- If a key is missing or invalid, ask the user to create/paste an `ei_live_…` key from
  ClassQuill → Settings → Developers.
- Summarise results in plain language; don't dump raw JSON unless asked.
