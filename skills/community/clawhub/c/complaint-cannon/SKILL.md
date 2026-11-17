---
name: complaint-cannon
description: "Use when a company wronged you and the support chat is going nowhere — builds escalation-aware complaint letters from incident timelines, with the three leverage multipliers consumers never use: regulator escalation ladders (who actually fears which regulator per industry and country), statutory refund rights (consumer protection timelines that turn 'policy' into 'law'), and public-review detonation sequencing (when a CEO email or review-site blast is optimal vs premature). Tracks each complaint as a case with a follow-up cadence so claims die of neglect never."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [complaints, consumer-rights, escalation, refunds, regulators, advocacy]
---

# Complaint Cannon — Escalation-Aware Complaint Engine

## Overview

Most consumer complaints fail for structural reasons, not factual ones:

1. **No paper trail** — the story lives in chat scrolls and phone calls; when it reaches someone with authority, there's nothing to review.
2. **Wrong audience** — complaints escalate horizontally (more agents) instead of vertically (supervisors, executives, regulators).
3. **Leverage unused** — companies weigh complaints by *feared consequence*. Naming the actual regulator for the actual industry, citing the actual statute with a deadline, and sequencing public review pressure are the three multipliers, and almost nobody uses them.

This skill builds complaints as **cases** with escalation-aware letters:

1. **Incident timeline** — dated facts, money amounts, evidence references. The spine every letter cites.
2. **Letter generator** — complaint, escalation, final-notice-before-action, each citing the timeline, with tone control (firm-but-professional; rage loses).
3. **Regulator router** — per industry and country: which regulator/bodies actually act (telecom → FCC/ofcom-equivalents, airlines → DOT/EU261, banking → CFPB-equivalents...), with the escalation ladder in the right order.
4. **Statutory overlays** — common consumer-protection timelines (EU 14-day withdrawal, US FCBA billing dispute windows, airline compensation deadlines) that convert "our policy" into "the law".
5. **Detonation sequencing** — when the CEO email, the review-site blast, and the regulator filing are each *optimal*: too early reads as unhinged and burns the escalation path; too late means the refund window closed.
6. **Case tracking** — every contact logged; follow-up cadence (never let a claim die of neglect — silence is a company strategy).

## When to Use

- A refund/replacement/repair is owed and support is stalling ("we'll get back to you", chat loops, dead timelines)
- Damaged delivery, billing error, unauthorized charge, service failure with documented loss
- You're about to write an angry email — don't; generate an escalation-aware one instead
- Post-filing tracking: what's due when, what to send next, when to escalate a rung
- Don't use for: employment disputes, landlord-tenant court process (different regimes), personal injury, or anything where a lawyer should act first.

## How It Works

1. **Open a case** — `case add "Delta broken TV"` with the company, industry, amount at stake, country.
2. **Log the timeline** — `event add` per dated incident: what happened, evidence file refs (photos, order numbers, chat logs).
3. **Generate letters** — `letter complaint` → `letter escalate` → `letter final`; each cites the full timeline and states a specific remedy + deadline.
4. **Route leverage** — `regulators` prints the ladder for the case's industry+country with what each body fears; `letter regulator` drafts the filing.
5. **Sequence detonation** — `plan` prints the escalation timeline: when CEO-email, public reviews, and regulator filing are each optimal given days-since-first-contact and response history.
6. **Track** — `contact add` logs each interaction (channel, person, response); `due` shows follow-ups owed today; `status` summarizes the case.

## Commands

```bash
# Case + timeline
python3 scripts/complaint.py case add "Broken TV delivery" \
    --company "ElectroMart" --industry retail --amount 649 --country US
python3 scripts/complaint.py event add C001 --date 2026-09-10 \
    --text "TV delivered with cracked screen (photo IMG_2231)"
python3 scripts/complaint.py event add C001 --date 2026-09-12 \
    --text "Support chat: 'not our fault, carrier issue' (chat log saved)"

# Letters (each cites the timeline; tone: firm, factual)
python3 scripts/complaint.py letter complaint C001
python3 scripts/complaint.py letter escalate C001
python3 scripts/complaint.py letter final C001

# Leverage
python3 scripts/complaint.py regulators C001
python3 scripts/complaint.py letter regulator C001

# Sequencing + tracking
python3 scripts/complaint.py plan C001
python3 scripts/complaint.py contact add C001 --date 2026-09-13 --channel chat \
    --person "agent 4412" --result "promised callback in 48h (never came)"
python3 scripts/complaint.py due
python3 scripts/complaint.py status C001
```

Storage: `complaints.json` in cwd. 100% local.

## The Escalation Ladder (what `plan` enforces)

| Rung | Action | Timing |
|---|---|---|
| 1 | Formal complaint letter (written trail starts) | day 0 |
| 2 | Escalation letter (supervisor/exec email) | +7 days silent or refused |
| 3 | Final notice before external action | +14 days |
| 4 | Regulator filing + review-site post + CEO email | +21 days, sequenced together |

A substantive company response resets the clock for its promised action only. Two broken promises = skip to rung 4 (the plan recomputes automatically).

## Common Pitfalls

1. **Raging.** Anger signals low escalation risk. The letters are deliberately factual: dates, amounts, remedy, deadline. Rage loses; records win.
2. **Chat-only contact.** Support chats are designed to dissipate. The first letter converts the scroll into a reviewable document — send it early.
3. **Escalating to regulators prematurely.** A regulator filing before the company had a written chance reads as bad faith and can get your case bounced. The ladder exists for a reason: rung 3's final notice is what makes rung 4 land.
4. **Vague remedies.** "Make this right" is not a remedy. Each letter states the exact amount/action and a specific deadline (default 14 days).
5. **No deadlines on yourself.** Statutory windows (chargebacks, EU withdrawal, airline claims) expire. `plan` surfaces the applicable windows; if a chargeback window is inside 30 days, it says so loudly.

## Verification Checklist

- [ ] Case opened with company/industry/amount/country
- [ ] Every incident logged as a dated event with evidence refs
- [ ] Complaint letter sent (rung 1) — written trail started
- [ ] Follow-up cadence active (`due` clean on every check)
- [ ] Escalation ladder timing respected (no premature regulator filing)
- [ ] Statutory windows checked against `plan` output
- [ ] Each contact logged with channel/person/result
- [ ] Case closed with outcome recorded — patterns across cases are leverage too
