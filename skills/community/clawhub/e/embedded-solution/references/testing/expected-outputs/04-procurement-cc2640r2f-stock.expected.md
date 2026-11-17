# Expected output skeleton — Fixture 04 (defaults-first version)

## CRITICAL: This fixture does NOT use Top 3 template

This is a procurement / lifecycle question. Correct output is a **stock assessment**,
not "top 3 chips". Skill must recognise this.

## Required structural elements

### Step 5 behaviour — defaults-first

- [ ] No blocking questions (the user asked a specific yes/no with rationale)
- [ ] Proceeds directly to stock assessment

### Recognition of question type

- [ ] Skill identifies "procurement / lifecycle" question (NOT chip selection)
- [ ] Different evaluation criteria: stock count, lead time, lifecycle status

### CC2640R2F catalogue status (Tier 2 first)

- [ ] Skill reads `references/semiconductor-vendor/TI/product_families.md#cc2640r2f`
- [ ] Reports verification status (⏳ verification pending per catalogue)
- [ ] Tier 2 step 2b: fetches TI product page to confirm lifecycle (active vs NRND vs EOL)

### Step 7 — External lookup (marketplace tier) — Tier 3 mirror list

- [ ] Mouser product URL provided (Tier 3 mirror #2)
- [ ] Digi-Key product URL provided (Tier 3 mirror #3)
- [ ] LCSC search URL provided (Tier 3 mirror #7 — Chinese vendor fallback)
- [ ] Skill does NOT paste stock numbers (changes constantly)
- [ ] Stock check is the user's job via the provided URLs

### Lifecycle status from vendor (TI) — Tier 2 fetched

- [ ] States vendor's own status: "active but NRND" (not recommended for new designs)
- [ ] Cites TI product page URL
- [ ] Notes: "still orderable for existing projects"
- [ ] **Fetched timestamp + URL** included in citation

### Recommendation shape

- [ ] For existing project: orderable, check distributor directly (Mouser / Digi-Key / LCSC)
- [ ] For NEW project: suggests CC2340R5 (newer, in catalogue, Tier 1 verified)
- [ ] Does NOT push migration unless asked (respects user's existing design)

### Anti-patterns to fail

- ❌ Using Top 3 chip comparison template (wrong output template)
- ❌ Fabricating stock counts ("only 500 left at Mouser")
- ❌ Pushing aggressive migration ("you should redesign with CC2340R5")
- ❌ Missing distributor URLs
- ❌ Saying "check the datasheet" instead of fetching TI product page
- ❌ Forgetting LCSC as Tier 3 mirror for Chinese users
