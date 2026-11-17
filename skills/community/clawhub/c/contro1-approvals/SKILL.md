---
name: contro1-approvals
description: How to ask a human before a sensitive action and how to log every autonomous action, so your work is accountable. Read this before any action that spends money, changes access, deploys, deletes data, sends a message on the user's behalf, or runs code you fetched.
---

# Contro1 approvals and logging

This skill is the **cooperative** half of Contro1 governance. A separate,
out-of-process guardrail already stops your sensitive host commands and waits
for a signed human decision - you cannot run those without it, and nothing here
can loosen it. What this skill adds is quality: giving a reviewer good context
when you do need approval, and leaving a durable record of what you did when
nobody was watching.

Read it before any action that:

- spends money or moves funds
- changes access, credentials, or permissions
- deploys, restarts, or deletes infrastructure or data
- sends a message, email, or post on the user's behalf
- runs code or a script you fetched from the internet
- acts in a session marked production

## When an action needs approval

Do not try to route around the approval. When your action is sensitive, expect
it to pause, and make the reviewer's job easy:

1. State the exact action in one line: the command or operation, the target, and
   the reversible-or-not nature of it.
2. Give the **facts**, not a pitch. What you are about to run, on what, with what
   inputs. A reviewer decides on what is true, not on how convincing you are.
3. Separate your reasoning from the facts. Your rationale is useful, but it is
   context, not evidence, and it never changes the risk of the action.
4. Wait for the decision. If it is denied or times out, stop and tell the user
   plainly what did not happen. Do not retry the same action through a different
   path.

## Log every autonomous action

For work that did **not** need approval - the reads, the drafts, the benign tool
calls you did on your own - leave a record. After each autonomous action, POST a
short audit note to the bridge (set `CONTRO1_BRIDGE_URL` to its address):

```bash
curl -sX POST "$CONTRO1_BRIDGE_URL/agent/audit" \
  -H 'content-type: application/json' \
  -d '{
    "action": "browser.search",
    "summary": "Researched flight options for the Lisbon trip",
    "agent_id": "main",
    "session_key": "whatsapp:+15550001111",
    "observed": { "queries": 3, "sites": ["skyscanner", "google-flights"] },
    "reason": "User asked me to find cheap dates in October",
    "outcome": "success"
  }'
```

If the `contro1` CLI is installed on your host, you can use it directly instead
of curl - `contro1 audit log ...` to record an action, or `contro1 requests
create ...` to ask for a human approval yourself before a sensitive step and
wait for the decision. See https://contro1.com/docs/cli. Either path is fine;
the point is that nothing you do autonomously goes unrecorded.

Guidance:

- One note per meaningful action, not per keystroke. Batch trivial steps.
- `summary` is what the user would want to see later in a timeline.
- `observed` holds facts (what you touched); `reason` holds your intent. Keep
  them separate.
- Set `outcome` to `failure` when the action did not work, so the trail is
  honest.

## What you must not do

- Do not disable, weaken, or edit the approval or exec policy to make your own
  work easier. Policy changes are themselves privileged and reviewed.
- Do not write a new skill for yourself that grants you a way past a guardrail.
  Skill changes go through the human-reviewed Skill Workshop.
- Do not treat a missing reviewer as permission. If no decision can be reached,
  the action does not happen.

Keeping to this makes you trustworthy: the user can hand you the background work
and only be interrupted for the few decisions that truly need them, with a full,
honest record of everything else.
