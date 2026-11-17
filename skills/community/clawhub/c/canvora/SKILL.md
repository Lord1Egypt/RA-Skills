---
name: canvora
version: 1.4.0
description: Create on-brand visuals (social posts, carousels, decks, PDFs, ads, landing-page kits, infographics) from any idea, text, URL, or PDF via Canvora. 100+ formats, native generation in 150+ languages, per-client brand kits. Use when the user asks to create, generate, or design visual content for social media, marketing, presentations, or documents.
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"🎨","requires":{"bins":["canvora"],"env":["CANVORA_API_KEY"]}}}
---

# Canvora — on-brand visuals as a shell command

Canvora turns ideas, text, URLs, docs, and PDFs into finished visuals: single
images (10 credits) and multi-slide carousels/decks/documents (15 credits per
slide) across 100+ formats, generated natively in 150+ languages. Brand kits keep
every output in the client's colors, fonts, logo, and tone.

This is the core skill: setup, the generate loop, credits, and refinement.
Task-specific skills build on it — see "Companion skills" at the bottom.

## Setup (once)

1. `npm install -g @canvora/cli` (Node 18+, zero dependencies; **v1.4+** for
   `--logo`, `--cta`, `--no-text`, `--freeform`, `--landing-page`)
2. Get an API key: canvora.ai → Integrations → API Keys (all plans, incl. Free)
3. `export CANVORA_API_KEY=vd_...`

Verify: `canvora credits --json` returns the account balance.

## Before you generate: the four things that decide the output

Generation costs credits and is not instant — a single visual usually lands in
under a minute or two, and multi-slide work scales from there (see "Long runs").
Get these right on the first call; there is no cheap retry.
Ask the user ONLY for what you cannot infer from the conversation — never
interrogate. In order of impact:

1. **Source** — do they have content, a link, a file, or just a topic? (picks
   `--input` / `--url` / `--file-url` / `--idea`)
2. **Where it goes** — the platform or artifact decides the format, not the
   other way round ("LinkedIn carousel", "a PDF one-pager", "Meta ads").
3. **Whose brand** — if a client or company is named, look up the kit
   (`canvora brands --json`) and pass `--brand`. Skipping this is the single
   biggest quality drop.
