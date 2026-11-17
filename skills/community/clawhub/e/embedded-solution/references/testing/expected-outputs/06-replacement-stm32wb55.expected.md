# Expected output skeleton — Fixture 06 (defaults-first version)

## CRITICAL: This fixture does NOT use Top 3 template

This is a **replacement / compatibility** question. Correct output is a **compatibility
assessment**, not "top 3 chips". Skill must recognise this.

## Required structural elements

### Step 5 behaviour — defaults-first, smart assumptions

The user asks a specific yes/no question (replace STM32WB55 with CC2640R2F). Most
variables can be defaulted:

- [ ] Skill **defaults** to: STM32WB55 in LQFP48 package (most common), STM32CubeWB SDK, 50Ω antenna feed
- [ ] Skill **states assumptions inline** (e.g. `*[Assumed: STM32WB55 LQFP48 + STM32CubeWB SDK + 50Ω antenna. Tell me if different.]*`)
- [ ] Only **high-cost ambiguity** would trigger a question — pin compatibility is the actual answer, not a clarification

### Skill MUST fetch both datasheets (no more "I don't know")

- [ ] Tier 2 step 2b: fetch STM32WB55 datasheet (Mouser mirror, st.com Cloudflare-gated)
- [ ] Tier 2 step 2b: fetch CC2640R2F datasheet (TI direct, OK)
- [ ] Both datasheet fetches have URL + timestamp citations
- [ ] **Pin comparison table built from fetched datasheets** — not "I don't know, you check"

### Compatibility assessment (NOT top 3)

- [ ] Skill states verdict clearly: "NOT pin-compatible" (with evidence from datasheet)
- [ ] Skill explains WHY based on fetched data:
  - STM32WB55 LQFP48 pinout (datasheet p.18) vs CC2640R2F RGZ QFN48 pinout (datasheet p.20)
  - Different RF pin locations, different power pin assignments
- [ ] Skill does NOT claim pin-compatible OR pin-incompatible without datasheet evidence

### Spec comparison (skill-fetched, both datasheets)

- [ ] Core architecture (dual M4+M0+ vs single M3)
- [ ] Flash (1 MB vs 275 KB) — major difference
- [ ] RAM (256 KB vs 28 KB) — major difference
- [ ] BLE 5 capability (both have it)
- [ ] 802.15.4 (STM32WB55 yes, CC2640R2F no)
- [ ] TX power / RX sensitivity (similar)
- [ ] Each value cited with Tier (Tier 2 datasheet fetch URL + timestamp)

### 3 alternatives listed (with effort assessment, not ranked)

| Option | Effort | Cost | Risk |
|--------|--------|------|------|
| CC2640R2F | PCB respin + 固件重写 | medium | medium (flash/RAM may be insufficient) |
| **Re-source STM32WB55** | stock check only | low (if available) | low |
| nRF52832 | PCB respin + 固件重写 | medium | medium |

- [ ] Each option has effort + cost + risk assessment
- [ ] **Re-sourcing STM32WB55 recommended as lowest-effort option**

### What skill CANNOT determine (explicit list, after fetch attempt)

- [ ] User's existing firmware flash/RAM usage (would need user's codebase)
- [ ] Whether user actually uses 802.15.4 features (would need user's spec)
- [ ] Antenna matching network impact on RF (would need PCB layout)

### Step 7 verification (only for what skill genuinely cannot know)

- [ ] Skill provides direct datasheet URLs for both chips (already fetched above)
- [ ] Skill does NOT pretend to have done comparison it hasn't

### Anti-patterns to fail

- ❌ Top 3 chip comparison template (wrong)
- ❌ Saying "I don't know if they're pin-compatible, check the datasheet" — that's the skill's job now
- ❌ Not providing pin comparison table after fetching both datasheets
- ❌ Not mentioning re-sourcing the existing chip as the cheapest option
- ❌ Quoting flash/RAM numbers without tier citation
- ❌ Asking which package / SDK / antenna instead of defaulting + stating
