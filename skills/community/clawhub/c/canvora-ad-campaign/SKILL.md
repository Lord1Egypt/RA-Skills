---
name: ad-campaign
version: 1.0.0
description: Produce paid ad creative sets with Canvora — Meta, Instagram, LinkedIn, Google Display and banner placements in one pass, with variants for testing. Use when the user wants ads, ad creative, paid social assets, display banners, or a campaign creative set.
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"📣","requires":{"bins":["canvora"],"env":["CANVORA_API_KEY"]}}}
---

# Ad creative sets

Ads fail on placement coverage and on having only one creative to test. Canvora
fixes both cheaply: every placement from one source in a single call, then
variants from the winner. Setup and credits: see the `canvora` skill.

## Placement map

| Format | Size | Placement |
|---|---|---|
| `ad_square` | 1:1 | feed (Meta, LinkedIn, the safe default) |
| `ad_portrait` | 9:16 | stories, reels, vertical video slots |
| `ad_landscape` | 16:9 1200×628 | link ads, in-stream, LinkedIn sponsored |
| `ad_banner` | 21:9 728×90 | classic leaderboard display |
| `google_display` | 1200×628 | Google Display Network |

**Full coverage = `ad_square,ad_portrait,ad_landscape`** — three placements,
30 credits, one consistent look. Add `ad_banner`/`google_display` only if they
actually run display.

Ads are 10 credits per creative. Say the total in the same message as the run —
announce it, don't ask permission; if you decided the number of angles yourself,
confirm that number. A campaign is several sequential calls, so **sum the whole
plan and run `canvora credits --json` once before you start**: running dry
halfway leaves a half-covered campaign with the earlier calls already paid for.
Any single call producing 3+ creatives should fire-and-poll rather than `--wait`
— most harnesses kill a shell command at 120s while the generation carries on
server-side, and re-running `generate` starts a second, separate job. See the
`canvora` skill's "Long runs" section.

## Intake

1. **What's being advertised?** A product URL is the best input — it carries
   the offer, the proof and the brand voice. Otherwise the offer in one line.
2. **Where does it run?** Meta/IG → square + portrait. LinkedIn → square +
   landscape. Google Display → `google_display` + `ad_banner`. Unsure → the
   three-format set.
3. **Brand kit** — `--brand` + `--logo`. Ads without the mark waste the spend.
4. **The offer/CTA** — "20% off first order", "Book a demo". Put it in the
   brief and pass `--cta`.

## The canonical runs

```bash
# Full placement coverage from a product page (3 outputs — fire and poll)
ID=$(canvora generate --url https://store.example.com/product \
  --format ad_square,ad_portrait,ad_landscape \
  --brand $BRAND --logo --cta --style bold | head -1)
canvora status "$ID" --json    # repeat every ~30s until completed

# Offer-led ad from a written brief
canvora generate --idea "Book a free 30-minute logistics audit — for e-commerce ops managers losing money on returns" \
  --format ad_square,ad_landscape --brand $BRAND --logo --cta --wait --json

# Display set
canvora generate --url $URL --format google_display,ad_banner --brand $BRAND --logo --wait --json
```

## Getting testable variants (do this properly)

One creative is not a campaign. Two correct ways, in order of preference:

1. **Different angles, separate calls.** Run the same format 2-4 times with
   genuinely different briefs — benefit-led, problem-led, social-proof-led,
   price-led. This produces creative diversity, which is what actually moves
   CTR. One call cannot make N distinct instances of the same format.
2. **`canvora variations <id> --count 2`** for visual re-rolls of the same
   message (10 credits per new image on single-image ad formats). Use this when
   the copy is right and only the look needs alternatives.

```bash
for ANGLE in \
  "Cut returns by 30% — the audit that finds where the money leaks" \
  "Your returns process is costing more than your ad spend" \
  "How Acme cut returns 30% in one quarter"
do
  canvora generate --idea "$ANGLE" --format ad_square \
    --brand $BRAND --logo --cta --wait --json
done
```

Rate limit is 20 generations/minute — run these sequentially with `--wait`.

## Craft notes

- **`--style bold`** is the right default for promotional creative; `elegant`
  or `dark` for premium/luxury; `minimal` for B2B SaaS.
- **Text-light wins on paid social.** Keep the offer to one line in the brief;
  platforms penalise cluttered creative and so does attention.
- **`--exact`** when legal or pricing copy must appear verbatim.
- **`--no-text`** if the team overlays their own copy in Ads Manager.
- Don't art-direct per-placement. Do pass a stated brand look once.

## Delivery

- Label each output by placement, not by index — the media buyer uploads them
  into different slots.
- Fix a headline with `edit` (3 credits) rather than regenerating a set.
- Group a campaign with `--project <uuid>` so everything stays together in the
  dashboard.

## Quality checklist

- [ ] Every placement they actually run is covered
- [ ] Brand kit + logo on every asset
- [ ] `--cta` set and the offer stated in the brief
- [ ] At least 2-3 distinct angles for anything with real spend behind it
- [ ] Outputs labelled by placement
