# Expected output skeleton — Fixture 07

## Required structural elements

### Recognition of Matter Border Router (vs End Device)

- [ ] Skill distinguishes Matter **Border Router** (Thread + WiFi + BLE) from
      Matter **End Device** (Thread + BLE only)
- [ ] Skill understands MBR has the gateway role, not just endpoint

### Step 5 questions

- [ ] WiFi 5 enough or WiFi 6 needed? (drives ESP32-C6 vs older ESP32)
- [ ] Ethernet backhaul required or WiFi-only?
- [ ] Production volume (>100k? single-chip wins for cost)

### Top 3 candidates

| Slot | Expected chip | Expected anchor | Single-chip? |
|------|---------------|-----------------|--------------|
| A    | CC2652R (TI)  | references/semiconductor-vendor/TI/product_families.md#cc2652r | ❌ (needs WiFi companion) |
| B    | nRF52840 + nRF70 (Nordic) | references/semiconductor-vendor/Nordic/product_families.md#nrf52840 | ❌ (split) |
| C    | ESP32-C6 (Espressif) | references/semiconductor-vendor/Espressif/product_families.md | ✅ (single chip) |

- [ ] All three present
- [ ] CC2652R listed for "proven Thread stack" rationale (TI Matter SDK track record)
- [ ] ESP32-C6 listed for "single-chip integration" rationale
- [ ] nRF52840 + nRF70 listed as middle ground

### Required comparison-table rows

- [ ] Thread support
- [ ] WiFi capability (built-in / companion)
- [ ] BLE
- [ ] Matter SDK maturity
- [ ] Single-chip integration
- [ ] Verification status

### Step 7 — External lookup (spec body)

- [ ] If user asks about CSA Matter spec / Thread 1.3 features, skill cites
      CSA URL
- [ ] Does NOT invent Thread 1.3 specific feature names

### Anti-patterns to fail

- ❌ Confusing Matter Border Router with Matter End Device
- ❌ Missing ESP32-C6 (single-chip option is critical for cost-conscious)
- ❌ Not asking WiFi 5 vs WiFi 6 question
- ❌ Treating Matter as just "another wireless protocol" without MBR/ED distinction
