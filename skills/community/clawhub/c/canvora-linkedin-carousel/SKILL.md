---
name: linkedin-carousel
version: 1.0.0
description: Create LinkedIn document carousels and post visuals with Canvora — correct aspect ratio, safe zones for LinkedIn's UI chrome, B2B content shaping. Use when the user wants a LinkedIn carousel, document post, swipe post for LinkedIn, or B2B thought-leadership visuals.
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"💼","requires":{"bins":["canvora"],"env":["CANVORA_API_KEY"]}}}
---

# LinkedIn carousels and post visuals

LinkedIn's document carousel is the highest-reach organic format on the
platform, and it has one detail everyone gets wrong: the bottom of every slide
is covered by LinkedIn's own UI. Canvora's LinkedIn formats declare safe zones
for exactly this. Setup and credits: see the `canvora` skill.

## Format choice

| Format | Ratio | Bottom safe zone | Use |
|---|---|---|---|
| `linkedin_carousel_portrait` | 4:5 | 60px | **the default** — most feed space per swipe |
| `linkedin_carousel` | 1:1 | 60px | when their existing template is square |
| `linkedin_carousel_vertical` | 9:16 | 80px | mobile-first, maximum height |
| `linkedin_post` | 16:9 1200×627 | — | single-image post |
| `linkedin_article` | 16:9 1920×1080 | — | article header |

Default to `linkedin_carousel_portrait` unless the user says otherwise. All
three carousels are 15 credits per slide. State that cost in the same message
as the run (a 7-slide carousel = 105) — announce it, don't ask permission. If
*you* chose the slide count rather than the user, confirm that number with them.

## Intake

1. **What's the point of view?** LinkedIn rewards a stance, not a summary. Get
   one sentence of opinion, not a topic.
2. **How many slides?** 6-8 is the sweet spot; match any promised count. Max 10.
3. **Personal brand or company brand?** Company → `--brand` + `--logo`.
   Personal/founder posts often read better without a logo on every slide.
4. **Is there a CTA?** Newsletter, demo, comment-bait → `--cta`.

## The canonical run

```bash
ID=$(canvora generate \
  --idea "Most B2B pipelines die at handoff, not at close — 6 fixes for the sales-to-CS transition" \
  --format linkedin_carousel_portrait --slides linkedin_carousel_portrait=7 \
  --brand $BRAND --style minimal --cta | head -1)
canvora status "$ID" --json    # repeat every ~30s until completed
```

From content the user already wrote (a post, a newsletter section):

```bash
ID=$(canvora generate --input "$POST_TEXT" \
  --format linkedin_carousel_portrait --slides linkedin_carousel_portrait=6 \
  --brand $BRAND | head -1)
canvora status "$ID" --json
```

Both are 3+ outputs, so fire-and-poll rather than `--wait` — most harnesses
kill a shell command at 120s while the generation carries on server-side. Never
re-run `generate` after a timeout; that starts a second, separate job. Poll
`status`. See the `canvora` skill's "Long runs" section.

## Content shaping for LinkedIn specifically

- **Slide 1 is a claim, not a title.** "Your pipeline is leaking at handoff"
  beats "Sales to CS handoff". The cover decides whether anyone swipes.
- **One idea per slide, in professional register.** No hype, no emoji walls.
  `--style minimal` or `corporate` matches the room; `bold` only for
  contrarian/opinion posts.
- **Keep text off the bottom edge.** The pipeline handles the safe zone, but
  don't request bottom-anchored text — LinkedIn's UI will cover it.
- **Last slide earns the follow.** `--cta`.
- **Don't art-direct slide by slide.** Do carry a stated brand look through.

## After generation

- **Sort by `sortOrder`**, then upload as a *document* post (PDF) — that is
  what LinkedIn treats as a carousel. MCP clients can produce the PDF directly:
  `export_visuals(generation_id, format: "pdf")`. CLI users download the images
  and export from the Canvora dashboard.
- **Also write the post caption** — the visuals don't carry the algorithm, the
  first two lines of the caption do. That's your job, not Canvora's.
- Fix one slide with `edit` (3 credits), never a full regeneration.

## Quality checklist

- [ ] Portrait 4:5 unless the user's template says otherwise
- [ ] Cover states a claim; 6-8 slides; count matches any promise
- [ ] Professional register; `minimal`/`corporate` unless the take is contrarian
- [ ] `--cta` when there's an ask
- [ ] Delivered as a PDF document post, slides in `sortOrder`
- [ ] Caption written alongside the visuals
