---
name: cattail-mat-weaving-basics
description: >-
  Use when you need durable, insulating, water-resistant, and fully repairable floor mats, bedding pads, wall insulation, or trade goods made from local cattail leaves and commercial mats or synthetic coverings are unreliable or unavailable. Agent identifies safe cattail stands from your photos/GPS, calculates leaf volume and weave density for target size/strength, generates multi-day harvest/weave/dry schedules with timed reminders, tracks pattern templates and load tests, and produces inventory/barter templates. Human performs every physical step — harvesting, sorting, plaiting, binding, and finishing — rebuilding tactile self-reliance in flat-weave plant crafts.
metadata:
  category: skills
  tagline: >-
    Turn abundant cattail reeds into thick, insulating mats that warm floors and beds for years — agent owns the botany math and schedules so you stay in the plaiting and tightening.
  display_name: "Cattail Mat Weaving Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install cattail-mat-weaving-basics"
---
# Cattail Mat Weaving Basics

Turn fresh or dried cattail leaves into thick, insulating, water-resistant mats for flooring, bedding, wall panels, or high-value trade goods using only your hands, a needle or awl, and natural cord. No loom required — just simple plaiting and edge binding. The agent owns all stand identification, volume math, pattern templates, and timeline tracking; you own the physical harvesting, sorting, weaving, and tightening that turns marsh reeds into functional, renewable coverings.

`npx clawhub install cattail-mat-weaving-basics`

## When to Use

Deploy this skill when:
- Commercial floor mats, rugs, or insulation become expensive, scarce, or you refuse synthetic dependence.
- You need custom-sized, repairable pads for cold floors, sleeping rolls, garden kneeling, or barter.
- You have access to cattail marshes or similar reeds and want a seasonal craft that produces zero-waste goods.
- Existing bedding or floor coverings are failing in damp or high-wear conditions.
- You want a repeatable micro-business or trade good (one large mat historically trades for days of labor in many regions).

**Do not use** if you cannot safely identify cattail or lack access to clean water for soaking. Agent will flag toxic look-alikes immediately.

## Agent Role vs. Human Role (Clear Division of Labor)

**Agent owns:**
- All plant-species identification and suitability scoring from user photos/GPS.
- Leaf-yield calculations, weave-density formulas, and size/load-rating estimates.
- Automated harvest/soak/weave/dry schedules with photo checkpoints.
- Ready-to-trace pattern templates and durability-test logging.
- Barter templates, inventory trackers, and escalation if leaves fail pliability tests.
- Full safety protocol enforcement (glove reminders, ergonomic breaks).

**Human owns:**
- All physical contact with leaves: harvesting, sorting, soaking, plaiting, edge binding, and final tightening.
- Sensory judgment of leaf flexibility, weave tightness, and final mat firmness.
- Manual load-testing and real-world use.

## Step-by-Step Protocol (21-Day First Mat Cycle)

### Phase 0: Stand Survey & ID (Agent-led, 1 day)
1. Agent asks for GPS or nearest town plus photos of candidate plants.
2. Agent cross-references safe reed species and issues a 5-question field checklist (tall straight leaves, no pollution).
3. Agent outputs top locations with exact harvest volume needed (≈200–300 leaves for one 1 × 2 m mat).

### Phase 1: Harvesting & Sorting (Human 1–2 hrs + Agent tracking, Day 1)
- Human cuts leaves near base; agent provides exact seasonal and height guidelines.
- Human sorts by length and width; agent requests photo of sorted bundles and logs counts.

### Phase 2: Soaking & Conditioning (Agent reminders, Days 2–7)
- Agent calculates soak time based on local temperature (5–10 days to pliable).
- Human submerges bundles; agent issues daily “check bend” reminders and flags readiness.

### Phase 3: Base Plaiting (Human 3 hrs, Day 8)
Agent supplies three ready-to-trace templates:
- Standard floor mat (1 × 2 m, 8–10 mm thick)
- Bedroll pad (1.2 × 2 m, extra cushion)
- Garden kneeling mat (0.6 × 1 m, heavy weave)

Human begins plaiting the base; agent issues timed 30-minute sessions with rest prompts and row-count checklists.

