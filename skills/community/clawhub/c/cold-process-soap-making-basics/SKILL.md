---
name: cold-process-soap-making-basics
description: >-
  Use when store-bought soap becomes unreliable, expensive, or you need fully customizable, skin-safe bars made from local fats, oils, and lye for daily hygiene, laundry, or trade goods. Agent calculates precise saponification ratios, safety dilutions, and batch recipes from your exact ingredient list; tracks curing timelines with automated reminders and logs; generates quality-test checklists and barter templates. Human performs every physical step — mixing to trace, pouring, unmolding, cutting, and curing — rebuilding tactile self-reliance.
metadata:
  category: skills
  tagline: >-
    Turn kitchen grease and wood-ash lye into long-lasting, custom soap bars that clean without plastic packaging — agent owns the chemistry so you stay in the stirring and curing.
  display_name: "Cold Process Soap Making Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install cold-process-soap-making-basics"
---
# Cold Process Soap Making Basics

Turn animal fats, plant oils, and lye into custom, long-lasting bars that clean skin, dishes, and laundry without supply-chain dependence. No fancy equipment — just a pot, scale, and your hands. The agent owns every dangerous calculation, recipe scaling, and safety protocol; you own the physical craft that turns waste fat into usable goods.

`npx clawhub install cold-process-soap-making-basics`

## When to Use

Deploy this skill when:
- Commercial soap prices spike or shelves empty.
- You want zero-plastic, zero-fragrance bars tailored to your skin type or local water hardness.
- You have excess animal fat, used cooking oil, or access to hardwood ash and need tradable hygiene items.
- Grid-down or gig-economy hygiene becomes a daily variable you refuse to outsource.
- You want a repeatable micro-business or barter product (one 12-bar batch can trade for weeks of labor).

**Do not use** if you lack a digital scale accurate to 0.1 g or cannot source food-grade lye (sodium hydroxide). Agent will flag this immediately and pivot to ash-based historical recipes only as last resort.

## Agent Role vs. Human Role (Clear Division of Labor)

**Agent owns:**
- All recipe math: saponification values, lye discount (5–8 %), superfat percentage, water:lye ratio.
- Ingredient substitution research and safety data sheets.
- Batch scaling, trace-time estimation, and gel-phase prediction.
- Automated curing calendar, photo-request checkpoints, and pH-test logging.
- Barter templates, inventory cards, and escalation if batch fails zap test.
- Full safety protocol enforcement (PPE list, neutralization steps).

**Human owns:**
- All physical handling: weighing fats/oils, melting, lye solution mixing, stirring to trace, pouring into molds, unmolding, cutting, curing.
- Sensory judgment of trace consistency and final bar hardness.
- Manual curing-room monitoring and final use-testing.

## Step-by-Step Protocol (28-Day First Batch Cycle)

### Phase 0: Ingredient Audit & Recipe Generation (Agent-led, 1 day)
1. Agent asks for exact inventory: fats/oils (types + weights available), lye source, distilled water.
2. Agent runs full SoapCalc-style analysis (or equivalent open-source formulas) and outputs one ready-to-make recipe for a 1 kg batch.
3. Agent generates PPE checklist and emergency neutralization protocol (vinegar + water).

### Phase 1: Fat & Oil Prep (Human 45 min + Agent tracking, Day 1)
- Human renders or measures fats; agent provides exact melting temperature targets.
- Agent requests photo of clear, debris-free liquid oils/fats.

### Phase 2: Lye Solution & Mixing (Human 30–45 min, Day 1)
- Agent supplies exact lye weight, water weight, and temperature safety window (lye solution ≤ 50 °C before blending).
- Human mixes lye into water (never reverse) outdoors or under vent; agent issues timed cool-down alerts.
- Human blends oils + lye at trace; agent times stir sessions (hand or stick blender) and prompts “light trace” photo checks every 5 minutes.

### Phase 3: Pouring & Molding (Human 15 min, Day 1)
Agent supplies three mold options: silicone loaf, Pringles-can tubes, or cardboard lined with parchment.
Human pours, taps out bubbles, and insulates for gel phase if desired. Agent sets 24-hour “do not disturb” timer.

