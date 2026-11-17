---
name: landing-page-visuals
version: 1.0.0
description: Generate a complete visual kit for a landing page from its URL — hero, features, process, stats, testimonials, comparison, timeline and CTA imagery, matched to the page's own sections. Use when the user wants landing page images, website section visuals, hero images, or asks to "make visuals for my site".
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"🧩","requires":{"bins":["canvora"],"env":["CANVORA_API_KEY"]}}}
---

# Landing page visual kits

Canvora has a section-aware mode that nothing else in the toolchain does: give
it a URL and it reads the page's actual sections, decides which ones deserve a
visual, and renders a matching kit. One command, a whole page's imagery, in the
page's own language.

Requires the **Starter plan or higher** — a 403 here means the plan, not auth.
Setup and credits: see the `canvora` skill.

## The one command

```bash
ID=$(canvora generate --url https://example.com --landing-page \
  --brand $BRAND --logo | head -1)
canvora status "$ID" --json    # repeat every ~30s until completed
```

`--format` is not required in this mode: the kit is derived from the page.
`--landing-page` requires `--url` (it has nothing to read otherwise).

A kit is up to 10 visuals, so fire-and-poll rather than `--wait` — most
harnesses kill a shell command at 120s while the kit carries on rendering
server-side. Never re-run `generate` after a timeout; poll `status`
(detail in the `canvora` skill's "Long runs" section). Say the cost in the same
message as the run: 10 credits per visual, so a full kit is up to 100. Announce
it, don't ask permission — but if the page could yield the full 10 and they
only wanted a hero, settle that first.

## What it produces, and what it deliberately skips

The pipeline maps sections onto these formats:

| Format | Section |
|---|---|
| `landingPage-Hero` | 21:9 hero banner |
| `landingPage-Feature` | feature blocks |
| `landingPage-Process` | how-it-works |
| `landingPage-Showcase` | product showcase |
| `landingPage-Stats` | metrics / proof |
| `landingPage-Testimonial` | quotes |
| `landingPage-Comparison` | vs / before-after |
| `landingPage-Timeline` | roadmap / history |
| `landingPage-CTA` | closing call to action |
| `landingPage-UseCase` | **never auto-emitted** — name it explicitly to get it |

Caps and guarantees, so you can set expectations before spending credits:

- at most **10 sections** and **10 visuals** per run; at most **5 per section**
- **hero and CTA are never trimmed** — everything else competes for slots
- FAQ, team, contact, footer and logo walls are intentionally skipped: they are
  not visual sections. If the user wants one anyway, generate it as a normal
  format in a separate call.

Note the IDs are camelCase with a hyphen — `landingPage-Hero`, not
`landing_page_hero`. Guessing the snake_case version fails.

## Intake

Usually just: **the URL** and **the brand kit**. Then two judgement calls:

1. **Is the page live and public?** The page has to be publicly fetchable —
   staging behind auth, localhost, and password walls won't work. Ask for the
   public URL.
2. **Whole page or one section?** If they only want a hero, don't use this mode
   — run `--format landingPage-Hero` with `--url` normally and spend 10 credits
   instead of a kit's worth.

Language is taken from the site itself, so a Spanish page yields Spanish
visuals without you passing anything.

## Selective runs (when the kit is overkill)

```bash
# Just the hero
canvora generate --url $URL --format landingPage-Hero --brand $BRAND --wait --json

# Hero + CTA + the use-case visual the kit never emits on its own (3 outputs — poll)
ID=$(canvora generate --url $URL \
  --format landingPage-Hero,landingPage-CTA,landingPage-UseCase \
  --brand $BRAND | head -1)
canvora status "$ID" --json

# Pure imagery with no typography baked in (devs adding their own copy in HTML)
canvora generate --url $URL --format landingPage-Hero --no-text --wait --json
```

`--no-text` is the flag web teams want and never find: it produces the artwork
without text, so the copy stays in the DOM where it belongs.

## After generation

- Hand back **URL per section**, not a flat list — the user has to place these.
  Sort by `sortOrder` and label each with its format ID.
- A section that looks wrong is an `edit` (3 credits), not a re-run of the kit.
- Rebranding later? `canvora variations <id>` or re-run with a different
  `--brand`; the page reading is the expensive part, not the rendering.

## Quality checklist

- [ ] Public, live URL confirmed
- [ ] `--landing-page` used only for a whole kit; single sections run as normal formats
- [ ] Brand kit applied
- [ ] `--no-text` offered when the visuals go into a real HTML page
- [ ] Outputs labelled by section, not dumped as a list
- [ ] Plan gate explained if a 403 comes back
