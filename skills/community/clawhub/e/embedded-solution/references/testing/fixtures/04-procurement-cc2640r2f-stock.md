# Fixture 04 — Procurement asking about CC2640R2F stock

**User persona:** Buyer / procurement (focused on availability and lead time)
**Source conversation:** 2026-06-27 simulated user query

## Input prompt (verbatim)

> CC2640R2F 现在 Mouser 库存怎么样？还能下单吗？

## What the skill should do

1. **Step 1**: Recognise as a **procurement / lifecycle** question, NOT a
   new-design BOM question. Different evaluation criteria: stock count,
   lead time, lifecycle status (active / NRND / EOL), not specs.
2. **Step 2-3**: No application-solution matches "procurement". Skip.
3. **Step 4**: CC2640R2F is in TI product_families.md (status: ⏳ verification pending).
   Skill should NOT fabricate stock counts or lead times.
4. **Step 5**: Question is clear — no clarification needed.
5. **Step 6**: Output should NOT be a "top 3 chips" comparison. Instead:
   - State the chip's status in this skill's catalogue
   - Link to TI product page (vendor's own statement on lifecycle)
   - **Trigger Step 7** for distributor inventory lookup
   - List distributor URLs (Mouser / Digi-Key / LCSC) for the user to check directly
6. **Step 7 — External lookup (marketplace tier)**: Provide Mouser / Digi-Key
   product URLs. Cite them. Do NOT fetch and paste stock numbers (changes
   constantly, would violate "no fabrication" if stale).

## Acceptance criteria

- [ ] Skill recognises this is a procurement question, not a chip-selection question
- [ ] Skill does NOT invent stock counts ("only 500 left") or lead times
- [ ] Skill explicitly says: "always check the distributor link below for live stock"
- [ ] Distributor URLs provided: Mouser, Digi-Key, LCSC
- [ ] Lifecycle status quoted from vendor (e.g. TI's "not recommended for new
      designs (NRND)" notice if applicable)
- [ ] For new projects, skill suggests checking newer alternatives in catalogue
      (CC2340R5) but does NOT push migration unless asked
- [ ] NO "Top 3" comparison table — wrong output template for this question type
