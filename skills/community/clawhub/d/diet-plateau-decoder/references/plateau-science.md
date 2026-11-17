# Diet Plateau Decoder — Reference

## 1. The signal problem

Daily body weight = fat mass change (slow, ~0.1 kg/day max on sane diets) +
water (fast, ±1–2 kg) + gut content (±0.5 kg) + glycogen (±1 kg with 3:1
water binding). The thing you care about is 5–10× smaller than the noise.
Hence:

- **7-day rolling average** is the minimum honest unit of measurement.
- A judgment needs **≥14 days** — masks routinely last 10–14 days (new
  training, luteal phase).
- The trend-over-noise ratio (skill output) should exceed ~2 before you
  believe any direction.

## 2. Energy arithmetic (sanity anchors)

- 7700 kcal ≈ 1 kg fat; 3500 kcal ≈ 1 lb (Wishnofsky heuristic; real-world
  slightly less neat — dynamic models like NIH Body Weight Planner add
  adaptation).
- A 500 kcal/day deficit ≈ 0.45 kg/wk *at first*; as weight falls, TDEE
  falls (smaller body + NEAT adaptation ~5–15% over months).
- Weekend math: −500 × 5 weekdays +400 × 2 weekend days = −1700/wk ≈ a
  0.22 kg/wk rate — less than half the intended 0.45, indistinguishable
  from a "plateau" on the scale for weeks.

## 3. Water-retention mechanisms (magnitudes)

| Mechanism | Size | Duration | Resolution |
|---|---|---|---|
| Sodium spike | +0.3–1.2 kg | 1–3 days | renal excretion |
| New training / return to lifting | +0.5–2 kg | 1–2 wks | repair completes |
| Luteal phase (PMS) | +0.5–2 kg | 5–10 days | with menses |
| Carb refeed after keto/low-carb | +0.5–1.5 kg | 2–4 days | glycogen stabilizes |
| Cortisol (sleep <6h, stress) | +0.3–1 kg | while chronic | sleep/stress fix |
| Creatine loading | +0.5–1 kg | ongoing | steady state |
| Alcohol | −0.5 then +0.3–1 kg | 1–2 days | rebound |

The "whoosh" folk term describes the resolution day when masked fat loss
appears at once — usually 2–7 days after the flag clears.

## 4. True-plateau differential (in order of likelihood)

1. **Intake creep** — portions grow 10–20% after ~6 weeks of logging
   fatigue; oils, sauces, "bites". Re-weigh everything for 2 weeks.
2. **TDEE shrink** — recalibrate: TDEE ≈ weight × activity factor; a
   90→78 kg loss mechanically removes ~150–250 kcal/day.
3. **NEAT collapse** — dieting reduces spontaneous movement (fidgeting,
   walking pace) before it reduces anything else; step counters catch it.
4. **Weekend structure** — see arithmetic above.
5. **Actual adaptive thermogenesis** — real but ~50–150 kcal/day magnitude;
  it *contributes*, it rarely *alone* explains a full stall.
6. **Recomposition** — novice/returning lifters gain muscle while losing
   fat; scale flat, waist shrinking. Measure the waist.
7. **Medical** — hypothyroidism, PCOS, meds (SSRIs, antipsychotics,
   steroids, insulin). If the log is truly clean for 4+ weeks, labs.

## 5. What NOT to do on a mask

- Cut another 300 kcal (stacks deprivation onto a phantom problem; rebound
  risk).
- Add cardio punishment (raises cortisol/appetite; NEAT drop elsewhere).
- Sauna/diuretic/water-load games (moves water for hours, teaches nothing).
- Switch diets (the mask follows you to the new diet; the switch *looks*
  like it worked when the old mask resolves).

## 6. Evidence notes

- Daily self-weighing shows *better* maintenance outcomes in RCTs (e.g.,
  Wing/Leonard studies) — the trend unit makes daily data non-triggering.
- Diet breaks at maintenance (MATADOR trial) preserved resting metabolic
  rate vs continuous restriction and improved adherence signals.
- Refeeds/diet breaks are psychological + behavioral tools; the "metabolic
  reset" framing outruns the evidence, but adherence is the real mechanism
  and it's enough.

## 7. Measurement protocol (collect clean data)

1. Morning, post-bathroom, pre-food/drink, same scale, same spot (floors
   differ), minimal clothing.
2. Log to the app same-minute; never "remember later" (reconstruction
   smooths exactly the outliers that carry information).
3. Record flags same-day: sodium-heavy meals, new workouts, cycle day,
   alcohol, sleep hours, travel.
4. Weekly: waist at navel, photos same lighting, gym lifts. Recomposition
   shows here first.
