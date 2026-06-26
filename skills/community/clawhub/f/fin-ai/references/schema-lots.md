# Lot Ledger Schema

## Purpose

Preserve the V2 lot ledger shape for later FIFO-aware and lot-aware workflows without forcing it into the phase-1 minimum loop.

## Top-level keys

- `version`
- `updated_at`
- `accounts`
- `notes`

## Account keys

- `method`
- `lots`

## Lot keys

- `lot_id`
- `open_date`
- `quantity`
- `cost_price`
- `source`

## Phase-1 retained minimum

Top-level:
- `accounts`

Per-account:
- `method`
- `lots`

Per-lot:
- `lot_id`
- `open_date`
- `quantity`
- `cost_price`
- `source`

## Phase-1 rule

Lot detail should be preserved when available, but imperfect lot data should not block authoritative holdings sync unless the workflow explicitly depends on lot detail.
