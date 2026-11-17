---
name: cs-reply-pack
description: Customer-service reply library and auto-reply rule pack — intent classification, emotion de-escalation (LEAP method), objection-handling matrix, escalation red lines. Outputs a JSON rule table you can import into any helpdesk or chatbot.
version: 1.0.0
author: RAY
license: CC-BY-4.0
tags: [customer-support, chatbot, helpdesk, scripts, automation]
pricing:
  free: Free — 3 generic replies/week
  pro: $9/month — industry-custom + objection matrix + de-escalation flow
  annual: $90/year
  pay_per_use: $5 one-time (industry pack)
  enterprise: $99/month (KB integration + escalation rules)
tiers:
  - id: free
    name: Free
    price: Free
    quota: Free — 3 generic replies/week
  - id: pro
    name: Pro Monthly
    price: $9/month — industry-custom + objection matrix + de-escalation flow
    quota: unlimited
  - id: annual
    name: Pro Annual
    price: $90/year
    quota: unlimited
  - id: enterprise
    name: Enterprise
    price: $99/month (KB integration + escalation rules)
    quota: team unlimited
monetization:
  model: freemium_subscription
  currency: USD
  paywall_trigger: free quota exhausted
  trial_days: 7
  free_trial: true
  upgrade_path: Pro Monthly -> Pro Annual -> Enterprise

---
# Customer Service Reply Pack

## What problem it solves

The three deadly sins of support replies: slow, defensive, blame-shifting. This pack hardens "how to answer every message type" into a three-layer structure — **intent → strategy → script** — that human agents copy-paste and bots use as their rule set.

## Core structure

### 1. Intent classification (8 types)
Pre-sale question / price negotiation / shipping chase / logistics status / return & refund / quality complaint / venting / off-topic chit-chat — each maps to a response priority and template set.

### 2. Objection matrix (LEAP method)
- **L (Listen)**: restate the customer's ask before answering — "So you're saying…, correct?"
- **E (Empathize)**: emotion before facts — "Five days of waiting is genuinely frustrating."
- **A (Ask/Act)**: give choices, not essays — "Would a reshipment or a full refund work better for you?"
- **P (Promise)**: every promise carries a deadline — "Tracking number to you by 6 PM today."

### 3. Escalation red lines (always human handoff)
Safety issues, legal threats (regulator complaints / media), journalists, key accounts (annual spend > threshold), refunds beyond authorization — stop templating immediately, hand off with an internal summary attached.

## Deliverables

1. 30 high-frequency scenario scripts (paste-ready)
2. Anger de-escalation flow (4-step cooldown)
3. Review-request and bad-review recovery scripts (compliant — no fake-review inducement)
4. Auto-reply rule table (intent → template → escalate?), JSON importable

## Boundaries

No false promises ("you'll definitely get a refund"), no competitor bashing; refund commitments defer to the merchant's actual policy via placeholders.