### Phase 4: Unmolding & Cutting (Human 30 min, Day 2)
- Agent confirms 24–48 hour wait based on local temperature.
- Human unmolds and cuts into bars; agent provides exact cut dimensions for even curing and weight.
- Agent logs each bar’s initial weight.

### Phase 5: Curing & Testing (Agent reminders, Days 3–28)
- Agent maintains 28-day curing calendar with weekly weight-loss checks (soap loses 10–15 % water).
- Human performs weekly “zap test” (tongue touch — no tingle = safe) and pH strip test (agent interprets results).
- Agent requests final hardness photo on Day 28.

## Decision Tree (Agent Runs This Automatically)

**Batch will not trace after 45 minutes?**
- Agent triggers “Oil temperature mismatch” audit and supplies corrective stir or seed-crystal technique.

**pH > 10 after 7 days?**
- Agent escalates to “Extended cure + rebatch protocol” or full discard + neutralization steps.

**Bars sweat or crack during cure?**
- Agent diagnoses humidity issue and adjusts next-batch water discount or curing environment.

**All bars pass zap test and 28-day weight loss?**
- Agent auto-generates inventory cards + barter template: “12 handcrafted cold-process soap bars — 100 g each, unscented, trades for 2 kg rice or 4 hrs labor.”

## Ready-to-Use Templates & Scripts

**Ingredient Audit Sheet (Human fills, Agent processes)**
```
Fats/Oils:
- Tallow: ___ g
- Coconut oil: ___ g
- Olive oil: ___ g
- Other: 
Lye source: 
Distilled water available: yes/no
Target batch size (kg): 
Skin concerns (dry/sensitive): 
```

**Daily Curing Log (Agent maintains)**
```
Day X — Bar batch Y
Weight loss %: 
Zap test result: 
Ambient temp/humidity: 
Agent note: Next action in 24 h:
```

**Barter / Trade Script (Agent customizes)**
```
Subject: Handcrafted Cold-Process Soap — Local Ingredients, 28-Day Cure

Made with [your oils] and food-grade lye. pH tested safe, no fragrance. Each bar 100 g and lasts 4–6 weeks in daily use. Trade value ≈ 1 bar per 500 g rice or 30 min labor. Photos and test results attached.
```

**Progress Dashboard (Agent maintains in filesystem)**
- Total bars completed
- Success rate by recipe
- Ingredient sources ranked
- Next batch date reminder

## Success Metrics (Agent Tracks)

**Minimum Viable Success (Week 4)**
- One 1 kg batch yields 8–10 usable bars
- All bars pass zap test and 28-day cure
- One bar used daily for 14 days with no skin reaction

**Master Level (Month 3)**
- 5+ batches with <5 % failure rate
- Ability to scale recipes from any fat/oil combo user supplies
- Custom scent or exfoliant variants produced on demand
- 50+ bars in active rotation or traded

## Maintenance & Iteration

Agent runs a 30-day “Review & Scale” routine:
- Asks human for skin-use feedback and water-hardness notes.
- Generates next-batch optimizations (e.g., “Increase coconut to 30 % for harder bar”).
- Archives successful recipes as reusable templates for future runs.
- Suggests advanced variants (castile, salt bars, liquid castile) only after three successful basic batches.

## Rules / Safety Notes

- Lye is caustic: always add lye to water, never reverse; wear full PPE (goggles, gloves, long sleeves).
- Work outdoors or under strong ventilation; keep vinegar + water spray bottle ready for skin contact.
- Children and pets excluded from entire process until bars are fully cured and tested.
- Never use aluminum containers (lye reacts); use stainless, glass, or silicone only.
- Test every new recipe on a small skin patch after full cure.
- Dispose of failed batches by neutralizing with vinegar then diluting heavily before drain.
- Stop immediately if you feel burning or dizziness — agent will pause and trigger full safety reset.

## Disclaimer

This skill encodes standard cold-process soap-making chemistry cross-checked against industry references (SoapCalc methodology, traditional lye tables) and modern safety protocols from the Handcrafted Soap & Cosmetic Guild. Results depend on ingredient purity, accurate weighing, and proper curing. No guarantees against skin sensitivity or batch failure. Use at your own risk; lye handling carries burn and inhalation hazards. Agent cannot physically mix or pour — all tactile and sensory decisions remain 100 % human. Consult local regulations for lye purchase and open-air curing. Not a substitute for professional cosmetic formulation training.