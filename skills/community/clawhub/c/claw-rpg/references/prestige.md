# Prestige System

Reach Lv.999 to trigger prestige and enter the next growth cycle.

## How to Prestige

```bash
node scripts/levelup.mjs --prestige
```

## Effects

| Effect | Details |
|--------|---------|
| Level reset | Returns to Lv.1 — the grind starts over |
| All stats +10% | Permanent bonus, stacks across prestiges |
| XP requirement ×1.5 | Each prestige raises the XP curve |
| New title unlocked | See title table below |

## Title Tiers

| Prestige | Title | Level Range |
|----------|-------|-------------|
| 0 | Little Lobster | Lv.1–999 |
| 1 | Lobster Warrior | Lv.1–999 |
| 2 | Lobster Knight | Lv.1–999 |
| 3 | Lobster Commander | Lv.1–999 |
| 4 | Lobster General | Lv.1–999 |
| 5 | Legendary Lobster | Lv.1–999 |
| 6 | Mythic Lobster | Lv.1–999 |
| 7 | Epic Lobster | Lv.1–999 |
| 8 | Ancient Lobster | Lv.1–999 |
| 9 | Eternal Lobster | Lv.1–999 |
| 10+ | Chaos Lobster | Lv.1–999 |

## Stat Cap After Prestige

Stats have no hard cap after prestige — each prestige adds a permanent +10% multiplier. The dashboard displays stats with a baseline of 20; overflow is rendered as a bonus indicator.

## XP Scaling

```
Prestige 1: base XP × 1.5
Prestige 2: base XP × 2.25  (1.5²)
Prestige n: base XP × 1.5ⁿ
```

The later you get, the harder the grind — a true long-term growth system.

## Does Class Reset?

**No.** Class is always derived from current stats. After prestige, all stats increase proportionally, so the class usually stays the same — unless the boost tips the balance, triggering a re-evaluation.

## Arena Rank by Prestige

Prestige count serves as the arena "division":

| Prestige | Arena Rank |
|----------|-----------|
| 0 | Bronze Lobster |
| 1–3 | Silver Lobster |
| 4–6 | Gold Lobster |
| 7–9 | Diamond Lobster |
| 10+ | Chaos Lobster (highest) |
