# USB-C Power Delivery Reference

## The chain

Fast-charge power is negotiated, not assumed. Three links, weakest
caps everything:

```
Charger (PDOs it offers)  x  Cable (amps it can carry)  x  Device (RDOs it requests)
```

The charger advertises power data objects (PDOs); the device picks
one and states its draw (request data object). The cable participates
**passively**: its e-marker chip (or lack thereof) tells the source
what current is safe. If any link lies or is missing, power falls
back — usually to 5V/3A (15W) or plain 5V/500mA-2.4A.

## PD revisions and voltage steps

**PD 2.0 / 3.0 (SPR — Standard Power Range):**

| Step | Max current | Power |
|------|------------|-------|
| 5V   | 3A          | 15W   |
| 9V   | 3A          | 27W   |
| 15V  | 3A          | 45W   |
| 20V  | 5A          | 100W  |

**PD 3.0 PPS:** programmable voltage in 20mV steps + current in 50mA
steps — the direct-current control that Qualcomm-class proprietary
protocols historically offered. PPS is how flagships (Galaxy, Pixel
Pro) hit 25-45W efficiently with less heat.

**PD 3.1 EPR (Extended Power Range):**

| Step | Max current | Power |
|------|------------|-------|
| 28V  | 5A          | 140W  |
| 36V  | 5A          | 180W  |
| 48V  | 5A          | 240W  |

EPR requires an **EPR-rated cable** (50V insulation, advertised as
240W) AND both ends speaking PD 3.1. A 100W e-marked cable refuses
EPR (the source reads the cable's rating and clamps to SPR).

## Cable taxonomy (what's actually in the drawer)

| Cable type | Current cap | Max power | Notes |
|-----------|------------|-----------|-------|
| Unmarked bargain | assume 3A | 60W | often no e-marker even when 5A-capable |
| Standard USB-C (certified) | 3A | 60W | the default assumption |
| E-marked / "5A" printed | 5A | 100W | required for >60W |
| EPR / "240W" printed | 5A + 50V | 240W | backward compatible, costs more |
| Charge-only (no data lines) | varies | ~0W PD | PD needs CC/data negotiation; dead end |

The e-marker is a tiny chip in the connector that answers the
source's query about cable capability. Cable jackets print "5A" or
"240W" when rated; absence of print = assume 3A.

## Device archetype appetite table

| Archetype | Full speed | Below this = throttle/refuse |
|-----------|-----------:|------------------------------:|
| earbuds / tiny battery | 5W | 2.5W |
| basic phone | 18W | 10W |
| flagship phone (PD/PPS) | 30W | 15W |
| proprietary phone (VOOC/SCP) | 65W* | 15W (*proprietary only) |
| iPhone Plus/Pro Max | 27W | 15W |
| tablet | 35W | 18W |
| handheld console (Steam Deck) | 45W | 30W |
| ultrabook 13-14" | 65W | 45W |
| performance laptop 15-16" | 100W | 65W |
| gaming laptop 16"+ | 240W* | 100W (*often proprietary barrel/EPR) |
| camera body | 15W | 9W |

"Min" is where behavior degrades: phones trickle, laptops charge
slowly or still drain under load (common 65W-brick-on-gaming-laptop
complaint).

## Proprietary protocol landscape (why the box says 80W but PD gives 27)

- **VOOC / SuperVOOC / Dash (OPPO/OnePlus/realme):** proprietary
  high-current-at-low-voltage over special cables. On standard PD
  these devices negotiate ~18-27W. Full rate only with the vendor's
  charger AND vendor's cable (the cable carries extra pins/chip).
- **SCP / FCP (Huawei):** same story; ~22W on PD.
- **QC 2.0/3.0/4+ (Qualcomm):** QC4+ is PD-compatible, older QC is
  not; most modern phones fall back to PD gracefully.
- **Apple:** plain PD (no proprietary wired protocol since 18W era);
  MagSafe is wireless and separate.
- **Steam Deck / ROG Ally etc.:** standard PD but large appetite;
  Ally X and gaming handhelds benefit from 65-100W PD bricks.

## Multicast traps in multi-port chargers

"100W charger" with 3 ports usually means:

- single-port use: 100W
- two ports: 65W + 30W (or 45+45)
- three ports: 45 + 30 + 25 or similar

The split changes as devices plug/unplug, renegotiating every time.
If a laptop mysteriously drops to 60W when a phone is plugged in —
that's the port-power budget, not a fault. Check the spec sheet's
per-combination table.

## Buying guidance (2026 market)

1. One good **100W 2-port GaN** charger + one **e-marked 100W cable**
   covers phone + tablet + ultrabook travel kits.
2. For 140W+ laptops: the OEM brick or a certified EPR set (charger
   AND cable both rated).
3. Avoid: unbranded multipack cables (charge-only rate high), any
   charger without UL/IEC 62368 marking, "240W" cables from
   marketplace sellers with no certification print.
4. Cables fail by heat-cycling at connectors; a 2-year-old daily
   driver cable delivering less than it used to is normal — retest
   with the `check` mindset.

## Measurement and verification

- OS readouts: macOS System Information → Power shows negotiated
  wattage live; Windows OEM apps often show it; Android shows
  "Charging rapidly" vs "Charging".
- Hardware: a $15 USB-C PD trigger/tester displays the active
  contract (V/A) — the definitive answer for drawer-sorting.
- Empirical test: 30 minutes on the suspicious chain vs a known-good
  one; compare % gained. A 60W cap vs 100W is visible in 30 min.

## Safety notes

- EPR at 48V is genuinely higher-energy; use only certified cables.
- Never bypass a damaged connector (bent pins can short VBUS).
- Hot connectors during negotiation = disconnect and retire the
  cable; PD includes overtemp protection but repeated trips indicate
  a failing e-marker or worn contacts.
