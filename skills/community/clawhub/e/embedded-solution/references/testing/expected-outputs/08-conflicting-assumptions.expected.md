# Expected output skeleton — Fixture 08

## CRITICAL: This fixture tests conflict detection, not chip recommendation

Correct output is a **single targeted question with enumerated options** that resolves the contradiction. Skill must NOT pick a chip yet.

## Required structural elements

### 1. Conflict is named explicitly

- [ ] "USB-powered" constraint explained (continuous or always-recharging; battery is backup)
- [ ] "5-year battery" constraint explained (primary cell, no maintenance)
- [ ] "Outdoors" constraint explained (wide temp, weatherproof)
- [ ] The three are mutually exclusive **as stated**, by name

### 2. Single targeted question

- [ ] **Exactly one** question (not 3+, not 0)
- [ ] Question is **enumerated** with 2-4 options (a/b/c or a/b/c/d)
- [ ] Options cover the most plausible resolutions of the conflict

### 3. Each option describes downstream impact

| Option | Downstream impact |
|--------|-------------------|
| (a) Outdoor + USB + solar harvest | Low-power MCU + solar + Li-Po buffer (LoRa weather station pattern) |
| (b) Outdoor + 5yr primary battery, no USB | Sealed enclosure, Li-SOCl2, ultra-low-power MCU (industrial tracker pattern) |
| (c) Outdoor USB-powered data logger | Almost any MCU; battery is short-term backup only |
| (d) Something else (open) | Free-form |

### 4. No chip recommendation yet

- [ ] No "Top 3 MCU" table in the question
- [ ] No spec citations (because no chip has been picked)
- [ ] Skill commits to "I'll re-rank after you pick"

### 5. Pre-Search-Priority escalation (meta-rule)

- [ ] Skill does NOT enter Step 4 (Search Priority) before the conflict is resolved
- [ ] Implication: the "validate per-tier" check in Step 6 doesn't apply yet
- [ ] Skill explicitly says: "no point comparing MCUs when the power architecture is unknown"

## Acceptance criteria

- [ ] Conflict named in plain language, not jargon
- [ ] Question is **single** and **enumerated**
- [ ] Each option describes what changes downstream
- [ ] No chip recommendation yet (the whole point — Top 3 belongs in Step 6, not Step 5)
- [ ] No datasheet fetch attempted
- [ ] No fabricated specs

## Anti-patterns to fail

- ❌ Silently pick (b) — primary battery — without flagging the conflict
- ❌ Ask 5 separate clarification questions
- ❌ "Let me look this up" filler before the question
- ❌ Recommend any chip before the user resolves the conflict
- ❌ Open-ended question ("Can you clarify?")
- ❌ Fabricated reasoning from memory
- ❌ Proceeding to Step 4 (fetch datasheets) before the power architecture is decided
