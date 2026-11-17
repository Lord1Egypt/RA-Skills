# Expected output skeleton — Fixture 02 (defaults-first version)

## Required structural elements

### Trigger check (must PASS — student learning IS valid hardware selection)

- [ ] Skill DOES trigger (does NOT refuse as "pure software/learning")
- [ ] Reasoning: comparing two BLE SoCs for hands-on development = hardware selection

### Step 5 behaviour — defaults-first

The question is reasonably specified (two specific chips to compare), so:

- [ ] Skill does NOT ask which BLE SoC family — user already named them (DA14531, ESP32)
- [ ] Skill may state 1 small assumption (e.g. "ESP32 → I'll pick ESP32-C3 over original ESP32 because catalogue has the C3 entry specifically")
- [ ] Proceeds directly to Top 2 + comparison
- [ ] No blocking questions

### Top 2 candidates (SKILL.md allows <3 for thin catalogue coverage of niche)

| Slot | Expected chip | Expected anchor |
|------|---------------|-----------------|
| A    | DA14531       | references/semiconductor-vendor/Renesas/product_families.md#da14531 |
| B    | ESP32-C3      | references/semiconductor-vendor/Espressif/system-solutions/ESP32-C3-BLE-Beacon-Reference.md |

> Note: NOT ESP32 (original) — catalogue has ESP32-C3 specifically for BLE-only learning.
> Skill should explicitly pick the right variant and state why.

### Required comparison-table rows

- [ ] Learning curve (focused vs ecosystem)
- [ ] Community / tutorial size
- [ ] Dev board cost (USD range) — fetched from LCSC / Mouser if needed
- [ ] IDE / SDK (Keil/Renesas vs Arduino/ESP-IDF)
- [ ] Datasheet access — note alcom mirror for Renesas Cloudflare-gated

### Per-parameter Tier citation

- [ ] Each spec field cites Tier 1/2/3 explicitly
- [ ] Note for published-skill users: `specs/` is a maintainer-only submodule
      (see SKILL.md `## Privacy / Publishing Notes`); published users
      reach specs via Tier 2 (`product_families.md` → vendor URL → datasheet
      mirror) and Tier 3 (Alldatasheet / Mouser / LCSC / alcom).
- [ ] ESP32-C3: Tier 2 (Espressif product_families → espressif.com → datasheet)
- [ ] DA14531: Tier 2 (Renesas product_families → alcom.be mirror — vendor
      site is Cloudflare-gated, mirror is the reliable route)

### Recommendation shape

- [ ] "For first BLE project → ESP32-C3 (ecosystem beats spec sheet)"
- [ ] "For learning BLE protocol internals → DA14531 (less distraction)"
- [ ] Recommendation based on fetched data, not memory

### Anti-patterns to fail

- ❌ Refusing as "out of scope: pure software/learning"
- ❌ Picking only one chip
- ❌ Recommending original ESP32 (overkill, WiFi+BLE confusion for BLE-only learner)
- ❌ Using production-spec criteria (CoreMark, RX sensitivity) instead of learning criteria
- ❌ Saying "specs vary; check vendor page" instead of fetching the spec
- ❌ Asking the user which chip family they want — they already named both
