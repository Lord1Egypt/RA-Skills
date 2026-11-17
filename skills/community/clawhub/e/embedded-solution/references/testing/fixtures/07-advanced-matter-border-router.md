# Fixture 07 — Advanced: Matter over Thread border router

**User persona:** Senior embedded engineer (Matter / Thread knowledgeable)
**Source conversation:** 2026-06-27 simulated user query

## Input prompt (verbatim)

> Matter over Thread 网关（边界路由器）的 SoC 怎么选？要 Thread + WiFi + BLE 三协议。

## What the skill should do

1. **Step 1**: Matter Border Router (MBR) — needs Thread + WiFi + BLE.
   Distinct from Matter End Device (which only needs Thread + BLE).
2. **Step 2**: No "matter border router" in INDEX.
3. **Step 4**: 
   - CC2652R (TI): Thread + BLE, **no WiFi** — needs companion
   - nRF52840 + nRF70: Thread + BLE + WiFi (split)
   - ESP32-C6: Thread + WiFi + BLE **single chip** (RISC-V)
   - ESP32-H2: Thread + BLE only (no WiFi)
4. **Step 5**: ASK — "WiFi 5 enough or WiFi 6 needed? Ethernet backhaul required
   or WiFi-only? Production volume (single-chip wins at >100k)?"
5. **Step 6**: Top 3 candidates (CC2652R, nRF52840+nRF70, ESP32-C6) with
   comparison matrix covering: Thread support, WiFi capability, BLE, Matter
   SDK maturity, single-chip integration.
6. **Step 7**: If user asks about CSA Matter specification or specific
   Thread 1.3 features, trigger Step 7 for external documentation URLs.

## Acceptance criteria

- [ ] Skill distinguishes Matter **Border Router** (3 protocols, needs WiFi)
      from Matter **End Device** (only needs Thread + BLE)
- [ ] Top 3 candidates use catalogue entries with Matter/Thread mention
- [ ] ESP32-C6 is included as the "single-chip" option — important for
      cost-sensitive designs
- [ ] CC2652R is included as the "proven Thread stack" option — even
      though it needs WiFi companion, its Matter SDK track record is solid
- [ ] Comparison matrix covers: Thread / WiFi / BLE / Matter SDK maturity /
      single-chip integration / verification status
- [ ] WiFi 6 vs WiFi 5 distinction is asked (drives ESP32-C6 vs older ESP32)
- [ ] Out-of-catalogue parts (if any) flagged for Step 7 lookup
