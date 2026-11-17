---
name: instagram-carousel
version: 1.1.0
description: Create high-performing Instagram carousels with Canvora — right format, right slide count, hook-first content shaping, and the correct refine workflow. Use when the user wants an Instagram carousel, multi-slide IG post, swipe post, or educational/listicle content for Instagram.
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"🎠","requires":{"bins":["canvora"],"env":["CANVORA_API_KEY"]}}}
---

# Instagram Carousel Creation

Map the user's intent onto the right Canvora levers. Canvora's carousel
pipeline owns the design *execution* — layout, composition, imagery, visual
variety per slide. Your job is the content and the parameters. Setup, credits,
and general CLI usage: see the `canvora` skill.

## Intake — ask only what you can't infer

Usually you already know the topic. Then you need at most two more things:

1. **How many items?** ("5 tips" → 5, plus a cover if they want one). If they
   don't say, use 6.
2. **Whose brand?** If a client/company is named → `canvora brands --json` →
   `--brand`. If they have no kit, don't ask again.

Anything else — style, language, CTA — infer it and state your assumption in
one line when you report back. Do not run a questionnaire.

## The rule that matters

**Don't art-direct slide by slide.** Do not prescribe per-slide layouts, color
values, or illustration details; over-specified briefs fight the tuned format
pipeline and produce worse, samey output.

**But do carry the user's stated look.** If they said "black and white with big
type" or "hand-drawn", pass it through as one line of overall direction. It is
honoured, and dropping it is the more common and more damaging mistake. The
line is: *overall aesthetic = yes, slide-by-slide instructions = no.*

## Parameter mapping (your actual job)

| User intent | Lever |
|---|---|
| Any IG carousel | `--format instagram_carousel_portrait` (1080×1350 — outperforms square for reach). Square (`instagram_carousel`) only if they ask for it. |
| "N tips/mistakes/steps" | `--slides instagram_carousel_portrait=N` (or N+1 with a cover). Never leave a promised count unmatched. No count promised → 6. |
| A named client or brand | `canvora brands --json` → `--brand <uuid>`. Mandatory when a kit exists. Add `--logo` to actually stamp the logo. |
| Tone words | `--style`: educational/punchy → `bold`; clean/professional → `modern` or `minimal`; luxury/coaching → `elegant`; consumer/fun → `playful`. |
| No tone signal at all | `--style modern`. Note: omitting the flag does NOT auto-pick — it pins `modern` anyway. Choosing deliberately is free. |
| "End with a follow/save CTA" | `--cta` (final slide becomes the call to action) |
| Exact wording required (quotes, taglines) | `--input "..." --exact` |
| User gave a topic only | `--idea` (Canvora develops the substance) |
| User gave finished content | `--input` (wording respected) |

## Content shaping (what goes IN the brief — copy craft, not design)

- **Hook first:** phrase the idea as the specific promise the cover should
  carry — "5 client-content mistakes that kill engagement", not "content
  mistakes". Numbers and specificity win.
- **One idea per item:** if using `--input`, structure it as a clean list
  (item = one point, ≤25 words). The pipeline maps items to slides.
- **End intent:** if they want a save/follow CTA, use `--cta` rather than
  describing it in prose.

```bash
ID=$(canvora generate \
  --idea "5 client-content mistakes that kill engagement — for freelance social media managers" \
  --format instagram_carousel_portrait --slides instagram_carousel_portrait=6 \
  --brand $BRAND_ID --logo --style bold --cta | head -1)
canvora status "$ID" --json    # repeat every ~30s until completed
```

- A carousel is always 3+ outputs, so fire-and-poll — never `--wait`, which
  your harness usually kills at 120s while the generation carries on
  server-side. Never re-run `generate` after a timeout; poll `status`.
  Detail in the `canvora` skill's "Long runs" section.
- State the cost in the same message as the run — 15 credits per slide, so the
  6-slide carousel above is 90. Announce it, don't ask permission. Confirm the
  *number* only when you picked it (the 6 default), not when they said "5 tips".

## After generation

- **Sort outputs by `sortOrder`** before presenting or posting — outputs can
  complete out of order.
- **`partial` status?** Some slides were blocked or failed and those credits
  were refunded. Say so, and offer to re-run the missing slides — don't hand
  over a 4-slide carousel that was meant to be 6 without explaining.
- **Different look wanted?** `canvora variations <id>` — fresh takes from the
  pipeline (15 credits per slide). Do NOT regenerate with a more prescriptive brief.
- **One slide needs a fix?** `canvora edit <outputId> --prompt "..." --yes` —
  targeted, design preserved, 3 credits. Always the first thing to try.

## Quality checklist

- [ ] Portrait format; slide count matches the promised item count
- [ ] Brand kit applied when one exists (`--brand`, plus `--logo` if they want the mark)
- [ ] Brief carries hook + content items + the user's stated look — no invented art direction
- [ ] Style chosen deliberately, not left to default
- [ ] Outputs sorted by `sortOrder`; partials reported
- [ ] Revisions via `edit` (3 cr) or `variations`, never regeneration
