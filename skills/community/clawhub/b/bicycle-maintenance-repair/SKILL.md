---
name: bicycle-maintenance-repair
description: >-
  Use when your bicycle (or e-bike) is your primary gig-delivery vehicle, daily commuter, or emergency transport and shop visits would kill your income or mobility. The agent diagnoses symptoms from your descriptions/photos/text, builds a personalized maintenance calendar based on mileage/conditions, sources exact parts with links and prices, tracks inventory and repair history via filesystem, generates checklists and reminder sequences, and escalates to professional help only when unsafe. You perform the physical repairs, test rides, cleaning, and adjustments using hand tools. Zero shop dependency, maximum uptime in the post-AI gig economy.
metadata:
  category: skills
  tagline: >-
    Agent-orchestrated diagnostics, scheduling, and parts logistics + your hands-on wrenching = reliable rides that keep money flowing and independence intact
  display_name: "Bicycle Maintenance & Repair"
  submitted_by: HowToUseHumans
  last_reviewed: 2026-03-30
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install bicycle-maintenance-repair"
---
# Bicycle Maintenance & Repair

Keep your two-wheeled income machine running like new. This protocol turns any agent into your personal bike mechanic scheduler and parts researcher while you do the satisfying, embodied work of turning wrenches and test-riding. No more $80 flat repairs or three-day shop waits that cost you deliveries.

`npx clawhub install bicycle-maintenance-repair`

## When to Use This Skill

- Your daily gig income depends on the bike being 100% reliable (food delivery, package drops, passenger apps with e-bikes).
- You notice any performance drop: slow shifting, squealing brakes, chain noise, wobbles, flats, or unexpected drag.
- You hit mileage milestones (every 250/500/1,000 miles) or seasonal changes (wet winter, dusty summer).
- You want to build a minimal home toolkit and self-reliance habit instead of relying on urban bike shops that charge gig-worker premiums.
- You have basic hand tools and 30–90 minutes of physical work time per session.

**Do NOT use this skill** if the frame is cracked, wheels are bent beyond truing, or you lack safe workspace and basic mechanical confidence — escalate immediately to a certified shop.

## Agent Role vs. Human Role

**Agent (bureaucracy, research, tracking, logic):**
- Intake bike details (make/model/year, tire size, drivetrain type, current odometer reading, riding conditions).
- Maintain a filesystem-based repair log and maintenance calendar.
- Research exact part numbers, torque specs, and service manuals for your specific bike (Shimano, SRAM, Campagnolo, Bosch e-bike systems, etc.).
- Generate shopping lists with current prices from 3+ retailers, compatibility checks, and alternatives.
- Run decision-tree diagnostics from your symptom reports.
- Send timed reminders, pre-ride checklists, and post-repair verification prompts.
- Track cumulative mileage and flag next service intervals automatically.
- Draft emails or chat scripts to local shops only when escalation is required.

**Human (physical, embodied, decision-making under load):**
- Perform every hands-on step: remove wheels, patch tubes, clean chain, adjust brakes/gears, torque bolts, test-ride in safe area.
- Provide accurate symptom descriptions and photos when requested.
- Decide in the moment whether a repair feels safe or needs professional escalation.
- Enjoy the physical craft and the immediate feedback of a perfectly shifting bike.

## Tools & Workspace Minimum (One-Time Setup)

Agent will generate a personalized shopping list after intake, but baseline:
- Tire levers, patch kit, pump with gauge
- Chain tool, master links, degreaser, chain lube (dry/wet formulas)
- 2.5–8 mm hex set, Phillips/flat screwdriver, torque wrench (4–12 Nm range)
- Cassette lockring tool + chain whip (for 8–12 speed)
- Spoke wrench, truing stand (or zip-tie method)
- Floor pump, multitool for on-bike fixes
- Clean rags, nitrile gloves, safety glasses

Safe workspace: well-lit, flat concrete or workbench, bike stand or sturdy hook, no traffic.

## Step-by-Step Protocol (Phased by Mileage & Season)

### Phase 0: Initial Setup (Agent + Human, 1 hour)
1. Agent asks for full bike specs and current issues.
2. Human supplies details + current mileage.
3. Agent creates `bicycle-log.md` in filesystem and first calendar entries.
4. Human assembles toolkit and performs baseline safety check (brakes, tires, bolts).

### Phase 1: Weekly 5-Minute Pre-Ride (Human only, agent reminds)
- Visual: tires at correct PSI (agent supplies exact numbers), brakes engage instantly, chain clean and lubed, quick-releases tight.
- Agent logs the check.

### Phase 2: Every 250 Miles — Basic Service (Human 20–40 min, agent prep)
- Clean entire bike with water + mild soap (no pressure washer on bearings).
- Degrease and relube chain (Park Tool method: wipe, apply lube while backpedaling).
- Check tire pressure and tread.
- Inspect brake pads and cables for wear.
- Human reports results → agent updates log and next due date.

