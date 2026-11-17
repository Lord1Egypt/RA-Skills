# Expected output skeleton — Fixture 03 (defaults-first version)

## Required structural elements

### Recognition of multi-function BOM (NOT single chip)

- [ ] Skill identifies BLE SoC + fingerprint sensor + charger + battery = 4 functions
- [ ] Top 3 picks PER FUNCTION, not 3 chips overall

### Step 5 behaviour — defaults-first with medium-cost flags

The request has $30 BOM cap (stated) but battery/lock-mechanism/fingerprint-sensor are unspecified:

- [ ] Skill **defaults** to: Li-Po battery, 6-12 months life, motor-driven lock, 1k-10k production, fingerprint sensor = skill recommends (out of catalogue → Step 7)
- [ ] Skill **flags medium-cost assumptions**: `*[Assumed: Li-Po 6-12mo, motor lock, 1k-10k volume. If your use case differs, tell me and I'll re-rank.]*`
- [ ] Battery chemistry (Li-Po) drives charger pick → ISL9238 (NVDC) is a derived default
- [ ] Production volume (1k-10k) is a default that affects BOM cost tier
- [ ] Lock mechanism (motor) is the most binding unknown — could be escalated to 1 question if the user says "I'm not sure"

### BLE SoC top 3 (catalogue in-stock)

| Slot | Expected chip | Expected anchor |
|------|---------------|-----------------|
| A    | DA1470x       | references/semiconductor-vendor/Renesas/product_families.md#da1470x |
| B    | nRF52832      | references/semiconductor-vendor/Nordic/product_families.md#nrf52832 |
| C    | STM32WB55     | references/semiconductor-vendor/ST/product_families.md#stm32wb55 |

### Charger top 2 (catalogue in-stock)

- [ ] ISL9238 (NVDC, more capable) — derived from Li-Po default
- [ ] ISL9205 (linear, simpler) — alternative for cost-sensitive variant
- [ ] At least one comparison row in the charger table

### Fingerprint sensor — **OUT OF CATALOGUE — STEP 7 TRIGGERED**

- [ ] Skill MUST say "out of scope for skill's curated data"
- [ ] Skill MUST trigger Step 7 (external lookup)
- [ ] Skill MUST NOT invent part numbers like "Goodix GW62J8" as if confirmed
- [ ] At most: lists candidate vendors (Microchip / Goodix / Egis) and asks
      user to verify with vendor directly

### BOM cost framing

- [ ] Cost estimate as RANGE, not single number ($X-Y)
- [ ] Fingerprint sensor marked as TBD (cost unknown until user picks one)
- [ ] Total BOM framing: "leave $3-8 budget for fingerprint"
- [ ] Skill should compute rough totals: BLE $3-5 + Charger $1.2 + Battery ~$2 + Passives ~$1 = $7-9 (before fingerprint)

### Per-parameter Tier citation

- [ ] Each BLE SoC spec cited with tier (Tier 1 Renesas/Nordic YAML or Tier 2 product_families + fetch)
- [ ] Charger specs cited (Tier 1 Renesas YAML)
- [ ] Battery pricing from Tier 3 (mouser.com/digikey.com fetch)

### Anti-patterns to fail

- ❌ Picking one chip overall instead of per-function
- ❌ Inventing fingerprint sensor part numbers without "verify"
- ❌ Quoting a single total cost (e.g. "$28.50") with confidence
- ❌ Asking 5 questions before recommending
- ❌ Telling user "go find a fingerprint sensor" without listing candidate vendors
- ❌ "verify against datasheet" as a cell value
