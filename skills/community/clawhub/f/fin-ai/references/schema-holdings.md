# Holdings Schema

## Purpose

Preserve the retained V2 holdings schema as the authoritative input shape.

## Top-level keys

- `date`
- `updated_at` (optional in phase 1)
- `groups`

## Group keys

- `cost_basis`
- `positions`
- `fund`
- `cash`

## Position keys

- `name`
- `ticker`
- `quantity`
- `cost_price`

## Phase-1 retained minimum

Top-level:
- `date`
- `groups`

Per-group:
- `positions`
- `cash`
- `cost_basis`
- `fund`

Per-position:
- `ticker`
- `quantity`
- `cost_price`
- `name`

## Validation posture

Required:
- `date`
- `groups`
- each group must have `positions`
- each position must have `ticker`
- each position must have numeric `quantity`

Allowed defaults:
- missing `cash` -> `0`
- missing `fund` -> `0`
- missing `cost_basis` -> `0`
- missing `cost_price` -> `0` with warning
- missing `name` -> empty or derived placeholder with warning

## Truth rule

This schema is the authoritative source of truth. Downstream analysis must be recomputable from holdings plus market/FX context.

## 推荐同步语义

- 默认使用 `replace_groups`
  适合用户说“更新某个账户”“替换今天某个组的持仓”
- 只有在用户明确想“整份覆盖今天持仓”时才使用 `overwrite_all`