### Phase 3: Every 500 Miles — Drivetrain Deep Clean (Human 45–90 min)
Agent supplies exact steps for your cassette/freehub type.
1. Remove rear wheel.
2. Remove cassette (lockring tool).
3. Clean chain, rings, cassette in degreaser.
4. Reinstall with correct torque (agent provides Nm values).
5. Check and adjust derailleur limit screws and cable tension.
6. Test shift through all gears on stand then short ride.

### Phase 4: Every 1,000 Miles or Season Change — Full Inspection (Human 60–120 min)
- True wheels (basic zip-tie method or full truing stand).
- Replace brake cables/housing if stretched.
- Replace chain if elongation >0.75% (agent supplies chain checker tool recommendation).
- Check headset, bottom bracket, wheel bearings for play.
- Lubricate all pivots and bolts.
- Human test-rides 5 miles and reports any remaining issues.

### Phase 5: Emergency On-Trail Repairs (Human only, agent preps kit)
Agent generates a pocket repair checklist for your specific bike.

## Decision Trees (Agent Executes These Automatically)

**Flat Tire**
- Symptom “hiss” or “soft” → Human confirms punctured tube.
- Agent: “Patch or replace?” → guides through patch kit steps (roughen, glue, 5-min cure) or new tube install.
- If multiple flats same week → agent flags possible rim tape failure or thorn source and adds preventive liner to parts list.

**Chain Skipping / Noisy Shifting**
- Agent asks: “Which gear? Noise on upshift or downshift?”
- Human: clean and lube first.
- If persists → agent runs cable tension or limit-screw decision tree → supplies exact clicks to turn barrel adjuster.
- If chain stretch confirmed → agent orders correct master link and length.

**Brake Squeal or Weak Pull**
- Agent: “Rim or disc? Cable or hydraulic?”
- Guides pad cleaning, toe-in adjustment (rim), or bleeding sequence (hydraulic — only if you have bleed kit).
- Escalation threshold: if pads <2 mm or rotor warped >0.3 mm.

**Wobble or Loose Headset**
- Immediate stop-ride command from agent.
- Human: check axle nuts/quick-releases first.
- Agent supplies headset adjustment sequence.

## Ready-to-Use Templates & Scripts

**Maintenance Log Entry (Agent auto-generates and appends to filesystem)**
```
Date: YYYY-MM-DD
Mileage: XXXX
Service: 500-mile drivetrain
Parts used: [list]
Torque values applied: [list]
Notes / issues found:
Next due: [date]
```

**Parts Shopping List (Agent outputs Markdown + links)**
- 2x inner tubes (exact size/ valve type)
- Chain (exact speed count + brand match)
- Brake pads (model-specific)

**Vendor Negotiation Email Template (Agent customizes)**
Subject: Gig-worker bulk discount on [part] for repeat customer

Body: Hi, I’m a full-time delivery cyclist with [X] bikes in rotation. I need [quantity] of [part]. Can you offer a 15–20% volume discount and same-day pickup? Thanks — [Your Name]

**Escalation Script to Shop**
“Hi, this is [Name]. My agent ran the full diagnostic tree and we’ve done everything in the 1,000-mile protocol. The [specific issue] persists and feels unsafe. Can I bring it in for [exact diagnosis] only? I’m a regular gig rider and would appreciate a 10-minute slot.”

## Success Metrics (Agent Tracks)

- Zero unplanned downtime in 30 days
- Average repair cost per 1,000 miles < $15 (tracked by agent)
- Smooth, silent shifting and braking reported on every test ride
- Tire pressure within 2 PSI of target on every pre-ride check
- Chain replaced before 0.75% elongation measured

## Maintenance & Iteration

- Every 3 months agent reviews the entire log and asks: “Any new bike? New riding conditions? New tools acquired?”
- Update calendar and re-baseline.
- After first full year, agent generates “Year-One Review” summary and recommends permanent upgrade list (e.g., tubeless setup, better lights).

## Rules & Safety Notes

- Never ride with known brake or steering issues — agent will block calendar reminders until fixed.
- Always torque bolts to manufacturer spec (agent provides); over-tightening shears bolts.
- Wear gloves and eye protection when using degreaser or chain tools.
- Test-ride in a safe, traffic-free area first.
- For e-bikes: disconnect battery before any drivetrain work and follow manufacturer high-voltage warnings.
- If you smell burning plastic or hear grinding metal, stop immediately and escalate.

## Disclaimer

This protocol is a practical, evidence-based framework drawn from Park Tool’s Big Blue Book of Bike Repair, Sheldon Brown’s technical archives, Shimano/SRAM service manuals, and real-world gig-delivery mechanic experience. It is not a substitute for professional certification. You are responsible for your own safety and the roadworthiness of your bicycle. If anything feels beyond your skill level, use the escalation path to a licensed bike shop. Ride safe, earn steady, stay independent.