### Phase 4: Full Weaving & Tightening (Human 6–8 hrs total, Days 9–14)
- Human continues over-under plaiting; agent provides exact row-density targets and photo checkpoints for even tension.
- Agent logs overall dimensions and flags loose spots for correction.

### Phase 5: Edge Binding & Finishing (Human 2 hrs, Days 15–17)
- Human binds edges with cord or extra leaves; agent supplies exact lashing technique.
- Agent requests final photos and sets 3–4 day air-dry schedule.

### Phase 6: Testing & Curing (Agent reminders, Days 18–21)
- Human performs 20 kg load test and water-splash test; agent logs results.
- Agent generates “Next Mat Improvements” report.

## Decision Tree (Agent Runs This Automatically)

**Leaves too brittle after soaking?**
- Agent extends soak time 48 hrs or switches to secondary reed species.

**Weave gaps >8 mm or mat warps?**
- Agent triggers “tighter tension” or “add cross-bracing leaves” protocol.

**Mat too thin after drying?**
- Agent adjusts next-batch leaf count upward.

**Mat passes 20 kg load test and water-splash test with <5 % flex?**
- Agent auto-generates inventory card + barter template: “2 m² hand-woven cattail floor mat — insulating & repairable, trade value ≈ 1 mat per 5 kg rice or 3 hrs labor.”

## Ready-to-Use Templates & Scripts

**Harvest Field Report (Human fills, Agent processes)**
```
Species (suspected): 
Location: [GPS or description]
Leaf count & length: 
Pliability test result: 
Photos attached: yes
```

**Weaving Progress Log (Agent maintains)**
```
Day X — Mat Y
Rows completed: 
Current size (m): 
Tension notes: 
Agent note: Next action in ___ hours
```

**Barter / Trade Script (Agent customizes)**
```
Subject: Hand-Woven Cattail Mat — 2 m², Insulating, Ready to Trade

Made from local cattail with tight plait weave. Tested for strength and water resistance. Perfect for floors, beds, or kneeling. Trade value ≈ 1 mat per 5 kg rice, 3 kg meat, or 3 hrs labor. Photos and test results attached.
```

**Progress Dashboard (Agent maintains in filesystem)**
- Total mats completed
- Average thickness and load capacity
- Cattail sources ranked by quality
- Next harvest window reminder

## Success Metrics (Agent Tracks)

**Minimum Viable Success (Week 3)**
- One 1 × 2 m mat that is uniformly thick, passes water-splash test, and holds 20 kg without deformation
- Zero major gaps or unraveling
- One mat used daily for 14 days with no loosening

**Master Level (Month 3)**
- 5+ mats across sizes and patterns with <5 % failure rate
- Ability to weave custom shapes from any local reed user supplies
- 10+ m² of matting in active use or traded
- Edge and handle variations produced on demand

## Maintenance & Iteration

Agent runs a 30-day “Review & Scale” routine:
- Asks human for real-world performance feedback (insulation, durability, ease of repair).
- Generates next-batch optimizations (e.g., “Add 15 % wider leaves for faster coverage”).
- Archives successful patterns as reusable templates.
- Suggests advanced variants (lidded storage mats, wall panels, chair seats) only after three successful basic mats.

## Rules / Safety Notes

- Wear heavy gloves during harvesting — cattail can cause skin irritation or cuts.
- Never harvest from polluted water or chemically sprayed areas.
- Test every new stand with a small 10-leaf sample weave before full mat.
- Use sharp knife for trimming; keep both hands behind blade.
- Children only under direct adult supervision; no harvesting participation.
- Store finished mats flat and dry to prevent mold.
- Stop immediately if you develop rash or wrist strain — agent will pause and trigger full safety reset.

## Disclaimer

This skill encodes traditional cattail-mat weaving techniques refined over centuries in Native American, European wetland, and bushcraft traditions and cross-checked against ethnobotanical references and modern natural-fiber manuals. Results depend on leaf quality, soak conditions, and weave consistency. Weaving involves sharp tools and repetitive motion that can cause cuts or strain if mishandled. No guarantees against breakage or skin irritation. Use at your own risk; improper harvesting carries plant-toxicity hazards. Agent cannot physically harvest or weave — all tactile, sensory, and safety decisions remain 100 % human. Consult local foraging regulations and perform a patch test with finished mats. Not a substitute for professional basketry training.