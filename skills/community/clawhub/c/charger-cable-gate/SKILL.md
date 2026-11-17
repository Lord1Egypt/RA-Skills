---
name: charger-cable-gate
description: Use when pairing a USB-C charger, cable, and device and wondering why charging is slow or not working — PD revision rules (2.0/3.0 PPS/3.1 EPR 140-240W), cable e-marker 3A vs 5A current caps, charge-only cable traps, proprietary protocols (VOOC/QC) vs standard PD, and per-archetype wattage needs; outputs OK / CAPPED / SLOW / NO-CHARGE verdicts with the exact bottleneck.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [usb-c, power-delivery, charger, cable, pd, epr, wattage, fast-charge]
---

# Charger & Cable Gate — USB-C PD Compatibility

Fast charging fails silently. You plug a 65W laptop brick into an
ultrabook with a bargain cable and get... 27W, or nothing. The chain
is charger protocol × cable current rating × device appetite, and the
weakest link caps everything — with no error message, just slower
charging. This skill checks the whole triple and names the bottleneck.

## When to Use

- "Why is my laptop charging slowly / battery draining while plugged
  in?" — the #1 USB-C mystery
- Buying a replacement charger or cable — what actually delivers the
  watts you're paying for
- Decoding wattage labels (what does 30W vs 65W vs 140W actually mean
  for a given device class)
- Sorting a cable drawer: which cables are 3A, which are e-marked 5A,
  which are charge-only junk
- Checking whether a phone with proprietary fast-charge (VOOC/SCP
  families) will fast-charge on standard PD gear (spoiler: no)

Don't use for: Thunderbolt/USB4 data speeds (40Gb/s is a data-chain
question, different math), MagSafe/Qi wireless (different physics),
or USB-A legacy charging (5V-only world, no negotiation).

## The Rules (memorize these five)

1. **PD fixed steps:** 5/9/15/20V (SPR), extended to 28/36/48V only
   under PD 3.1 EPR. Power = V × A at the negotiated step.
2. **The 3A cable wall:** without an e-marker chip (or explicit 5A
   rating), a cable caps at 3A → **60W max** (20V × 3A). This is the
   single most common 65W+ laptop undercharge cause.
3. **EPR needs an EPR cable:** 140W/240W only works over a
   50V-rated cable; a 100W e-marked cable won't carry EPR.
4. **Charge-only cables can't negotiate.** PD handshakes live on the
   data lines; a charge-only cable = dumb 5V mode forever. Classic
   hidden trap in cheap multipacks and some KVM/dock paths.
5. **Proprietary ≠ PD.** VOOC/SuperVOOC/SCP devices charge at ~10-27W
   on standard PD chargers regardless of the brick's rating; the
   full 65W+ rate only exists on the vendor's own charger+cable pair.

## Workflow

1. Identify the three links (device archetype, charger wattage +
   protocols, cable type). Labels and original packaging beat
   memory; assume the worst for unmarked cables (3A, no e-marker).
2. Get the verdict:
   ```bash
   python3 scripts/pd_compatibility_checker.py check \
       --device laptop-ultrabook --charger 30w-pd --cable 5a-emarked
   ```
   Output names the negotiated watts, the device's full/min needs,
   and the verdict: **OK** (full rate) / **CAPPED** (works, below
   max — fine overnight) / **SLOW** (device throttles or refuses) /
   **NO-CHARGE** (5V fallback at best).
3. Decode wattage marketing:
   ```bash
   python3 scripts/pd_compatibility_checker.py watt --watts 65
   ```
   prints the V×A operating points and the device-class meaning.
4. Browse the archetype tables:
   ```bash
   python3 scripts/pd_compatibility_checker.py table
   ```
5. Buy the fix in this order: e-marked 5A cable (cheapest big win
   for 65-100W), then adequate brick, then EPR cable only for
   140W+ laptops.

## Verdict Semantics

| Verdict | Meaning | Action |
|---------|---------|--------|
| OK | ≥ device full-speed watts | none |
| CAPPED | between min and full | fine for overnight; upgrade if you need daytime top-ups |
| SLOW | above zero but below device min | device throttles / battery may still drain under load |
| NO-CHARGE | no common PD contract | replace the broken link (usually the cable) |

## Common Pitfalls

1. **Blaming the charger first.** The cable is the culprit more often
   than the brick — a 3A cable silently caps a 100W setup to 60W.
2. **"USB-C to USB-C, so it's fine."** Connector shape says nothing
   about e-markers, EPR rating, or data lines. Test, don't assume.
3. **Trusting wattage stickers on multi-port chargers.** "65W" often
   means 65W *total, single port* — split across ports it can be
   45+18 or worse. Check per-port specs.
4. **Assuming proprietary phones fast-charge on PD.** They don't;
   expect standard-PD rates (~18-27W) on any third-party brick.
5. **Buying 240W EPR cables for everything "to be safe."** Fine, but
   EPR cables cost more and older (pre-3.1) devices can't use the
   headroom; a certified 100W e-marked cable covers 99% of gear.
6. **Charging a laptop through a dock/hub port.** Every hop adds
   negotiation and current caps; dock "PD passthrough" is often
   60-90W even when the dock's brick is bigger.

## Verification Checklist

- [ ] Device archetype confirmed (full-speed and min watts known)
- [ ] Charger per-port (not total) wattage identified
- [ ] Cable current rating checked (e-marker/5A print on jacket)
- [ ] Charge-only suspicion ruled out (does the cable transfer data?)
- [ ] Re-run the check after any swap — verify the negotiated watts
      actually moved (some devices report charge rate in settings)

## One-Shot Recipe: diagnose "slow laptop charging"

```bash
python3 scripts/pd_compatibility_checker.py check \
    --device laptop-performance --charger 100w-pd --cable 3a-standard
# -> CAPPED at 60W of 100W: the cable. Buy e-marked 5A, re-check.
```
Check the OS battery/charge readout after swapping — the negotiated
number should jump within seconds of replug.