4. **Any look they already have in mind** — one line is enough ("black and
   white, big type"). If they say nothing, do not invent art direction.

Defaults that are safe when the user gives nothing: 5 slides, `--style modern`,
2K, language auto-detected from their input.

## Creating visuals

Always pass `--json`: results print to stdout as JSON, progress goes to stderr.

```bash
# From a short concept (Canvora plans it: detects language, develops the items)
canvora generate --idea "5 tips for remote work" \
  --format linkedin_carousel_portrait --slides linkedin_carousel_portrait=5 --wait --json

# From YOUR full content (used as the source material; needs 50+ chars)
canvora generate --input "$FULL_POST_TEXT" --format instagram_post --wait --json

# From a URL (blog post, landing page - content is extracted automatically)
canvora generate --url https://example.com/post \
  --format instagram_post,quote_card --wait --json

# From a PDF or DOCX (the URL must be PUBLICLY fetchable - no localhost/private links)
canvora generate --file-url https://example.com/report.pdf \
  --format presentation_slide --slides presentation_slide=8 --wait --json
```

The final JSON contains `generation.outputs[]`, each with a stable CDN
`fileUrl` you can post, embed, or download.

## Choosing the input mode

- `--idea`: a concept, not content ("5 tips for X"). Canvora runs a planning
  pass: detects the language, invents the substance, maps items to slides.
- `--input`: the user already wrote the content (50+ chars). It is used as
  source material; wording is respected, not reinvented.
- `--url` / `--file-url`: content is extracted from the page/PDF/DOCX first.
- Rule of thumb: if the user hands you finished text, use `--input`; if they
  hand you a topic, use `--idea`; if they hand you a link or file, pass it
  directly instead of copy-pasting its text.

## Choosing formats

The live catalog is the source of truth - do not guess format IDs:

```bash
canvora formats --json
```

Each entry has `id`, `dimensions`, `category` (social, marketing, infographic,
presentation, document, advertising, web, email, landing_page), `is_carousel`,
and a `description`. Match the user's intent against category + description.
Carousel-flagged formats take `--slides`.

Two ID traps: landing-page formats are camelCase with a hyphen
(`landingPage-Hero`, not `landing_page_hero`), and the multi-page PDF format is
called `document_page` — nobody guesses that one (see the `pdf-document` skill).

Combos worth knowing (these span formats, so the catalog can't tell you):
- Announcing something: `announcement_card` + `instagram_post` + `instagram_story`
- Promoting an article: `blog_header` + `og_image` + a carousel from the same URL
- Ad campaign: `ad_square` + `ad_landscape` + `ad_portrait` (covers all placements)
- A claim + its proof: a carousel plus `stat_card` or `testimonial_card` from the same source

Batching: one generation can carry several formats
(`--format instagram_post,linkedin_post,quote_card`) - all outputs come from
the same source with a consistent look, and cost is simply the sum
(10/visual, 15/slide). Prefer one batched call over several separate ones.
One instance per format per call: for 3 different Instagram posts, run 3
calls with 3 different ideas (not `instagram_post,instagram_post`).

## Slide counts (carousel formats only)

`--slides <format>=<n>` (1-10, default 5). If the idea or content promises N
items ("5 tips", "6 formas", "7 steps"), set `--slides` to N so each item
gets its own slide - or N+1 if you also want a cover. If you omit it, Canvora
fits the items into 5 slides (combining or stretching as needed).
`x_multi_image` caps at 4.

## Brand kits

`canvora brands --json` lists the account's brand kits. Pass one with
`--brand <uuid>` so outputs use that client's colors, fonts, and logo. If the
user names a client or brand, ALWAYS look up and pass their kit - it is the
difference between on-brand output and generic output.

Add `--logo` to actually place the brand logo on the visual. `--brand` alone
applies the colors, fonts and voice but **does not** stamp the logo.

On a single-image format `--logo` applies to that image. On a **carousel or
deck it applies to the first and last slide only** - the cover and the closing
slide carry the mark, the middle stays clean. That is deliberate. If the user
wants the logo on a middle slide, add it afterwards with an edit.

## Styles, art direction, and language

`--style` sets the aesthetic: `modern` (default), `minimal`, `bold`,
`elegant`, `playful`, `corporate`, `creative`, `dark`. Pick from the user's tone:

- corporate, professional, B2B → `corporate` or `minimal`
- friendly, consumer, lifestyle → `playful` or `creative`
- premium, luxury → `elegant` or `dark`
- loud, promotional → `bold`

**Omitting `--style` does not mean "let Canvora choose" — it pins `modern`.**
So make a deliberate pick whenever the user's tone gives you one.

**How much to art-direct.** Let Canvora own the design *execution* — layout,
composition, per-slide imagery, color harmony. Do not write slide-by-slide
visual instructions. But when the user states an aesthetic ("black and white,
grey background, large type", "hand-drawn", "dark and premium"), pass it
through in one line: it is honoured and it measurably improves the result.
Dropping the user's stated look is a worse failure than over-specifying.

Language is detected from your input automatically - a Spanish idea yields a
Spanish carousel, natively generated (not translated). To force a specific
language (e.g. an English brief for a Turkish audience), pass
`--language tr` or `--language Turkish`.

## The v1.4 levers

| Flag | Use it when |
|---|---|
| `--logo` | the visual should carry the brand mark (needs `--brand`; first + last slide on carousels) |
| `--cta` | a carousel/deck should end on a call-to-action slide (it **consumes one of your slides** - ask for 6 with `--cta` and slide 6 is the CTA, not extra) |
| `--no-text` | they want pure imagery: backgrounds, hero art, textures |
| `--freeform` | they want the format's shape only, with no format-specific art direction |
| `--landing-page` | with `--url`: read a page's sections and produce a matching visual kit (Starter+) |
| `--exact` | the text must appear verbatim (quotes, taglines, legal lines) |

## Recipes for common asks

```bash
# "Promote this blog post" - full promo set from one URL
canvora generate --url $POST_URL \
  --format blog_header,instagram_carousel,linkedin_post --slides instagram_carousel=6 \
  --brand $BRAND --logo --wait --json

# "Weekly content in English and Spanish" - run twice, native each time
canvora generate --idea "3 mistakes first-time founders make" --format instagram_carousel --slides instagram_carousel=4 --wait --json
canvora generate --idea "3 errores de los fundadores primerizos" --format instagram_carousel --slides instagram_carousel=4 --wait --json

# "Turn this report into a deck"
canvora generate --file-url $PDF_URL --format presentation_slide --slides presentation_slide=8 --wait --json

# "Make an ad set for this product page"
canvora generate --url $PRODUCT_URL --format ad_square,ad_landscape,ad_portrait --brand $BRAND --cta --wait --json
```

## Budgeting and errors

- Check before large jobs: `canvora credits --json` (10 credits per visual,
  15 per slide; a 5-slide carousel = 75 credits).
- Exit code 0 = success, 1 = failure (message on stderr), 2 = usage error.
- Failed generations refund automatically; safe to retry on exit 1 unless the
  error says the request was declined by content safety checks (those are
  terminal - do not retry).
- A `partial` status means some visuals were blocked or failed; the credits for
  those are refunded automatically. Report what came back and why, don't silently
  hand over a short carousel.
- Rate limit: 20 generation requests/minute. For big batches, run
  sequentially rather than firing them all at once.
- Free-plan outputs carry a watermark; paid plans export clean. If the user
  asks why there is a watermark, that is the reason.
- Everything you create also lands in the user's Canvora dashboard for review
  and editing - tell the user where to find it.

## Long runs: your own command timeout is the real limit

`--wait` polls until done, up to 600s (`--timeout` to change). But the binding
constraint is usually **your harness's shell timeout, not Canvora's** - many
agent runtimes kill a shell command at 120s by default. A single visual lands in
under a minute or two; multi-slide work takes proportionally longer.

- **1-2 outputs:** `--wait` is fine if you can raise your shell timeout to 300s.
- **3+ outputs:** do NOT use `--wait`. Fire the generation, keep the returned
  `generation.id`, and poll `canvora status <id> --json` in separate short
  commands until `status` is `completed`, `partial`, or `failed`.
- A killed shell does NOT cancel anything - the generation carries on
  server-side. `canvora status <id>` always retrieves it.
- **NEVER re-run `generate` after a timeout.** That starts a second, separate
  generation. Poll `status` instead. This is the single most expensive mistake
  an agent can make here.

```bash
# 3+ outputs: start it, then poll. Without --json the first stdout line is the
# bare generation id, so this needs no jq (progress notes go to stderr).
ID=$(canvora generate --idea "..." --format pitch_deck --slides pitch_deck=10 | head -1)
canvora status "$ID" --json  # repeat every ~30s until completed
```

Use `| head -1` rather than parsing `--json` for the id: it works identically
for `generate`, `localize` and `variations`, whereas the JSON shape differs
between them (`generate` nests it at `.generation.id`, the other two return
`.generationId`). Poll with `--json` as usual once you have the id.

## Delivering carousels: slide order matters

Each output in `generation.outputs[]` has a `sortOrder` field. When posting
or downloading carousel/deck slides, ALWAYS sort by `sortOrder` first -
outputs can complete out of order, and a scrambled carousel ruins the story.

## Refining existing visuals (NEVER regenerate from scratch)

When the user wants to change something about a visual you already made,
regenerating loses the design and costs full credits. Use these instead.
The rates differ per operation - do not assume one number:

| Operation | Credits |
|---|---|
| `edit` one visual | **3** |
| `localize` per visual, per language | 10 |
| `variations` of a single-image format | 10 per new image |
| `variations` of a carousel/deck | **15 per slide** |

Editing is deliberately the cheap path - reach for it first. `localize` and
`variations` need the Visual Editor feature (Starter plan or an active
Campaign Pack); a 403 there means the plan lacks it, not an auth problem.

```bash
# Same design, different language - the layout survives, only text changes
canvora localize <generationId> --language es --wait --json

# Fresh takes on the same generation. NOTE: --count is PER OUTPUT -
# count 2 on a 5-slide carousel = 10 new images at 15 each = 150 credits.
canvora variations <generationId> --count 2 --wait --json

# Natural-language edit of ONE output (3 credits). Without --yes it prints
# Canvora's interpretation of your instruction for confirmation.
canvora edit <outputId> --prompt "make the headline bigger" --yes --json
```

If `edit` replies "needs clarification", re-run with a more specific prompt.

Exact wording: when the user's text must appear verbatim (quotes, taglines,
slogans), generate with `--input "the exact text" --exact` - this disables
rewording.

## What needs the MCP server instead of the CLI

The remote MCP server (`https://api.canvora.ai/mcp`) exposes capabilities the
CLI does not. If the user is on an MCP-capable client, use these tools:

- `export_visuals` — PDF / PPTX / ZIP export of a generation
- `upload_photo` + `confirm_generation(embedding_photos)` — put the user's own
  product or team photos INTO the design (see the `product-photo-visuals` skill)
- `get_edit_history` / `revert_edit` — version history, free revert
- `convert_image` — JPG/WebP/PNG conversion
- `chat` / `confirm_generation` — the conversational planning flow

CLI-only users: point them at their Canvora dashboard for export.

## Other commands

```bash
canvora status <generationId> --json      # progress + output URLs
canvora download <generationId> --dir ./  # save files locally
```

## Companion skills

Load the one that matches the job — each assumes this skill for setup:

| Skill | For |
|---|---|
| `instagram-carousel` | Instagram carousels / swipe posts |
| `linkedin-carousel` | LinkedIn document carousels |
| `pitch-deck` | presentations, pitch/sales/training decks, doc → deck |
| `pdf-document` | multi-page PDFs: brochures, reports, one-pagers, menus |
| `landing-page-visuals` | a whole landing page's visual kit from its URL |
| `ad-campaign` | paid social + display ad sets |
| `blog-promo-kit` | blog header, OG image, and promo set from one post |
| `data-infographic` | process flows, comparisons, timelines, stat cards |
| `multilingual-campaign` | one campaign, many languages |
| `product-photo-visuals` | designs built around the user's own photos (MCP) |
| `visual-refresh` | fixing, varying, and versioning what already exists |
