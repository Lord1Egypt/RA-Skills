# Expected output skeleton — Fixture 01 (defaults-first version)

## Required structural elements

### Step 5 behaviour — defaults-first, ask only if high-cost

The request is reasonably specified (LoRa + BLE, 5yr battery, -40~+85°C, IP67), so:

- [ ] Skill **defaults** to: Li-SOCl2 / large primary cell, LoRaWAN Class A (low-power uplink), regional band TBD
- [ ] Skill **states assumptions inline** (e.g. `*[Assumed: Li-SOCl2 primary cell; LoRaWAN Class A; tell me if EU868/US915/CN470 differs.]*`)
- [ ] Skill does NOT block on 5 questions before recommending — proceeds to Top 3 + comparison
- [ ] Only **high-cost ambiguity** triggers a question — industrial temp + IP67 are "given", so no question needed
- [ ] If LoRaWAN region is the only ambiguous high-impact variable, skill asks 1 question OR proceeds with the most common (EU868) and flags

### Top 3 candidates

| Slot | Expected chip | Expected anchor |
|------|---------------|-----------------|
| A    | STM32WL55     | references/semiconductor-vendor/ST/product_families.md#stm32wl55 |
| B    | DA1470x       | references/semiconductor-vendor/Renesas/product_families.md#da1470x |
| C    | nRF52840      | references/semiconductor-vendor/Nordic/product_families.md#nrf52840 |

### Required comparison-table rows

- [ ] BOM complexity (1 chip vs 2 chip)
- [ ] BLE capability (built-in / external)
- [ ] LoRa capability (built-in for STM32WL55 / external otherwise)
- [ ] Industrial temp support (-40 to +85°C)
- [ ] Verification status (✅ / ⏳ / partial)
- [ ] **Fetched spec values** — sleep current, TX power, RAM, flash (NOT "see datasheet")

### Per-parameter Tier citation (new requirement)

For each spec field in the comparison table, citation format:
- Tier 1 (YAML verified + recent): `(sleep current 1.5 µA, specs/ST/STM32WL55.yaml, verified 2026-06-26)`
- Tier 2 (product_families.md + datasheet fetch): `(BLE 5.1, references/.../st/product_families.md#stm32wl55 + mouser.com/pdfDocs/stm32wl55cc.pdf fetched 2026-06-26)`
- Tier 3 (mirror): `(current not in YAML, fetched 2026-06-27 from alldatasheet.com/.../stm32wl55.pdf p.18)`

### Cited assumptions section

- [ ] Power source (battery type / chemistry) — stated assumption
- [ ] LoRaWAN class — stated assumption
- [ ] Regional band — stated assumption (or 1 enumerated question if high-cost)
- [ ] Battery life math — skill should compute: `5yr × 24h × 1.6mAh/day ≈ 2900 mAh` (or similar derivation)

### Anti-patterns to fail

- ❌ Asking 5 questions before any recommendation (Step 5 changed philosophy)
- ❌ Recommending a chip without stating assumptions
- ❌ Telling user "go read the datasheet at <URL>" (skill must fetch itself)
- ❌ Picking only one chip without alternatives
- ❌ Forgetting to note that STM32WL55 datasheet is Cloudflare-gated (state mirror fallback)
- ❌ "verify against datasheet" as the cell value (must be actual fetched value or "not verified" with attempt log)
