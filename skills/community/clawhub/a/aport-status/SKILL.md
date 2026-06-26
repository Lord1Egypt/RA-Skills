---
name: aport-status
description: >
  Show your current APort passport status — capabilities, deliverable
  contract, pending tasks, and recent decisions. Like `git status` for
  your agent's identity and accountability state.
license: Apache-2.0
compatibility: Any AI agent or coding assistant with HTTP access
metadata:
  author: uchibeke
  version: 1.0.0
  tags: ai-agent, status, passport, aport, accountability, identity
---

# /aport-status — Your Agent's Current State

Shows your passport, what you're allowed to do, what your deliverable
contract requires, and the state of any tasks you've started.
Run this any time you want to understand your own standing.

## When to use this skill

- At the start of a session to orient yourself
- When a user asks "what can you do?" or "what are your limits?"
- Before attempting an action to check you have the capability
- When debugging why a task completion was denied
- To show a user your verified identity and capabilities

## Prerequisites

You need `APORT_AGENT_ID` in your environment.

If you don't have a passport yet, create one first:
- **Web:** https://aport.id
- **CLI:** `npx aport-id`
- **Agent skill:** Read https://aport.id/skill and follow the instructions

## Step 1 — Fetch your passport

By agent_id (from APort API):
```
GET https://aport.io/api/passports/YOUR_AGENT_ID
```

By slug (from aport.id proxy):
```
GET https://aport.id/api/passport/YOUR_SLUG
```

## Step 2 — Fetch recent activity

```
GET https://aport.io/api/verify/decisions/YOUR_AGENT_ID
```

## Step 3 — Display status

Format the output clearly:

```
APORT STATUS — [AGENT NAME]
Passport: https://aport.id/passport/YOUR_SLUG
Status:   ACTIVE  (or SUSPENDED / REVOKED)
Assurance: L0  (or L1 / L2 / L3 / L4KYC / L4FIN)
Regions:   global

IDENTITY
  ID:      ap_a2d10232...
  Role:    agent
  Model:   Claude Sonnet (Labrador)
  Owner:   claimed  (or unclaimed — check email)
  Born:    March 13, 2026

CAPABILITIES  (what I can do)
  data.file.read
  data.file.write
  web.fetch
  repo.merge
  deliverable.task.complete

DELIVERABLE CONTRACT  (what I must produce)
  Written summary required  (min. 20 words)
  Tests passing required: no
  Different reviewer required: no
  Output scanned for: TODO, FIXME, console.log

  Acceptance criteria:
  - A concrete output artifact must be produced
  - No placeholder text in output

RECENT DECISIONS  (recent)
  ALLOW  [decision_id]  — 09:14  — deliverable.task.complete.v1
  ALLOW  [decision_id]  — 11:30  — deliverable.task.complete.v1
  DENY   [decision_id]  — 14:05  — oap.tests_not_passing  (retry pending)

PASSPORT URL
  https://aport.id/passport/YOUR_SLUG
```

## Step 4 — Surface any issues

After displaying status, flag any conditions requiring attention:

**If passport is SUSPENDED:**
```
Your passport is suspended. You cannot complete tasks or use
restricted capabilities. Contact APort at https://aport.io
```

**If passport is unclaimed:**
```
Your passport has not been claimed yet. Check the email sent
to [owner email] for the claim link.
```

**If tasks are repeatedly DENIED:**
```
[decision_id] has been denied 3 times (oap.tests_not_passing).
This likely needs human attention — tests are not passing.
```

**If assurance level is L0 and a capability requires higher:**
```
Some capabilities require higher assurance (L2+).
Upgrade your assurance at https://aport.io/assurance
```

## Step 5 — Answer capability questions

If a user asks "can you do X?", use the status to answer directly:

```
User: Can you merge this PR?
You:  [check capabilities list for repo.merge]
      Yes — repo.merge is in my passport
      Before I can call it done, I need: [deliverable contract requirements]

User: Can you send an email?
You:  [check capabilities list for messaging.send]
      No — messaging.send is not in my passport
      To add it, create a new passport at https://aport.id
```

## Compact mode

If the user wants a shorter output, show compact status:

```
[AGENT NAME] — ACTIVE — ap_a2d1...425c
Caps: data.file.write, web.fetch, repo.merge, deliverable.task.complete
Contract: summary(20w), scan(TODO,FIXME), criteria(2)
Recent: 2 ALLOW, 1 DENY (tests_not_passing)
```

## Links

- Create a passport: https://aport.id (web) or `npx aport-id` (CLI) or https://aport.id/skill (agent)
- Your passport page: https://aport.id/passport/YOUR_SLUG
- Your decisions: GET https://aport.io/api/verify/decisions/YOUR_AGENT_ID
- APort dashboard: https://aport.io/dashboard
