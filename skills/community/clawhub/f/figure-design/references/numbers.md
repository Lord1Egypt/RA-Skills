# Numbers Reference

Load this file whenever a quantitative decision is required: scale selection, price band, tolerance, mold economics, coating parameters.

All values are for **1/12 – 1/4 collectible figures** unless stated otherwise. Quote them as ranges, not point values — factory processes differ.

## 1. Scale → Height → Detail Budget → Price

| Scale | Height | Detail budget (recognition points) | Typical product | Price band (CNY) |
|---|---|---|---|---|
| 1/12 | 12–15 cm | ≤3 | action figures, chibi, blind box | 59–199 |
| 1/10 | 16–18 cm | 3–5 | prize figures, entry static | 99–299 |
| 1/8 | 20–24 cm | 5–7 | mainstream static | 399–999 |
| 1/7 | 22–26 cm | 6–8 | premium / limited static | 600–1500 |
| 1/6 | 28–32 cm | 8–10 (fabric, rooted hair possible) | high-end articulated, military | 1200–3000 |
| 1/4 | 40–45 cm | 10–12 | large-scale collectible | 2000–5000 |
| 1/3 and up | 50 cm+ | unbounded; material is the selling point | statue, silicone articulated | 5000+ |

Notes:
- Height varies even at the same scale: a 168 cm character at 1/7 is ~24 cm, but hair, pose, and base routinely push finished height to 22–27 cm. A seated 1/6 can be shorter than a standing 1/7. Never quote scale alone as a space requirement.
- The detail budget is empirical: 8 details on a 1/12 produce 8 smeared details, not 8 details.

## 2. Tolerance and Structure

| Item | Value | Note |
|---|---|---|
| Wall thickness, PVC / 搪胶 | 2.5–4 mm | max/min ratio ≤1.3 |
| Wall thickness, hollow resin | 1.5–2 mm | drain holes mandatory |
| Peg / socket clearance | 0.25–0.3 mm | static fit |
| Moving parts (ball joint, hinge) | 0.2–0.5 mm | too tight won't assemble, too loose wobbles |
| Magnet pocket diameter | magnet Ø + 0.2–0.3 mm | |
| Magnet pocket depth | magnet thickness + 0.2 mm | leave a 0.3–0.5 mm glue cap above the face |
| Magnet pocket wall | ≥1.2–1.5 mm | thinner and it breaks through |
| Pocket chamfer | 0.3 mm | eases insertion |
| Draft angle | 1–3° | take the larger value on textured surfaces |
| Ball joint diameter | 15–20% thicker than the limb | otherwise it shows when rotated |
| Thin parts (ribbons, hair tips) | ≥1 mm, or thicken and add wire | else breaks in printing and shipping |
| Detail depth floor | FDM ≥1 mm · resin ≥0.3 mm | below this it does not render |

## 3. Molds and Lead Time

| | Silicone mold (resin / GK) | Steel mold (PVC / ABS) |
|---|---|---|
| Life | 20–50 casts | tens of thousands of cycles |
| Cost | roughly 1/10 of steel | hundreds to thousands USD per cavity |
| MOQ | ~100 pcs | ~1000 pcs to be economic |
| Mold build | 2–5 days | 15–30 days |
| Total lead time | ~5–8 weeks | ~8–14 weeks |
| Use | market test, limited, art pieces | mass production, licensing, retail |

Typical schedule breakdown (resin, ≤500 pcs): sculpt + digitize 7–14 d · DFM + prototype 7–12 d · silicone tooling 2–5 d · production + paint 10–20 d · QC + pack 5–10 d.

Peak-season paint queuing adds 2–3 weeks. Book the paint line three weeks ahead.

## 4. Coating Parameters

| Parameter | Value |
|---|---|
| Surface prep | 1000–1500 grit wet sand; alcohol wipe to remove release agent |
| Primer | grey filler for dark parts, white for light parts; two thin coats |
| Pre-shade | spray dark into recesses, gun distance ~20 cm |
| Base color | three thin passes, 10 min apart, gun distance 15 cm |
| Air pressure | 0.8–1.2 kg/cm² |
| Thinner ratio | 1:2.5 |
| Highlight | 45° oblique, low pressure, small flow |
| Panel line | enamel thinned to milk consistency, 000 brush, wipe overflow after drying |
| Clear coat | matte by cross-hatch passes; gloss in two thin coats |
| Cure before handling | 48 h |
| Face, hand-painted | ~2 days per face |
| Face, water-slide decal | ~3 hours, ~80% of the effect |

## 5. Color Control

| Rule | Value |
|---|---|
| Color blocks per figure | ≤4 (counting black and white) |
| Split | base 60% / secondary 25% / accent 15% |
| Color matching | lock Pantone or factory code + written formula |
| Batch tolerance | agree ΔE limit with the factory before tooling; photograph against the golden sample |
| Every added block | +1 process step, +1 drift risk |

## 6. Cost Model

| Line | Note |
|---|---|
| Material + processing | per part, scales with part count and size |
| Paint | hand airbrush can be 3–5× pad printing |
| Packaging | window box / blister / gift box differ by ~3× |
| Mold amortization | mold cost ÷ first batch quantity |
| Returns / defects reserve | 5–8% |
| **Target gross margin** | **≥3× total unit cost** to be viable at retail |

If the margin cannot reach 3×, the scale was chosen wrong. Return to T0 and reduce ratio, part count, or paint complexity — do not silently cut accessories.

## 7. QC

| Item | Standard |
|---|---|
| Sampling | AQL 2.5 for consumer collectibles |
| Gates | incoming material · first-article + patrol · final |
| Drop test | 1 m, six faces, packaged |
| Batch color check | side-by-side photo against golden sample, archived |
| Golden sample archive | physical + six-view photos + color codes — all three |

## 8. IP / Compliance

- Blind boxes: no sale to children under 8; sale to 8+ requires guardian consent; disclose draw rules, probabilities, and quantities; a single unit price is encouraged to stay at or below ¥200.
- Magnetic parts: avoid detachable small magnets in child-directed lines; EN71 / CPSIA small-parts compliance.
- Licensed IP: three review nodes (spec sheet → unpainted prototype → painted sample); budget review rounds into the schedule.
