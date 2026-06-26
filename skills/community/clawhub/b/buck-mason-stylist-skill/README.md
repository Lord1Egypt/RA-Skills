# Buck Mason Stylist Skill

A personal-shopping skill for [Buck Mason](https://www.buckmason.com), built for Claude Code, Codex, ChatGPT custom GPTs, and any agent that loads `SKILL.md`–style skills. Talks to the pima.io MCP at `pima.io/mcp/buckmason/*`.

## What it does

- **Stock check** — "do they have the [item] in my size, online and at the Abbot Kinney store?" — returns bucketed live counts (`In stock` / `Low stock (N left)` / `Out of stock`) per location.
- **Wardrobe gap analysis** — "what am I missing for a Sonoma wedding in May?" — diffs your owned items against a season + climate + dress-code-aware capsule recommendation, with a one-sentence "why" per pick.
- **AI try-on lookbooks** — by default, "lookbook" means gpt-image-2 virtual try-on images of you wearing the recommended outfits, assembled into a hosted HTML/HTML-cart lookbook with partner voting enabled.
- **One-shot MPP checkout** — `POST /mcp/buckmason/checkout` speaks the [Merchant Payments Protocol](https://mpp.dev): HTTP 402 + Stripe Shared Payment Token via [`stripe/link-cli`](https://github.com/stripe/link-cli), push-approved by the customer in the Link app. See `references/mpp.md`.

## Required setup

### `OPENAI_API_KEY` (for the default AI try-on lookbook workflow)

```bash
export OPENAI_API_KEY=sk-...
```

The skill posts to `https://api.openai.com/v1/images/edits` with `model: "gpt-image-2"` to generate virtual try-on images. **The OpenAI organization tied to the key must be verified for `gpt-image-2`** (see <https://help.openai.com/en/articles/10910291>). Get a key at <https://platform.openai.com/api-keys>.

The other workflows — stock check, recommend, checkout, order tracking — do **not** require an OpenAI key. They only call the pima.io MCP. If a lookbook request is missing the key or usable reference photos, the skill should say what is missing and offer the Editorial tier instead of silently downgrading.

### Voting on deployed lookbooks

Cloudflare Pages deploys include the voting mechanism by default. Create one KV namespace per Cloudflare account, then save the id in `profile.md` as `lookbook_votes_kv_id:` or export it as `LOOKBOOK_VOTES_KV_ID`.

```bash
CLOUDFLARE_ACCOUNT_ID=<account-id> wrangler kv namespace create LOOKBOOK_VOTES
```

### Profile

One profile file in your agent's workspace (copy from `templates/profile.example.md`):

```bash
cp templates/profile.example.md ~/agent-workspace/profile.md
$EDITOR ~/agent-workspace/profile.md   # fill in sizes, home zip, build, face, reference photos
```

That's it. No Buck Mason credentials. No Pima account.

Optional but useful:
- `wardrobe.md` — owned items (enables gap analysis)
- `events.md` — upcoming travel/events (enables event-aware suggestions)
- `magick`, `python-pptx`, `Pillow` — only needed for the PPT/HTML lookbook output (see `references/output-formats.md`)
- [`stripe/link-cli`](https://github.com/stripe/link-cli) — required for the MPP fully-agent-driven checkout path

For MPP checkout, `profile.md` can remember payment preferences by purpose using card last4s, for example `preferred_link_payment_methods: { clothing: "1234", business: "9876" }`. The agent still resolves the live Link payment-method id with `link-cli payment-methods list` immediately before checkout and passes it to `link-cli spend-request create --payment-method-id`; never store Link internal ids, SPTs, card numbers, or CVVs.

## Codex support

- `AGENTS.md` is the Codex-facing repo guide for editing this skill.
- `SKILL.md` is the runtime skill entry point used by Claude, Codex, ChatGPT, and other agents.
- `agents/openai.yaml` provides OpenAI/Codex skill-list metadata and the default `$buck-mason-stylist` invocation prompt.
- `CLAUDE.md` remains in place for Claude Code-specific maintenance notes.

## Quick start

```text
You:  Stock check on the Daily Shirt in olive, in my size near 90291.
Skill: Online: 1,844 (in stock). Abbot Kinney: 36, Century City: 31. Pickup today.
       https://www.buckmason.com/products/olive-daily-shirt
```

```text
You:  Build me a 3-look capsule for a Sonoma wedding in May, smart-casual.
Skill: [pulls /mcp/buckmason/recommend, filters via style-reasoning matrix,
        diffs against your wardrobe, generates 3 gpt-image-2 virtual try-on
        images, outputs a hosted voting-enabled HTML lookbook or HTML-cart
        handoff, then runs a fully-agent-driven MPP checkout if you've opted in]
```

See `examples/stock-check.md` and `examples/lookbook.md` for full walkthroughs.

## Files

| File | Purpose |
|---|---|
| `AGENTS.md` | Codex-facing repo guidance for editing and validating the skill |
| `SKILL.md` | Main skill entry point — workflows, data sources, output style |
| `agents/openai.yaml` | OpenAI/Codex skill UI metadata and default invocation prompt |
| `references/mcp-api.md` | Pima MCP endpoint contract |
| `docs/advanced/pima-api.md` | Advanced — legacy `/api/*` reference (login, account, checkout); not needed for v0.1.0 stylist flows |
| `references/image-generation.md` | OpenAI image-gen prompt cookbook + gpt-image-2 hint inventory |
| `references/seasons.md` | Season + region + heat-type mapping |
| `references/style-reasoning.md` | Climate matrix, formality scale, classic-vs-trend filter |
| `references/output-formats.md` | Lookbook output: `images` / `ppt` / `html` / `html-cart` builders + quickest-host options |
| `references/brand-style.md` | Buck Mason visual style guide (fonts, colors, button shape, image ratios) extracted from buckmason.com — used by every rendered lookbook builder |
| `references/hosting-options.md` | Capability-aware menu of hosts for the HTML lookbook — probe script + ranked transports (Cloudflare Pages → Netlify → Vercel → Surge → Gist → S3 → 0x0.st) |
| `references/voting.md` | Cloudflare Pages voting capability — per-look and per-item thumbs + comments, backed by KV |
| `references/mpp.md` | Merchant Payments Protocol checkout (mpp.dev + stripe/link-cli) — fully agent-driven transactions via HTTP 402 + Stripe Shared Payment Token |
| `references/acceptance-checklist.md` | Lookbook validation gates (local + deployed) — implemented by `scripts/validate-lookbook.py` |
| `references/headless-mode.md` | Cron / scheduled / voice run rules: no questions, defaults, fallback tier, deploy-if-pre-authorized, silent-unless-blocker |
| `references/event-suitability.md` | Calendar-driven scoring rubric — score events 0–10; ≥6 triggers a lookbook (hard veto for medical/therapy) |
| `references/run-layout.md` | Per-lookbook directory isolation + `.lookbook_id` marker convention (hard rule against cross-lookbook image reuse) |
| `templates/*.example.md` | Copy these into your workspace |
| `templates/profile.schema.json` | JSON Schema for the customer profile — machine-validate enums + required fields |
| `examples/*.md` | End-to-end walkthroughs |
| `scripts/build-html-lookbook.py` | Deterministic builder (config + picks → deploy directory) |
| `scripts/deploy-lookbook.sh` | Cloudflare Pages deploy wrapper with probe + validate gates |
| `scripts/validate-lookbook.py` | Runs `references/acceptance-checklist.md` against a local dir and/or deployed URL |
| `scripts/score-calendar-event.py` | Implements `references/event-suitability.md` for calendar-driven invocations |
| `scripts/discover-weekly-candidates.py` | Surfaces recently-live + previously-unproposed products for the weekly newsletter — dedupes against the long-term wishlist |
| `scripts/run-headless-lookbook.py` | Canonical end-to-end orchestrator (score → discover → curate → build → deploy → validate → summary) |
| `scripts/verify-face.py` | Face-verification gate for Premium-tier outputs — GPT-4o-vision rubric against the customer's reference photos |
| `scripts/inject-voting-ui.py` | Post-build injector for the default Cloudflare Pages voting widget |
| `templates/voting/*` | Cloudflare Pages Functions and `wrangler.toml` template for lookbook voting |
| `PUBLISHING.md` | ClawHub distribution path |
| `SECURITY.md` | Threat model, data flows, opt-in capability matrix, vulnerability reporting |

## Install via ClawHub

Listing: <https://clawhub.ai/nickmerwin/buck-mason-stylist-skill>

```bash
clawhub install nickmerwin/buck-mason-stylist-skill

# Some ClawHub install paths strip the executable bit on unpack — restore it
# once after installing so the bundled scripts can run directly. (The skill's
# own command examples all use explicit `bash` / `python3` prefixes that
# work regardless, so this step is optional but tidier.)
chmod +x ~/.clawhub/skills/buck-mason-stylist-skill/scripts/*
```

## License

MIT. See `LICENSE`.

## Contributing

This skill is Buck Mason / Pima.io–specific by design. The MCP endpoints, brand voice, store footprint, and product taxonomy are all Buck Mason. Forks for other brands are welcome — replace the `/mcp/buckmason/...` paths with your own tenant slug, swap the references, and you're most of the way there.

Source + issues: <https://github.com/pima-io/buck-mason-stylist-skill>
Listing: <https://clawhub.ai/nickmerwin/buck-mason-stylist-skill>
