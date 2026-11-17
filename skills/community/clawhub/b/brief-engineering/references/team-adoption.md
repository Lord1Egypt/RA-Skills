# Rolling this out to a team

The brief is per-user by design. Each person runs it under their own delegated auth and
sees only what they already have permission to see. There is no shared service account
and no central deployment step.

That means adoption is additive: one person can start today, and each additional person
costs one install plus a scope confirmation.

## What a teammate does

Three steps, roughly ten minutes.

**1. Install the skill.** From a machine with public egress:

```bash
clawhub --workdir ~/.openclaw/workspace install @<owner>/brief-engineering
```

Where that is unavailable, copy the skill folder into
`~/.openclaw/workspace/skills/brief-engineering/`. It is plain markdown — no binary, no
compilation, no credentials inside it.

**2. Confirm scope once.** Ask for an engineering brief. It discovers candidate services
from Compass ownership and recent work, then asks for confirmation before treating
anything as owned. Confirmed scope is stored at
`memory/engineering-brief/scope.json`.

**3. Schedule it.** Weekday morning, in their own timezone. An on-call engineer might
want it at handoff time instead.

## What the team does once

Register a signal pack. This is the difference between a brief that reports deploys and
one that reports DLQ depth and latency breaches.

A pack is one JSON file naming the team's Splunk index, SignalFlow programs, thresholds,
critical workflows and their expected cadence, and the operational channel allowlist.
The full contract is in `signal-packs.md`.

Register it once and every teammate whose confirmed scope matches gets it
automatically. Nobody copies configuration between machines.

Without a pack, a teammate still gets deployments, ownership, dependencies, migrations
and their own work context. They just do not get team-specific telemetry.

## Why per-user beats a shared dashboard

A shared dashboard shows everyone the same thing, so most of it is irrelevant to any
given reader and the important item is buried. Worse, it has to run as a service
account with union-of-everyone permissions, which is both a security problem and a
reason it can never show private or restricted signals.

Per-user briefs invert this. Results mirror exactly what that person can already see.
An engineer sees their services' latency; their manager sees aggregate reliability
across the team; a PM sees customer and commitment impact. Same collection logic, same
signal pack, different ranking and framing.

It also fails safely. If one person's OAuth lapses, their brief degrades and says so.
Nobody else is affected.

## Personas

Set persona per user, not per team. See `personas.md`.

| Persona | Gets |
| --- | --- |
| Engineer / on-call | latency, errors, SLO burn, DLQ age, stuck workflows, failed deploys, red CI, runbooks |
| Engineering manager | aggregate service and delivery risk, recurring failures, ownership gaps, cross-team blockers, trends |
| PM | customer escalations, adoption, roadmap risk, deadlines, migration commitments, dependencies |

The manager view is aggregate only: no private messages, no individual activity
scoring, no per-person attribution of failures. This is deliberate and should not be
configured away — a brief that scores individuals stops being a health tool and becomes
a surveillance one, and people will route around it.

## A rollout that works

Start with one engineer on one team. Run it for a week and compare against their manual
morning triage. The question is not whether it produces output — it will — but whether
the top item is the one they would have found themselves.

Then register the signal pack and add two or three teammates on the same services. This
is where pack quality gets tested: wrong thresholds produce daily false alarms, and a
missing `criticality: ignore` on a test workflow will flag it forever.

Add the manager next. Their view exercises aggregation and will expose whether service
ownership is actually recorded in Compass, which is often the first real finding.

Only then take it to a second team with different infrastructure. A second pack proves
the contract generalises rather than encoding one team's assumptions.

## What tends to go wrong

**Scope drift.** Someone changes teams and their brief still reports their old
services. Scope is reconfirmed on ownership change; if Compass is stale, the brief is
stale. Fixing Compass ownership fixes both.

**Pack rot.** A threshold set during an incident stays tuned for that incident and
produces noise for a year. Review thresholds when feedback says "irrelevant" repeatedly
on the same signal.

**Treating gaps as failures.** An empty on-call schedule or a missing `platform` field
is a real finding about the team's setup, not a broken brief. These are usually the
most valuable early output, because they are cheap to fix and nobody had noticed.

**Expecting it to act.** It does not deploy, promote, file or send. Every external
action is drafted behind a confirmation step. That is the boundary that makes it safe to
run unattended every morning.

## Cost of adding one person

| Step | Effort |
| --- | --- |
| Install skill | 2 minutes |
| Confirm scope | 5 minutes, once |
| Set schedule | 1 minute |
| Signal pack | Zero if their team already has one |

No infrastructure, no service account, no admin approval, no credential provisioning.
