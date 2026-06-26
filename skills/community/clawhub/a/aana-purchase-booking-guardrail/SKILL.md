# AANA Purchase Booking Guardrail Skill

Use this skill when an OpenClaw-style agent may purchase, book, reserve, subscribe, renew, upgrade, downgrade, cancel, refund, bid, donate, transfer funds, or take any irreversible or financially binding action.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Financial commitment actions should happen only after the agent verifies the exact item, vendor, price, fees, dates, cancellation terms, payment method, user authorization, and reversibility.

The agent should separate:

- browsing or comparing options,
- drafting a plan or cart,
- filling forms without submitting,
- reversible holds or saved drafts,
- actions that create charges, subscriptions, reservations, renewals, deposits, penalties, or legal/financial commitments,
- payment or identity data that must be minimized or redacted.

## When To Use

Use this skill before:

- buying products, services, tickets, memberships, gift cards, domains, software, or subscriptions,
- booking travel, hotels, rentals, appointments, restaurants, events, or services,
- reserving inventory or placing deposits,
- renewing, upgrading, downgrading, or cancelling subscriptions,
- accepting fees, penalties, cancellation terms, auto-renewal terms, or non-refundable terms,
- submitting payment, billing, shipping, identity, loyalty, or account information,
- confirming a purchase order, invoice, donation, bid, transfer, or refund request.

## Financial Risk Classes

Treat these as higher risk:

- non-refundable purchases, deposits, cancellation penalties, auto-renewals, trials that convert to paid plans,
- travel dates, event dates, hotel check-in/check-out, appointment times, time zones, party size, and identity details,
- recurring subscriptions, annual contracts, seat counts, usage-based billing, overdraft risk, installment plans, and financing,
- high-value items, limited inventory, resale tickets, third-party sellers, warranty terms, taxes, shipping, import duties, service fees,
- payment methods, card details, bank details, billing address, account identifiers, loyalty numbers, and private purchase history,
- purchases or bookings for someone else.

## AANA Commitment Gate

1. Identify the action: browse, compare, draft, hold, purchase, book, reserve, subscribe, renew, cancel, refund, bid, donate, or transfer.
2. Identify the commitment: one-time charge, recurring charge, deposit, cancellation penalty, reservation, contract, or irreversible submission.
3. Verify key facts: item/service, vendor, quantity, date/time, location, total cost, taxes, fees, currency, refundability, cancellation terms, and renewal terms.
4. Check authorization: confirm the user explicitly approved this exact action and cost.
5. Check payment privacy: do not expose full payment numbers, bank details, credentials, or unnecessary account data.
6. Check reversibility: prefer cart, quote, draft, hold, or review screen before final submission.
7. Check scope: do not add extras, warranties, insurance, upsells, tips, donations, seats, bags, or subscriptions without approval.
8. Choose action: accept, revise, ask, defer, refuse, or route to human review.

## Required Pre-Flight Checks

Before a financially binding action, verify:

- exact item, service, reservation, or subscription,
- vendor or merchant,
- recipient or traveler/customer identity when relevant,
- date, time, location, time zone, and duration when relevant,
- quantity, seat count, tier, plan, add-ons, and renewal behavior,
- total price including taxes, fees, shipping, deposits, tips, and currency,
- refund, cancellation, return, trial, and auto-renewal terms,
- payment method to use without exposing full sensitive details,
- whether the action is reversible after submission,
- explicit user approval for the final action.

## Explicit Approval Rule

Ask for explicit approval before final submission when an action may charge money, create a recurring commitment, reserve scarce inventory, expose payment details, or become hard to undo.

Approval should include the exact commitment:

```text
Please confirm: book 1 refundable hotel room at the listed property for May 8-10, total $412.30 including taxes and fees, using the card ending in 1234.
```

Do not treat broad intent as final approval. "Find me a hotel" is not approval to book. "This one looks good" is not approval to pay. "Renew it" still requires plan, price, term, renewal date, and payment method confirmation.

## Purchase And Booking Overclaim Rules

Do not claim:

- an item was purchased,
- a booking was confirmed,
- a refund was issued,
- a subscription was cancelled or renewed,
- a price is guaranteed,
- a reservation is refundable,
- a fee will not apply,
- a vendor will honor an exception,
- inventory will remain available,

unless the agent has verified evidence from an approved system or the user-provided confirmation.

## Private Payment Data Rules

Minimize or remove:

- full card numbers, bank numbers, security codes, auth codes, passwords,
- billing address, shipping address, loyalty numbers, account IDs,
- purchase history, invoices, receipts, reservation codes, confirmation numbers,
- identity documents, passport numbers, date of birth, travel companions, and private messages.

Prefer:

- "card ending in 1234" instead of full card number,
- "saved payment method" instead of raw payment details,
- "confirmation code redacted" instead of the full code,
- "billing address on file" instead of repeating the address.

## Safer Alternatives

Prefer:

- compare options before choosing,
- prepare a cart without checking out,
- hold or reserve only when the terms are clear,
- ask the user to complete payment directly,
- use a review screen before final confirmation,
- save a draft rather than submit,
- defer high-value, ambiguous, or third-party purchases to human review.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `task_summary`
- `action_type`
- `commitment_type`
- `amount_summary`
- `terms_status`
- `authorization_status`
- `payment_privacy_status`
- `reversibility_status`
- `recommended_action`

Do not include full payment details, bank details, credentials, identity documents, raw receipts, full reservation codes, private messages, or unrelated account records when a redacted summary is enough.

## Decision Rule

- If the action is non-binding browsing, comparing, or drafting, accept with ordinary care.
- If final commitment facts are incomplete, ask.
- If the draft includes unapproved add-ons, recurring terms, fees, or payment details, revise.
- If the action is high-value, non-refundable, legally binding, or for someone else, defer or require explicit approval.
- If the request would expose payment secrets, bypass consent, misrepresent terms, or spend money without approval, refuse and explain briefly.
- If a checker is unavailable or untrusted, use manual purchase and booking review.

## Output Pattern

For purchase-sensitive actions, prefer:

```text
Purchase/booking review:
- Action: ...
- Total cost: ...
- Terms: refundable / non-refundable / recurring / unclear
- Payment privacy: ...
- Reversibility: ...
- Approval: confirmed / needed / unclear
- Decision: accept / revise / ask / defer / refuse
```

Do not include this review block in the user-facing flow unless useful or required before final action.
