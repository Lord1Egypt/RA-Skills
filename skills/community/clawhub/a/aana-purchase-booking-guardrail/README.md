# AANA Purchase Booking Guardrail Skill

This OpenClaw-style skill helps agents gate purchases, bookings, reservations, subscriptions, renewals, and irreversible financial actions.

## Marketplace Slug

Recommended slug:

```text
aana-purchase-booking-guardrail
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/purchase-booking-review.schema.json`: optional review-payload shape.
- `examples/redacted-purchase-booking-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Separate browsing or drafting from financially binding actions.
2. Verify exact item, vendor, date, quantity, price, fees, currency, refundability, cancellation terms, and renewal behavior.
3. Require explicit user approval before charges, bookings, reservations, subscriptions, renewals, deposits, bids, donations, or transfers.
4. Avoid unapproved add-ons, upsells, warranties, tips, insurance, or recurring terms.
5. Minimize payment, identity, and reservation data in review payloads and replies.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect accounts by itself,
- place orders, bookings, or subscriptions by itself.

## Safety Model

Use redacted summaries for review payloads. Do not include full payment numbers, bank details, security codes, identity documents, raw receipts, full reservation codes, credentials, or unrelated purchase history.

High-value, non-refundable, recurring, legally binding, third-party, or unclear financial actions should require explicit user approval or human review.
