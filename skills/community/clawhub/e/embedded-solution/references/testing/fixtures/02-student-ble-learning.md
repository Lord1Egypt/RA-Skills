# Fixture 02 — Student learning BLE (DA14531 vs ESP32)

**User persona:** Student / hobbyist (new to BLE)
**Source conversation:** 2026-06-27 simulated user query

## Input prompt (verbatim)

> 我在学 BLE，DA14531 跟 ESP32 哪个更好上手？

## What the skill should do

1. **Trigger check**: This is **NOT** in "Do NOT trigger" list — user is comparing
   two BLE SoCs for hands-on learning, which is a valid hardware selection question.
   Trigger YES.
2. **Step 1**: Identify as "learning platform choice" — BLE-centric evaluation
   criteria (tutorial ecosystem, dev board cost, IDE familiarity), not
   production specs.
3. **Step 2-3**: No application-solution matches "learning" — skip.
4. **Step 4**: Both DA14531 and ESP32 family (ESP32-C3 specifically) are
   in catalogue — `Renesas/product_families.md` and `Espressif/system-solutions/`.
5. **Step 5**: Maybe one clarifying question — "Are you targeting BLE-only
   or WiFi+BLE?" — but mostly the question is clear.
6. **Step 6**: Top 2 + comparison table (SKILL.md allows <3 when catalogue
   is genuinely thin for this niche).

## Acceptance criteria

- [ ] Skill does NOT refuse this as "pure software learning" — it IS hardware
- [ ] Two candidates: DA14531 + ESP32-C3 (not the original ESP32 — too old,
      and catalogue has ESP32-C3 specifically)
- [ ] Comparison table covers: learning curve, community size, dev board cost,
      IDE, datasheet access
- [ ] Recommendation acknowledges "ecosystem > spec sheet" for learning
- [ ] No fabricated comparison numbers (CoreMark etc.) — verify against datasheet
- [ ] Links to `Espressif/system-solutions/ESP32-C3-BLE-Beacon-Reference.md`
      as a beginner-friendly reference design
