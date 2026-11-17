---
name: call-script-coach
description: "Use before any difficult phone call you're anxious about or that has stakes — calling customer service to dispute a fee, negotiating a bill, cold-calling a client, delivering bad news to a vendor, calling a landlord about repairs, insurance disputes, or handling collections calls — builds a branching call script from your situation (goal, leverage, fallback), generates objection→response trees for the specific counter-arguments you'll hear, produces a one-page printable cheat sheet, and includes a practice-drills mode that plays the other side and scores your responses."
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [negotiation, communication, phone-calls, customer-service, billing-disputes, coaching]
---

# Call Script Coach

## Overview

Almost everyone hates difficult phone calls — and hatred costs money. People accept
wrong fees, skip refund disputes, overpay for years, and avoid negotiating because
when the rep says "that's our policy," they have nothing to say. The difference between
a resolved dispute and a capitulation is usually 4 things: knowing your goal, knowing
your leverage, having a response ready for the 2–3 predictable objections, and knowing
when to escalate instead of arguing.

This skill builds a **branching call script** for your specific situation:

1. **Situation intake** — what the call is about, what you want, what you can offer or
   threaten (leverage), what your fallback is.
2. **Scenario library** — 10 pre-built situations (billing dispute, late-fee waiver,
   rate negotiation, service cancellation, landlord repair demand, insurance denial
   pushback, collections response, vendor complaint, salary/raise call, sales cold
   call), each with goals, leverage points, and the objections you will actually hear.
3. **Objection→response trees** — for every "no" the other side can say, a grounded
   response: acknowledge → restate value/leverage → concrete ask.
4. **Cheat sheet** — a printable one-pager: opening line, asks in order, escalation
   path, what NOT to say, notes field.
5. **Practice mode** — the script plays the other side with realistic pushback, scores
   your typed responses against the tree (did you acknowledge? restate leverage? make a
   concrete ask?), and tells you what to tighten.

## When to Use

- Before disputing a charge, fee, or bill increase by phone
- Calling to cancel a service while dodging retention traps
- Negotiating a rate with a provider (internet, phone, insurance, SaaS)
- Demanding a repair from a landlord or contractor
- Responding to a collections call without admitting or paying wrongly
- Any call you're rehearsing in your head for the third time — write it down instead
- Don't use for: emergency calls, legal proceedings (get a lawyer), or HR complaints
  at work (different rules, written trail matters more).

## Commands

```bash
# List pre-built scenarios
python3 scripts/call_coach.py scenarios

# Build a script interactively (prompts for goal/leverage/fallback)
python3 scripts/call_coach.py build --scenario billing-dispute

# Build non-interactively
python3 scripts/call_coach.py build --scenario rate-negotiation \
    --goal "Cut internet bill to $45/mo" \
    --leverage "3 years customer; competitor offers $42" \
    --fallback "Accept $55 with 12mo lock; else cancel"

# Add your own objection responses to the tree before printing
python3 scripts/call_coach.py build --scenario cancellation \
    --objection "You'll lose your loyalty discount" \
    --response "I understand — the total is still higher than my alternative"

# Printable one-pager (also saved to ~/.call-scripts/<name>.txt)
python3 scripts/call_coach.py sheet --scenario billing-dispute --title "ISP $80 overcharge"

# Practice the call — script plays the other side, scores your replies
python3 scripts/call_coach.py practice --scenario billing-dispute

# See the full objection tree for a scenario
python3 scripts/call_coach.py tree --scenario collections
```

## The 5 Rules (baked into every script)

1. **Open with your name + account + one-sentence goal.** Reps triage in the first 15
   seconds; make the issue classifiable.
2. **Ask, then silence.** State the concrete ask ("remove the $80 charge") and stop
   talking. The first person to fill silence usually concedes ground.
3. **"Policy" is a position, not an answer.** Respond: "I understand that's the
   standard policy — and I'm asking what you can do in this case." Reps have
   discretionary ranges they never volunteer.
4. **Escalate on the second no.** "I appreciate your help — please transfer me to
   someone who can approve this." Retention/loyalty desks exist and have bigger limits.
5. **Know your walk-away.** If fallback is "cancel," say it once, calmly, with a date.
   Empty threats train them to ignore you.

## Objection Tree Shape

```
THEIR LINE                      YOUR RESPONSE (pattern)
──────────────────────────────  ─────────────────────────────────────────
"That's our policy"          →  acknowledge → policy ≠ this case → repeat ask
"I can't do that"            →  "can't" or "not allowed"? → ask for who can
"It's already billed"        →  dispute window + billing error rights → ask
"Manager is busy"            →  hold or callback with name + timeframe
"Offer: partial credit"      →  compare vs goal → accept/counter explicitly
"You agreed to terms"        →  terms ≠ this situation → mischarge facts → ask
```

Every response follows **acknowledge → bridge → concrete ask**. Practice mode scores
exactly those three elements.

## Common Pitfalls

1. **Arguing instead of asking.** Venting feels productive; only concrete asks
   ("remove X", "credit Y", "transfer me") move a call. The cheat sheet's ask list
   keeps you on target.
2. **Threatening without a fallback.** If you say "I'll cancel" and won't, you've spent
   your only card. Decide the fallback *before* dialing — it's an intake field.
3. **Accepting the first "no" as final.** Front-line reps have the smallest authority
   by design. Second no → escalate (Rule 4).
4. **Admitting/paying on a collections call.** The collections script's first branch is
   validation-before-payment: never acknowledge the debt or make a partial payment
   before written validation — both can restart statutes of limitations.
5. **Getting angry at the rep.** The person on the phone didn't cause the problem and
   can't fix what they can't classify. Scripts work because they're calm and specific.
6. **No notes during the call.** The cheat sheet has a notes field — write rep name,
   times, promises, and ticket numbers. That's your paper trail if the promise
   evaporates.

## Verification Checklist

- [ ] Scenario chosen (or custom goal/leverage/fallback written out in full sentences)
- [ ] Sheet printed/saved and visible during the call
- [ ] Fallback decided and realistic — would you actually do it?
- [ ] Practice mode run at least once; your responses hit acknowledge+bridge+ask
- [ ] Account number, billing dates, and any confirmation numbers written on the sheet

## One-Shot Recipes

**ISP charged $80 for a "tech visit" that the rep said was free**
```bash
python3 scripts/call_coach.py build --scenario billing-dispute \
    --goal "Remove the $80 tech-visit charge" \
    --leverage "Chat log where rep said visit was free; 3yr customer" \
    --fallback "File FCC + state AG complaint (5 min, free)"
python3 scripts/call_coach.py sheet --scenario billing-dispute --title "ISP $80"
```

**Canceling a gym/app/SaaS subscription with retention pushback**
```bash
python3 scripts/call_coach.py practice --scenario cancellation
```
