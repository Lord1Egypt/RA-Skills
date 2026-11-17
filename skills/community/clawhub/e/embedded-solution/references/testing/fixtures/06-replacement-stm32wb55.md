# Fixture 06 — Replacement question (STM32WB55 burned, can I swap to CC2640R2F?)

**User persona:** Engineer doing field repair / respin
**Source conversation:** 2026-06-27 simulated user query

## Input prompt (verbatim)

> 之前设计的板子 STM32WB55 烧了，能直接换成 CC2640R2F 吗？引脚兼容吗？

## What the skill should do

1. **Step 1**: Recognise as a **replacement / compatibility** question, not a
   greenfield design. Critical evaluation criteria: pin compatibility,
   firmware migration effort, RF matching network changes.
2. **Step 2-3**: No replacement-solution in INDEX. Skip.
3. **Step 4**: Both STM32WB55 and CC2640R2F in catalogue. Both BLE SoCs but
   different architectures. Skill should NOT just compare BLE specs.
4. **Step 5**: ASK — "What STM32WB55 package (LQFP48/64/100)? What SDK
   does your firmware use (STM32CubeWB)? What was the antenna matching
   network?"
5. **Step 6**: Output is NOT a "top 3 replacement" — it's a **compatibility
   assessment** with caveats:
   - State clearly: "No drop-in replacement expected"
   - List 3 alternatives (CC2640R2F / re-source STM32WB55 / nRF52832)
     with the cost/effort of each
   - List what skill CANNOT tell without datasheet comparison
6. **Step 7 — External verification**: Skill must explicitly defer to datasheet
   comparison (vendor URLs to both PDFs) and list the specific datasheet
   sections to compare (pin tables, RF matching, BLE stack API).

## Acceptance criteria

- [ ] Skill recognises this is a compatibility/replacement question, NOT a
      "recommend the best chip" question
- [ ] Skill does NOT claim "yes, they're pin-compatible" or "no, they're
      not" without citing datasheet — both are equally risky to fabricate
- [ ] Skill asks about package + SDK + antenna (the 3 things that drive
      "how hard is the swap?")
- [ ] Skill lists what it CANNOT determine without direct datasheet
      comparison (pin tables, RF matching, BLE stack API)
- [ ] Skill suggests **re-sourcing STM32WB55** as the lowest-effort option
      (stock check + PCB unchanged) before recommending a respin
- [ ] Output template is **compatibility assessment**, not "top 3 comparison"
