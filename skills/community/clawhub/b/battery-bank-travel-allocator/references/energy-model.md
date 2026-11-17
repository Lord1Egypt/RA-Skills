# The Energy Model — Losses, Devices, Activities

## Where the rated mAh goes

A 20000 mAh bank, new, in perfect conditions:

```
20000 mAh × 3.7 V            = 74.0 Wh  (cell energy, what the sticker means)
× 5 V delivery (0.74)        = 54.8 Wh  (your phone drinks at 5 V, not 3.7 V)
× conversion+cable (0.85)    = 46.6 Wh  (boost converter heat, connector, wire)
                              ────────
≈ 47 Wh realistic transfer (63% of sticker energy)
```

Add age and cycles:

| Condition | Derating | 20000 mAh delivers |
|---|---|---|
| New | none | ~47 Wh |
| 2 years old | −8% | ~43 Wh |
| 3 yr + 500 cycles | −12% −8% | ~38 Wh |
| 5 yr daily-cycled | −20% −20% (capped) | ~28 Wh — a new 10000-class bank |

Fast-charge protocols (PD, QC) add another 5–15% waste when
negotiating higher voltages, but devices charge faster; net cost is
small and ignored by the model (it's inside the 0.85).

## Device library (typical 2020s hardware)

| Device | Battery | Screen-on drain | Idle | Stop-charge |
|---|---|---|---|---|
| phone | 15 Wh (~4000 mAh) | 8%/h | 1.0%/h | 85% |
| phone-small | 11 Wh (~3000) | 9%/h | 1.2%/h | 85% |
| phone-big | 20 Wh (~5400) | 7%/h | 0.9%/h | 85% |
| tablet | 28 Wh | 6%/h | 0.6%/h | 90% |
| camera | 12 Wh | per-shot model | — | 100% |
| earbuds (case) | 1.5 Wh | — | — | 100% |
| watch | 1.2 Wh | — | 2%/h | 90% |
| laptop-usb (PD) | 60 Wh | 9%/h | 1.5%/h | 80% |
| drone battery | 30 Wh | swap-based | — | 100% |

Camera/drone drain is usage-shaped (shots, GPS logging, screen
preview minutes) — model via screen-hours as a rough proxy
(`camera:2:50:video` ≈ 2 h of active preview/shooting).

## Activity multipliers (applied to screen-on rate)

| Activity | Multiplier | Why |
|---|---|---|
| light (messaging, reading) | 1.0 | baseline |
| offline-maps | 1.8 | GPS + screen, no radio hunting |
| photos | 1.6 | ISP + screen bursts |
| video playback | 2.5 | decode + bright screen |
| hotspot | 2.8 | radio TX at duty |
| navigation (online) | 3.5 | GPS + screen + data + compute |
| gaming | 4.0 | GPU + SoC sustained |

Airplane mode + offline maps turns a 3.5× navigation day into a
1.8× offline-maps day — the single biggest lever in the model.

## Idle/background reality

- Radios on, good signal: ~1%/h
- Radios on, poor signal (festival, subway, backcountry): 2–3%/h —
  the phone boosts power hunting for towers
- Airplane mode: ~0.3%/h
- Overnight in a cold tent: cold increases apparent drain (see below)

## Cold-weather derating (hiking/ski)

Li-ion chemistry delivers less below ~10 °C and refuses below 0 °C:
at −5 °C expect 20–40% less usable energy from the same bank, and
keep the bank in an inner pocket (body heat) — phone in outer pocket
dies first, then "recovers" when warmed. The model doesn't take a
temperature flag; multiply your margin manually.

## Airline rules (carry-on)

- Banks ≤ 100 Wh (≈27000 mAh at 3.7 V): fine, no approval
- 100–160 Wh: airline approval often required (many airlines refuse anyway)
- > 160 Wh: prohibited
- Always carry-on, never checked; caps on quantity (usually 20
  batteries) rarely bind travelers

## Charge-order tactics on the day

1. Priority device to 85% first, while the bank is fresh and cool
2. Devices near their idle-only profile can wait — charge them during
   the commute home, not at lunch
3. A 30-min top-up mid-day (lunch wall plug) removes ~15 Wh of demand
   from the bank — often the difference between FITS and SHORTFALL
4. Turn OFF charging-through (bank pass-through) — it adds a
   conversion loss; charge devices from the bank directly
