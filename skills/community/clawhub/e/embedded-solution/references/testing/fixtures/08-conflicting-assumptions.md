# Fixture 08 — Conflicting assumptions (USB + 5yr battery + outdoor)

**User persona:** Distracted founder giving a quick verbal brief without reviewing constraints
**Source conversation:** 2026-06-27 (added after defaults-first UX change)

## Input prompt (verbatim)

> "I need a remote sensor node — USB powered, but must last 5 years on battery, and it'll be outdoors. Recommend the MCU."

## What the skill should do

1. **Step 1 — Understand application**: outdoor sensor node (environmental? asset tracker? weather?)
2. **Step 2 — INDEX lookup**: no matching application-solution; this is a one-off
3. **Step 4 — Run Search Priority**: per Tier 1 / 2 / 3
4. **Step 5 — DETECT CONFLICT** (this fixture's whole point):
   - "USB powered" → implies mains or always-charged, NOT a battery that runs out
   - "5 years on battery" → implies primary battery (Li-SOCl2 / Li-thionyl / large Li-Po) with no maintenance
   - "outdoors" → implies weatherproof enclosure, possibly solar, possibly wide temperature
   - **These three cannot all be true at once without clarification.** USB-powered devices are NOT battery-primary; battery-primary devices don't need USB (unless charging).
5. **Skill must surface the conflict**, NOT silently pick one and assume.
6. **Step 5 high-cost escalation justified** — the cost of being wrong is medium (a wrong pick wastes prototyping time, not lives). So skill should ask ONE targeted question to resolve the conflict, with enumerated options.

## Expected behaviour (defaults-first, conflict-aware)

The skill should produce a response that:

1. Names the conflict explicitly
2. Asks ONE question to resolve it (not 5 questions, not silently assume)
3. The question offers 2-4 enumerated options covering the most likely resolutions
4. Each option includes what changes downstream (chip pick, BOM cost, design effort)

### Example acceptable response (structure)

> The 3 constraints are mutually exclusive as stated. Let me name the conflict:
>
> - **USB-powered** → continuous mains or always-recharging; battery is backup (days, not years)
> - **5-year battery** → primary cell (Li-SOCl2 / large Li-Po); no USB, no maintenance access
> - **Outdoors** → wide temp, weatherproof, possibly solar-recharged
>
> Which use case are you actually building?
>
> (a) **Outdoor sensor with USB power + solar charging** — 5-year "battery" is really "5 years without grid power, USB when available" → use low-power MCU + solar harvest + Li-Po buffer (think LoRa weather station)
>
> (b) **5-year primary battery, no USB** — sealed enclosure, Li-SOCl2 cell, ultra-low-power MCU (think industrial asset tracker) — outdoors is just about temperature/IP rating
>
> (c) **USB-powered outdoor data logger** — short battery (hours–days) for blackout, mains otherwise — power budget is easy; pick almost any MCU
>
> (d) **Something else** — describe
>
> After you pick, I'll re-rank the MCU candidates.

## Acceptance criteria

- [ ] Skill identifies the 3-way conflict by NAME (not silently picks one)
- [ ] Skill asks **exactly one** question to resolve, not 3+ separate questions
- [ ] The question offers 2-4 **enumerated** options (a/b/c/d), not open-ended
- [ ] Each option describes what changes downstream (which chip family, BOM cost tier, design effort)
- [ ] Skill does NOT silently default to (a) or (b) — both are plausible, ambiguity is real
- [ ] After the user picks, skill proceeds to Step 6 with no further questions (Step 5 escalation is over)
- [ ] No fabricated spec numbers in the question options
- [ ] No "let me look this up" filler — skill commits to "I'll re-rank after you pick"

## Anti-patterns to fail

- ❌ Silently assume USB is for charging, recommend a solar + Li-Po design without flagging
- ❌ Pick the "most common" option (primary battery sensor) without telling the user the others were rejected
- ❌ Ask 5 separate questions: "What's the application? Battery capacity? Outdoor enclosure rating? USB connector type? Solar panel?"
- ❌ Recommend a chip before the user picks (a)/(b)/(c)/(d)
- ❌ Open-ended question: "Can you clarify what you mean?"
- ❌ Fabricated: "Most USB-powered outdoor sensors use the nRF52832..." (memory, not verified)

## Tier usage in the question itself

The skill should NOT fetch any datasheet before resolving the conflict — there's no point comparing MCUs when the power architecture is unknown. The conflict-detection step happens **before** Search Priority tier escalation. This is a meta-rule:

> **If the request is internally inconsistent, ask 1 question FIRST; do not waste fetch budget on a chip that won't be picked.**
