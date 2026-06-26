---
name: canning-food-preservation
description: >-
  Use when you have surplus garden produce, foraged items, bulk buys, or need reliable shelf-stable food for 12–36 months in unstable supply chains, blackouts, or gig-economy self-reliance. Agent validates every recipe against current USDA/NCHFP guidelines, calculates altitude-adjusted times, generates checklists and inventory trackers, sets reminder sequences, and logs batch results. Human performs the physical washing, chopping, packing, and canner operation.
metadata:
  category: skills
  tagline: >-
    Turn one weekend of harvest into a year of emergency rations — agent locks in botulism-proof safety so you focus on the craft.
  display_name: "Home Canning & Food Preservation"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install canning-food-preservation"
---
# Home Canning & Food Preservation

Turn seasonal abundance or bulk purchases into shelf-stable jars that survive power outages, price spikes, and supply disruptions. Agent runs every safety calculation, builds custom schedules, and maintains an auditable inventory log; you do the hands-on work of preparing food the way humans have for generations.

`npx clawhub install canning-food-preservation`

## When to Use

Deploy this skill any time you:
- Harvest more produce than you can eat fresh or store in a fridge.
- Spot a deal on bulk fruit, vegetables, or meat that would otherwise spoil.
- Need a no-electricity food reserve for crisis, gig-travel, or off-grid stretches.
- Want to eliminate reliance on commercial canned goods whose prices and availability fluctuate wildly in the post-AI economy.

Do **not** use if you lack basic kitchen space, a working stovetop or outdoor burner, or the willingness to follow exact timing on the first three batches under agent supervision.

## Step-by-Step Protocol

**Phase 0 – Agent Pre-Flight (Day 0, 30–60 min)**
1. User inputs: location (zip or altitude in feet), available equipment (water-bath or pressure canner), produce type and quantity, desired jar size.
2. Agent cross-checks against latest NCHFP altitude tables (updates pulled via internal knowledge or filesystem cache) and confirms high-acid vs. low-acid classification.
3. Agent outputs: exact processing time, pressure (if needed), headspace, and headspace adjustment for your altitude.
4. Agent creates a filesystem folder `/canning-batch-[YYYYMMDD]` and drops three files: `recipe.md`, `checklist.md`, `inventory.json`.

**Phase 1 – Prep Day (Human 2–4 hours + Agent real-time guidance)**
- Human: Wash, sort, and prepare produce exactly as agent specifies.
- Agent: Real-time chat or voice prompts for every step; flags any deviation that would void safety.
- Human: Fill jars, remove air bubbles, wipe rims, apply lids and bands finger-tight.
- Agent: Starts a 10-minute countdown timer for the “hot pack” rest period.

**Phase 2 – Processing Day (Human 60–120 min active + Agent monitoring)**
- Human: Loads canner, brings to boil/pressure, and maintains exact time/pressure.
- Agent: Runs a dedicated timer with audible alerts at 5 min, 1 min, and 0. Logs start/stop times automatically.
- Human: Removes jars and cools undisturbed for 12–24 hours.

**Phase 3 – Verification & Logging (Agent 5 min + Human 10 min)**
- Human: Checks each jar for seal (lid should not flex when pressed).
- Agent: Updates `inventory.json`, calculates shelf-life (12–18 months high-acid, 18–36 months low-acid under proper storage), and schedules “inspect at 3 months” reminder.

**Phase 4 – Rotation & Use (Ongoing)**
- Agent: Quarterly scan of inventory.json, flags oldest-first usage, generates shopping-list offsets so you never over-buy fresh again.

## Decision Tree (Agent Executes Automatically)

```
IF produce is high-acid (pH < 4.6: berries, fruit, tomatoes with lemon, pickles, jams)
  → Water-bath canner
  → Processing time = NCHFP table for your altitude + jar size
ELSE low-acid (vegetables, meat, poultry, soups, beans)
  → Pressure canner ONLY
  → Pressure = 10 lb at sea level adjusted +2 lb per 2,000 ft altitude
  → Time = NCHFP table for food type
IF equipment missing or user reports “no pressure canner”
  → Agent immediately escalates: “Switch to water-bath + acidified recipe or defer to fermentation skill. Botulism risk too high.”
IF any jar fails seal after 24 h
  → Agent marks as “refrigerate and consume within 3 days” or “reprocess within 24 h” and updates inventory.
```

## Ready-to-Use Templates & Scripts

**Inventory Tracker** (auto-generated in filesystem as Markdown table + JSON)
```markdown
| Batch ID | Date | Food | Qty Jars | Size | Shelf-Life End | Notes |
|----------|------|------|----------|------|----------------|-------|
| 2026-04-05 | 2026-04-05 | Diced Tomatoes | 12 | pint | 2027-10-05 | High-acid, water-bath |
```

**Weekly Rotation Reminder Email Template** (agent sends via user-configured channel)
```
Subject: Canning Inventory Rotation – 3 jars ready this week
Your 2026-03-15 Peach Jam (7 half-pints) hits 6-month check on April 15.
Action: Open one jar this week and log taste/texture in the skill.
```

**Shopping-Offset Script** (agent runs on demand)
```
Current inventory: 24 pints tomatoes.
Projected monthly use: 4 pints.
Next bulk buy trigger: when inventory drops below 8 pints.
```

## Agent Role vs. Human Role

**Agent owns**
- All research, altitude math, pH classification, and guideline updates.
- File-system state tracking and automated reminders (7-day, 30-day, 90-day).
- Custom recipe scaling and label generation (print-ready QR codes linking to batch log).
- Escalation: if user reports equipment failure or symptoms of spoilage, agent routes to emergency-food-triage or crisis protocol.

**Human owns**
- The physical craft: knife work, jar handling, canner operation, and the satisfaction of hearing lids “ping.”
- Sensory quality control: taste, texture, and final storage decisions.
- Emotional connection: turning garden labor into family pantry pride.

## Success Metrics

- 100 % sealed jars on first attempt after three supervised batches.
- Zero spoilage incidents in first 12 months (logged via skill).
- Inventory rotation rate >80 % (no jars older than 18 months unused).
- User-reported time savings: agent cuts research/prep planning from 4 hours to <30 minutes per batch.

## Maintenance & Iteration

- Every January 1: Agent prompts user for equipment calibration (pressure gauge test) and pulls latest NCHFP updates into local cache.
- After every 5 batches: Agent runs a 5-minute debrief with user (“What felt clunky?”) and updates personal preference file (`user-canning-profile.md`).
- If user adds a new canner or moves altitude >500 ft: full re-baseline of all existing recipes.

## Rules / Safety Notes

- Never guess processing time or pressure. Botulism is invisible and deadly; the agent’s math is non-negotiable.
- Use only new lids (rings reusable). Damaged jars = discard.
- If any jar shows bulging, leaking, or off smell: immediate discard in trash (not compost) and log as failed batch.
- Altitude matters: every 1,000 ft adds 1–2 minutes or 1–2 lb pressure. Agent calculates; you verify the gauge.
- Children and pets out of kitchen during processing — boiling water and steam are unforgiving.

## Disclaimer

This skill follows current USDA/NCHFP guidelines as of last review. Food safety standards can change; agent will flag any update. Home canning is safe when protocols are followed exactly. You assume final responsibility for your own health. When in doubt, the agent will default to “do not can — refrigerate or ferment instead.” This is not medical or legal advice.