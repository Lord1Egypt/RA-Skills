# Expected output skeleton — Fixture 07 (defaults-first version)

## Required structural elements

### Step 5 behaviour — defaults-first

The user knows what they want (Matter + Thread + WiFi + BLE border router). Most
ambiguities can be defaulted:

- [ ] Skill **defaults** to: WiFi 5 (most home gateways), no Ethernet backhaul, production volume "unknown — assume 1k-10k for cost sweet spot"
- [ ] Skill **flags production volume** as a medium-cost question because single-chip vs split depends on volume
- [ ] Skill proceeds with Top 3 (single-chip vs split tradeoff)

### Recognition of Matter Border Router (vs End Device)

- [ ] Skill distinguishes Matter **Border Router** (Thread + WiFi + BLE) from
      Matter **End Device** (Thread + BLE only)
- [ ] Skill understands MBR has the gateway role, not just endpoint

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

### Required comparison-table rows (skill-fetched)

- [ ] Thread support
- [ ] WiFi capability (built-in / companion)
- [ ] BLE
- [ ] Matter SDK maturity
- [ ] Single-chip integration
- [ ] Verification status
- [ ] **WiFi 5 vs WiFi 6 distinction** — fetched from product page
- [ ] Each value cites Tier 1/2/3 with URL + timestamp

### Defaults stated inline

- [ ] WiFi 5 (default); "tell me if WiFi 6 required"
- [ ] No Ethernet (default); "tell me if wired backhaul needed"
- [ ] Production volume (default 1k-10k); "tell me if >100k (single-chip wins)"

### Step 7 — External lookup (spec body) — only if user asks for CSA Matter spec

- [ ] If user asks about CSA Matter spec / Thread 1.3 features, skill cites
      CSA URL
- [ ] Does NOT invent Thread 1.3 specific feature names

### Anti-patterns to fail

- ❌ Confusing Matter Border Router with Matter End Device
- ❌ Missing ESP32-C6 (single-chip option is critical for cost-conscious)
- ❌ Asking "WiFi 5 or 6?" as blocking question (should default + flag)
- ❌ Treating Matter as just "another wireless protocol" without MBR/ED distinction
- ❌ Quoting WiFi/BLE/Thread versions without tier citation
- ❌ Missing single-chip vs split tradeoff explanation
