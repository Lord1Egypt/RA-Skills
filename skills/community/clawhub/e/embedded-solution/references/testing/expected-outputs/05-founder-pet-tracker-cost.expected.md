# Expected output skeleton — Fixture 05 (defaults-first version)

## Required structural elements

### Step 5 behaviour — defaults-first with 1 medium-cost question

The request is "minimize BOM cost" but doesn't specify active vs passive GPS:

- [ ] Skill **defaults** to: passive GPS (lower cost + longer battery), since user prioritised cost
- [ ] Skill **flags the active-vs-passive choice** as a medium-cost question because it dramatically changes BOM
- [ ] Skill does NOT block on this — proceeds with passive track BOM + lists active alternative
- [ ] User can override and get re-ranked BOM

### Two-track framing (proceed with default)

- [ ] Track 1 (default): Passive GPS (BLE-query-triggered, lower cost, longer battery)
- [ ] Track 2 (alternative): Active GPS (real-time tracking, higher cost, shorter battery)
- [ ] Skill leads with Track 1 (matching the "minimize cost" intent)

### BLE SoC top 3 (catalogue)

| Slot | Expected chip | Expected anchor |
|------|---------------|-----------------|
| A    | nRF52832      | references/semiconductor-vendor/Nordic/product_families.md#nrf52832 |
| B    | CC2640R2F     | references/semiconductor-vendor/TI/product_families.md#cc2640r2f |
| C    | DA1470x       | references/semiconductor-vendor/Renesas/product_families.md#da1470x |

### GPS module — **OUT OF CATALOGUE — STEP 7**

- [ ] Lists candidate vendors (Quectel, AT semiconductor, u-blox)
- [ ] Cites vendor URLs (Step 7 external, Tier 3)
- [ ] Does NOT invent specific part numbers as "the answer"
- [ ] Notes: GPS modules are external; user picks

### Total BOM framing — skill computes, not user

- [ ] Active track: cost range "$11-15 per unit" (approximate)
- [ ] Passive track: cost range "$6-8 per unit" (approximate)
- [ ] Cost given as RANGE, not single number
- [ ] "Sub-$5 BOM requires single-chip GPS+BLE — not in catalogue, aspirational"

### Cost-floor reality check

- [ ] Honest "below $5 needs integrated GPS+BLE single-chip — none in catalogue"
- [ ] Engineering + cert NRE will dominate at low volumes
- [ ] Does NOT pretend to know exact volume pricing

### Per-parameter Tier citation

- [ ] BLE SoC spec from Tier 1 (YAML) where available
- [ ] Battery + GPS pricing from Tier 3 (mouser / LCSC / alibaba)
- [ ] BOM total cost marked "estimated, verify with distributor"

### Anti-patterns to fail

- ❌ Single BOM (not two tracks)
- ❌ Inventing specific GPS module part numbers
- ❌ Quoting single total cost without "verify with vendor"
- ❌ Ignoring the cost-volume-NRE reality
- ❌ Asking "do you want active or passive GPS?" as a blocking question (should default to passive + flag)
- ❌ Forgetting to provide cost RANGE
