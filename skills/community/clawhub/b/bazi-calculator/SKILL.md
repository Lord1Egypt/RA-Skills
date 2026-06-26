---
name: bazi-calculator
description: Calculate a person’s Four Pillars (BaZi / Eight Characters) from birth date and time using sexagenary-cycle offsets from one trusted reference datetime that already has known year/month/day/hour pillars. Also calculate DaYun (10-year luck cycles) when gender is provided, and include the current LiuNian (流年) Ganzhi. Use when user asks for BaZi pillars, eight characters, stem-branch pillar calculation, DaYun, or current LiuNian.
---

# BaZi Calculator

Calculate Year/Month/Day/Hour pillars with a **single reference point**.

## Quick Start

1. Use `references/reference-verified.json` (or your own verified reference JSON) with one trusted reference datetime and its four pillars.
2. Run:

```bash
python3 scripts/calc_bazi.py \
  --birth "1992-08-14 21:35" \
  --tz "Asia/Shanghai" \
  --reference references/reference-verified.json \
  --gender male
```

3. Return results left-to-right as:
- Hour pillar
- Day pillar
- Month pillar
- Year pillar
- Eight characters (Hour Day Month Year)

## Workflow

### 1) Validate inputs
- Require birth datetime (`YYYY-MM-DD HH:MM`).
- Require timezone (default `Asia/Shanghai` if omitted).
- Require one reference JSON with:
  - `reference_datetime`
  - `reference_pillars.year/month/day/hour`

### 2) Compute offsets from reference
- Year offset: LiChun-adjusted year difference (approximation: Feb-04 00:00 local).
- Month offset: calendar month difference.
- Day offset: calendar day difference.
- Hour offset: 2-hour bin difference (Zi starts at 23:00).

### 3) Shift each base pillar in 60-cycle
- `target_pillar = shift(reference_pillar, offset mod 60)` for year/month/day/hour separately.

### 4) Present output

```text
Birth (local): 1992-08-14 21:35 (Asia/Shanghai)
Hour Pillar: 丙戌
Day Pillar: 癸亥
Month Pillar: 丙申
Year Pillar: 壬申
Eight Characters (L→R Hour/Day/Month/Year): 丙戌 癸亥 丙申 壬申
```

## Notes
- This is a deterministic reference-based method.
- Accuracy depends on correctness of the chosen reference and boundary rules.
- For professional-grade astrology, validate solar-term boundaries and true solar time adjustments.
