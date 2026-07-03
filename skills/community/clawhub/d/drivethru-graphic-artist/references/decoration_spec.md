# Decoration spec — real-world print sizes & placements

Ground-truth print dimensions from the **Bacon & Co. Recommended Garment &
Accessory Decoration Guide** (`assets/decoration_guide.png` — the canonical
placement diagram; open it when you need to see where a location sits). Use
this as the reference the [self-review loop](self_review.md) judges against, so
"correct" means *industry-standard*, not a guess.

## Why inches map cleanly to our ratios

The spec is in inches and split adult/youth; our rules are ratios of the
detected garment bbox. Those are two views of the same thing: youth full-front
(9″) ÷ adult full-front (13″) ≈ 0.69, and youth garments run ~0.69 the width of
adult — so **one ratio reproduces both columns automatically**. That's the
whole reason the model is ratio-based; the spec validates it. What the spec
pins down that a lone ratio can't is the *proportion between placements* (a left
chest is ~¼ the width of a full front) and *height caps* (a hoodie front must
clear the pocket).

## Print dimensions (adult / youth), width unless noted

| # | Location | Adult | Youth | Frac of full-front width |
|---|---|---|---|---|
| 1 | Full front | 13″W | 9″W | 1.00 (the anchor) |
| 2 | Center chest | 3–5″W | 3″W | ~0.31 |
| 3/4 | Right / left chest | 3–4″W | 3–4″W | ~0.27 (pocket-sized) |
| 5 | Pocket | 3″W × 3″H | 3″W × 3″H | ~0.23, square |
| 6 | Full back | 13″W | 9″W | 1.00 (= full front) |
| 7 | Upper back | 10–13″W | 7–9″W | ~0.88 |
| 8 | Tag | 3–4″W | 3–4″W | ~0.27, high under collar |
| 9 | Lower back | 10–13″W | 7–9″W | ~0.88, low |
| 10/11 | Sleeve (short) | 3–4″W | 3″W | ~0.27 |
| 12/13 | Sleeve (long) | 3.25″W × **12″H** | 3″W × 9″H | ~0.25, height-dominant |
| 14 | Full front (hoodie) | 13″W × **9″H** | 9″W × 6″H | 1.00 width, **9″H cap (pocket)** |
| 15/16 | Left / right chest (polo) | 3–4″W | 3″W | ~0.27 |
| 23 | Drawstring backpack | 11–12″W | — | large, centered panel |
| 24 | Hat front | 2.5″H max (high) / 2″H (low) | — | **height-capped**, width varies |
| 25 | Hat back | 1.25″H max | — | small |
| 26 | Hat side | 2″W max | — | small |
| 27 | Visor front | 1.5″H max (high) / 1″H (low) | — | small |

Embroidery floor: lettering ≥ 0.25″H and 2 mm stroke — a mark that renders
below that in the mockup is too small to actually sew.

## How this shaped the shipped ratios

`assets/placement_rules.json` was reconciled to the proportions above:

| Placement | Was | Now | Why |
|---|---|---|---|
| left/right chest (all cats) | 0.18 | 0.14–0.15 | 3–4″ is ~¼ of a 13″ full front — pocket-sized, not 1/3 |
| full_back | 0.55–0.60 | 0.50–0.55 | spec sizes full back = full front (both 13″) |
| back_yoke / upper back | 0.40 | 0.44 | spec upper back ~10–13″ ≈ 0.88 of full front |
| sleeve | 0.12 | 0.14 | spec sleeve 3–4″ ≈ 0.27 of full front |
| hoodie full_front | 0.55 | 0.55 + `max_height_ratio 0.33` | 13″×9″ box — cap height so tall art clears the pocket |

Full front, hat, and mug were left as-is (full front already matched; hats are
height-capped in ways the width-ratio model doesn't govern; no mug on the
sheet).

## Caveats when reading the sheet

- **Absolute inches need a bbox width to become a ratio**, and the detected
  bbox varies with the photo (a worn hoodie's silhouette includes sleeves; a
  flat-lay tee doesn't). So trust the *proportions between locations* over any
  single inch→ratio conversion.
- **"may vary based on artwork"** — the sheet says so itself. These are
  recommended maxes/typicals, not hard law. The self-review loop should treat
  them as the target to land near, then defer to what looks right on the
  specific garment.
- **Height caps are estimates in ratio terms.** The hoodie 9″ pocket line ≈
  0.33 of a ~27″ body bbox; if a specific blank is cropped differently, the cap
  may need a nudge. It only ever scales art *down* to fit, never up.
