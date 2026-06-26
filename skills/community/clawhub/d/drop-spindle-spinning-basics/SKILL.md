---
name: drop-spindle-spinning-basics
description: >-
  Use when commercial yarn, thread, or fiber becomes unreliable, expensive, or unavailable and you need custom-strength, colorable, repairable yarn from local wool, flax, or plant fiber for knitting, weaving, sewing, or trade goods. Agent identifies suitable local fibers from your photos/inventory, calculates twist ratios and yardage yields, generates multi-day prep-and-spin schedules with timed reminders, tracks yarn thickness and strength tests, and produces inventory/barter templates. Human performs every physical step — drafting, spinning, plying, and finishing — rebuilding tactile self-reliance in fiber-to-yarn conversion.
metadata:
  category: skills
  tagline: >-
    Turn raw wool or plant fiber into strong, usable yarn on a simple drop spindle — agent owns the math and schedules so you stay in the drafting and spinning.
  display_name: "Drop Spindle Spinning Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install drop-spindle-spinning-basics"
---
# Drop Spindle Spinning Basics

Turn raw wool, flax, cotton, or dogbane fiber into strong, consistent yarn using only a simple drop spindle, your hands, and a few minutes of practice. No wheel, no electricity, no prior experience required — just drafting and twist. The agent owns all fiber identification, ratio calculations, yardage math, and timeline tracking; you own the physical drafting, spinning, and plying that turns loose fiber into tradable, repairable thread.

`npx clawhub install drop-spindle-spinning-basics`

## When to Use

Deploy this skill when:
- Commercial yarn or thread prices spike or shelves empty.
- You need custom yarn for knitting, weaving, sewing repairs, or high-value barter goods.
- You have access to raw wool, flax, or wild plant fiber and refuse supply-chain dependence.
- Existing textiles are wearing out and you want a renewable source that you can dye or ply exactly to spec.
- You want a portable, repeatable micro-craft that builds focus and produces measurable progress in short sessions.

**Do not use** if you lack a drop spindle (agent supplies 5-minute DIY build instructions) or cannot source clean fiber. Agent will flag contamination immediately.

## Agent Role vs. Human Role (Clear Division of Labor)

**Agent owns:**
- All fiber-type identification and suitability scoring from user photos/inventory.
- Twist-ratio calculations, singles-to-plied formulas, and yardage-per-gram estimates.
- Automated prep/spin/ply/dry schedules with photo checkpoints.
- Thickness and strength-test logging plus escalation if yarn breaks under load.
- Barter templates, inventory cards, and “next-batch optimization” reports.
- Full safety protocol enforcement (ergonomic spin breaks, fiber-dust warnings).

**Human owns:**
- All physical contact with fiber: teasing, drafting, spinning, plying, and winding.
- Sensory judgment of draft consistency, twist feel, and final yarn evenness.
- Manual tension control and real-world use-testing.

## Step-by-Step Protocol (14-Day First Skein Cycle)

### Phase 0: Fiber Audit & Recipe Generation (Agent-led, 1 day)
1. Agent asks for fiber type/weight available plus photos.
2. Agent outputs exact recipe for a 50 g skein (wool or plant fiber) with target twist-per-inch and ply style.
3. Agent generates spindle balance checklist and DIY spindle build if needed.

### Phase 1: Fiber Prep (Human 45 min + Agent tracking, Day 1)
- Human teases and cards or hand-combs fiber into rolags; agent provides exact tuft size and alignment guidelines.
- Agent requests photo of prepared fiber and logs total weight.

### Phase 2: Singles Spinning (Human 2–3 hrs total, Days 2–6)
Agent supplies three ready-to-use targets:
- Beginner singles (medium thickness, 8–10 twists per inch)
- Fine singles (thread-weight for sewing)
- Worsted-weight singles (for knitting)

Human drafts and spins using the drop-and-twist method. Agent issues timed 15-minute sessions with built-in 5-minute “rest-and-assess” prompts and twist-count reminders. Agent logs length spun via photo uploads.

### Phase 3: Plying (Human 60–90 min, Days 7–8)
- Agent calculates exact plying direction and twist ratio.
- Human plies two or more singles; agent times the process and prompts evenness checkpoints.

### Phase 4: Washing & Setting Twist (Agent reminders, Days 9–11)
- Agent supplies warm-water + mild-soap recipe and soak time.
- Human washes and hangs to dry with weight; agent sets 48-hour set-twist timer.

### Phase 5: Testing & Finishing (Days 12–14)
- Human performs 1 kg tension test and knit/swatch test; agent logs results.
- Agent generates “Next Skein Improvements” report (e.g., “Increase twist 10 % for harder yarn”).

## Decision Tree (Agent Runs This Automatically)

**Fiber too short or slippery to draft?**
- Agent switches to secondary fiber or supplies “pre-draft and oil” protocol.

**Yarn breaks repeatedly?**
- Agent reduces twist or flags fiber contamination and recommends carding aid.

**Uneven thickness after plying?**
- Agent adjusts drafting tension for next singles or supplies “navajo plying” alternative.

**Skein passes 1 kg test and knits evenly without curling?**
- Agent auto-generates inventory card + barter template: “50 g hand-spun wool yarn — 2-ply worsted, trade value ≈ 1 skein per 500 g rice or 1 hr labor.”

## Ready-to-Use Templates & Scripts

**Fiber Intake Form (Human fills, Agent processes)**
```
Fiber type & weight (g):
Source (washed/raw):
Color notes:
Photos attached:
Notes (coarse/fine):
```

**Spinning Progress Log (Agent maintains)**
```
Day X — Skein Y
Grams spun:
Twists per inch:
Length estimate:
Agent note: Next action in ___ hours
```

**Barter / Trade Script (Agent customizes)**
```
Subject: Hand-Spun Drop-Spindle Yarn — 2-Ply, Custom Twist

Made from local wool/flax with traditional drop-spindle technique. Even, strong, and ready to knit or weave. Trade value ≈ 1 skein per 500 g rice, 200 g fiber, or 1 hr labor. Photos and test results attached.
```

**Progress Dashboard (Agent maintains in filesystem)**
- Total skeins completed
- Average yardage per gram
- Fiber sources ranked by spin quality
- Next spinning batch reminder

## Success Metrics (Agent Tracks)

**Minimum Viable Success (Week 2)**
- One 50 g 2-ply skein that passes 1 kg tension test and knits/swatches evenly
- Zero major slubs or breaks
- One skein used in a small project for 7 days with no pilling

**Master Level (Month 3)**
- 10+ skeins across fibers and weights with <5 % failure rate
- Ability to produce custom ply counts from any local fiber user supplies
- 500+ meters of yarn in active rotation or traded
- Dyed or multi-color variants produced on demand

## Maintenance & Iteration

Agent runs a 30-day “Review & Scale” routine:
- Asks human for real-world performance feedback (knit feel, durability, dye uptake).
- Generates next-batch optimizations (e.g., “Add 15 % flax for stronger warp yarn”).
- Archives successful twist recipes as reusable templates.
- Suggests advanced variants (supported spindle, Andean plying, small wheel intro) only after three successful basic skeins.

## Rules / Safety Notes

- Maintain neutral wrist position; agent issues timed spin breaks every 20 minutes to prevent strain.
- Work in well-ventilated area; fiber dust can irritate lungs — optional mask recommended.
- Never leave spindle unattended while spinning (tangle risk).
- Test every new fiber batch with a 5 g sample skein before full run.
- Children only under direct adult supervision; no spindle participation until confident.
- Store finished yarn dry and away from moths (agent supplies natural repellent recipe).
- Stop immediately if you feel wrist or shoulder pain — agent will pause and suggest 48-hour rest plus ergonomic review.

## Disclaimer

This skill encodes traditional drop-spindle spinning techniques refined over thousands of years in cultures worldwide and cross-checked against historical fiber-arts references and modern hand-spinning manuals. Results depend on fiber quality, consistent drafting, and proper twist setting. Spinning involves repetitive motion that can cause strain if mishandled. No guarantees against breakage or uneven yarn. Use at your own risk; improper technique carries repetitive-strain hazards. Agent cannot physically draft or spin fiber — all tactile, sensory, and tension decisions remain 100 % human. Consult local fiber sourcing regulations and perform a small test skein before large production. Not a substitute for professional fiber-arts training.