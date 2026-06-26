<div align="center">

# 🛍️ skill-autoecom

**Daily AI-driven product carousel pipeline for ecommerce — runs inside agent harnesses.**

*Identifies your brand. Picks the next bestseller. Generates stylized slides with nano-banana. Publishes to Instagram + TikTok.*

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Gemini 2.5 Flash Image](https://img.shields.io/badge/model-nano--banana-orange.svg)](https://ai.google.dev/)
[![Upload-Post](https://img.shields.io/badge/publishing-Upload--Post-purple.svg)](https://upload-post.com/)

[Quick install](#-one-shot-install-paste-into-any-agent) · [How it works](#-how-it-works) · [How it learns](#-how-it-learns) · [Manual setup](#-manual-setup) · [Compatibility](#-compatibility)

</div>

---

## 🤖 Built for agent harnesses

This is **not** a one-shot script. It's a **Skill** — a structured workflow with explicit human-in-the-loop checkpoints, designed to be driven by a multimodal agent that can see, decide, and write.

Officially supported harnesses:

| Harness | Status | Notes |
|---|---|---|
| **[Hermes Agent](https://hermesagent.com)** | ✅ Primary target | Daily-routine orchestrator. Bridges Telegram / WhatsApp so you approve carousels from your phone. |
| **[OpenClaw](https://openclaw.com)** | ✅ Primary target | Self-hosted agent harness. Same daily-routine orchestration as Hermes. |
| **Claude Code** | ✅ Works | Run `/autoecom` directly in the terminal. Prompts appear in CLI instead of phone. |
| **Codex / any agent w/ shell + WebFetch** | ⚠️ Should work | Untested but the SKILL.md is harness-agnostic. |

The **agent** does the creative + visual work (identifying the logo, choosing colors, inferring brand voice, planning slides, writing copy). The **Python script** (`autoecom.py`) is glue — it does the mechanical parts the agent can't (calling APIs, compositing pixels, persisting state).

---

## ⚡ One-shot install (paste into any agent)

Open Claude Code, Codex, Hermes, OpenClaw, or any agent with shell access and paste:

```
Set up https://github.com/mutonby/skill-autoecom for me. Read README.md and SKILL.md, clone the repo into ~/Documents/skill-autoecom, create the venv, install requirements.txt, copy .env.example to .env, and ask me for the values of STORE_URL, GEMINI_API_KEY, UPLOAD_POST_API_KEY, and UPLOAD_POST_PROFILE one by one. After .env is filled, run a health check against the Upload-Post API and tell me whether Instagram and TikTok are connected. Then PROGRAM TWO RECURRING ROUTINES IN MY AGENT HARNESS: (1) `/autoecom` daily at 09:00 local time — generate the carousel and send it to my configured messenger (Telegram / WhatsApp / whatever) for approval; (2) `/autoecom-learn` weekly on Monday at 09:00 — run `python autoecom.py learn` and post a digest of what was learned to the same messenger. Ask me which messenger I want before scheduling. Do not echo any API key back to me after I paste it.
```

The agent will handle the entire bootstrap **including the two cron jobs**. Without those routines, the daily round-robin stalls and the priors never refresh — see [How it learns](#-how-it-learns). Total time: ~2 minutes + however long it takes you to paste 4 keys.

> [!IMPORTANT]
> **This skill is designed to run on a schedule, not on demand.** Two routines are mandatory:
> - **Daily 09:00** — generate today's carousel and ask for approval via your messenger.
> - **Weekly Monday 09:00** — refresh `HOT_HOOKS.md` + `HOT_IMAGERY.md` from real engagement data, and post a chat summary of what changed.
>
> Hermes and openclaw handle this natively (they have built-in schedulers + messenger bridges). For plain Claude Code, fall back to system `crontab`. The agent will offer to set both up on first invocation.

---

## 🧭 How it works

```
                          ┌─────────────────────────────────────┐
                          │  HARNESS  (Hermes / OpenClaw / CC)  │
                          │  schedules /autoecom daily          │
                          └─────────────┬───────────────────────┘
                                        │
                ┌───────────────────────▼───────────────────────┐
                │              AGENT (Claude / Opus)             │
                │  reads SKILL.md and orchestrates the workflow  │
                └───────────────────────┬───────────────────────┘
                                        │
   ┌────────────────────────────────────┼────────────────────────────────────┐
   │                                    │                                    │
   ▼                                    ▼                                    ▼
┌──────────────┐                  ┌──────────────┐                    ┌──────────────┐
│  Step 1-2    │                  │  Step 3-5    │                    │  Step 6-9    │
│ BRAND KIT    │                  │  PLAN +      │                    │  REVIEW +    │
│ + PRODUCT    │                  │  GENERATE    │                    │  PUBLISH     │
└──────┬───────┘                  └──────┬───────┘                    └──────┬───────┘
       │                                 │                                   │
       │  WebFetch homepage              │  Agent writes plan.json           │  Agent QAs
       │  Multimodal vision              │  (3-8 slides, copy, layout)       │  every slide
       │  → identifies logo,             │                                   │
       │    colors, font, voice          │  python autoecom.py generate ─┐   │  User approves
       │                                 │     ↓                         │   │     ↓
       │  python autoecom.py             │  ┌────────────────┐           │   │  python autoecom.py
       │   ├ download (logo)             │  │  nano-banana   │           │   │   publish
       │   ├ palette  (hex colors)       │  │  (Gemini 2.5   │           │   │     ↓
       │   └ product  (JSON-LD parse)    │  │  Flash Image)  │           │   │  ┌──────────┐
       │                                 │  └────────────────┘           │   │  │Upload-Post│
       │  → state/brand_kit.json         │                               │   │  └─────┬────┘
       │  → round-robin pick             │  python autoecom.py compose ──┘   │        │
       │    (state/processed.json)       │     ↓                             │        ▼
       │                                 │  ┌────────────────┐               │   ┌──────────┐
       │                                 │  │     Pillow     │               │   │ Instagram│
       │                                 │  │  text overlay  │               │   │  TikTok  │
       │                                 │  │  logo + grad.  │               │   └──────────┘
       │                                 │  └────────────────┘               │
       │                                 │     ↓                             │
       │                                 │  output/<sku>/slide_*.jpg         │
       └─────────────────────────────────┴───────────────────────────────────┘
```

**Daily flow** (≈ 5 min agent time, plus your approval taps):

1. **Preflight** — agent verifies venv + `.env` + Upload-Post platform health.
2. **Brand kit** — agent fetches the homepage, extracts logo / palette / font / voice. Cached for 7 days.
3. **Pick product** — agent reads the bestseller list, picks the next unprocessed item (round-robin).
4. **Plan** — agent writes a 3–8 slide structure: hook / benefit / proof / CTA, with on-image copy.
5. **Generate** — `nano-banana` re-imagines the product photo per slide (stylized, on-brand).
6. **Compose** — Pillow lays text + logo + gradient onto each slide.
7. **Visual QA** — agent looks at every slide and flags drift before showing the user.
8. **Approval** — user approves the carousel from Telegram / WhatsApp / CLI.
9. **Publish** — multipart POST to Upload-Post → IG carousel + TikTok draft.
10. **Mark processed** — round-robin state advances; tomorrow picks the next product.

---

## 🧠 How it learns

The skill **gets smarter every week**. Two evidence-backed priors are maintained from real engagement and re-injected into future runs:

```
                 ┌───────────────────────────────────────────┐
                 │           DAILY PIPELINE                  │
                 │                                           │
                 │   plan.json ──► log-candidate ──► raw     │
                 │       │                                   │
                 │       │ (agent reads HOT_HOOKS.md         │
                 │       │  for slide-1 copy)                │
                 │       ▼                                   │
                 │   generate ──► nano-banana                │
                 │       ▲                                   │
                 │       │ (script auto-prepends             │
                 │       │  HOT_IMAGERY.md)                  │
                 │                                           │
                 │   publish ──► post-history.jsonl ◄──┐     │
                 └─────────────────────────────────────┼─────┘
                                                       │
                              ┌────────────────────────┘
                              │
                              ▼
                      ┌───────────────┐         Upload-Post
                      │  learn (weekly)│ ◄──── post-analytics
                      └───────┬───────┘
                              │ z-score winners vs losers
                              ▼
                      ┌───────────────┐    ┌───────────────┐
                      │ HOT_HOOKS.md  │    │HOT_IMAGERY.md │
                      │ (slide-1 copy)│    │(image prompts)│
                      └───────────────┘    └───────────────┘
                              ▲                    ▲
                              │                    │
                              └────────┬───────────┘
                                       │
                              tomorrow's carousel
                              reflects what worked
```

| Subcommand | Cadence | What it does |
|---|---|---|
| `log-candidate <plan.json>` | once per planning session | Records the agent's INITIAL proposal to `learnings/candidate-history.jsonl`. |
| `publish` (auto) | every approved carousel | Appends the FINAL plan + `request_id` to `learnings/post-history.jsonl`. |
| `learn` | weekly (Monday 09:00 cron) | Pulls Upload-Post metrics, finds winners/losers (z-score on views + engagement), asks Gemini to refresh BOTH `HOT_HOOKS.md` AND `HOT_IMAGERY.md`. **Agent posts a digest of what changed to your messenger** (Telegram / WhatsApp / whatever the harness is bridging) so you don't have to read audit files. |
| `reflect` | on demand | Compares candidates vs published in a window. Emits qualitative observations on hooks AND imagery. NOT auto-promoted. |

### What's better than a single-prior system

Most "learning loops" mix copy and visual signals into one prior. Bad idea — they're independent variables, and a winner's hook could be carrying its mediocre imagery (or vice versa). This skill keeps them separate:

- **`HOT_HOOKS.md`** is creative input — the **agent reads it** before writing slide-1 `text_overlay`. Bullets like *"hooks <8 words convert 3× better, seen in 4/5 winners, 0/5 losers"* directly inform the planner.
- **`HOT_IMAGERY.md`** is mechanical injection — the **script auto-prepends it** as a prefix to every nano-banana prompt during `generate`. The agent doesn't have to remember; it just happens.

### Composite scoring

`learn` ranks carousels by:

```
composite = 0.6 · z(total_views) + 0.4 · z(engagement_rate)
```

Top 20% = winners, bottom 20% = losers. Defaults tunable via `--top-pct`, `--bottom-pct`, `--weight-views`, `--weight-engagement`.

`learn --soak-days 7` (default): carousels younger than 7 days are excluded — engagement metrics need time to mature, daily learning would chase noise. Older than 90 days = stale and ignored too.

If fewer than ~5 winners + 5 losers are eligible, `learn` skips the synthesis and writes a "not enough data" note to `learnings/runs/learn-YYYY-MM-DD.md`. Just keep publishing.

### Audit trail

Every `learn` run writes a full audit to `learnings/runs/learn-YYYY-MM-DD.md`: which carousels were called winners, with their composite scores, the previous priors, and the new priors side-by-side. Old priors are backed up as `HOT_HOOKS.YYYYMMDD-HHMMSS.md.bak` and `HOT_IMAGERY.YYYYMMDD-HHMMSS.md.bak`. You can roll back if Gemini synthesizes garbage.

### Reflect: edit-as-rejection signal

`reflect` exploits a smarter signal than autoshorts'. It uses `candidate_id` (sha1 of the plan content) to detect three distinct outcomes:

- **Approved-unchanged**: agent's initial plan was published verbatim → strong positive signal.
- **Edited-then-published**: initial plan logged, but post-history has a different `candidate_id` for the same product → user revised it before publishing (mild negative on the original).
- **Never-published**: candidate logged, no matching post → full rejection.

Output goes to `learnings/runs/reflect-...md` and is **not** auto-promoted to the HOT files — reflect could lock in your past biases rather than what actually performs. Read, curate manually.

### Don'ts

- Don't edit `HOT_HOOKS.md` / `HOT_IMAGERY.md` by hand AND keep running `learn` — `learn` will overwrite. Manual rules go in `learnings/insights/`.
- Don't delete `post-history.jsonl`, `candidate-history.jsonl`, or `metrics.jsonl` — they're append-only memory.
- Don't run `learn` more than once a week — Gemini will just churn the same patterns.
- Don't call `log-candidate` multiple times per planning session — only the FIRST plan, before user edits.

---

## 🧩 Architecture: agent-driven, script-as-glue

The Python script (`autoecom.py`) deliberately does **not** scrape the brand kit, plan slides, or write copy. Those tasks are creative + visual — the agent does them with `WebFetch`, `Read` (multimodal), and `Write`. The script only handles mechanical work the agent can't do directly:

| Subcommand | Purpose |
|---|---|
| `download <url> <out>` | Fetch a URL to a local file (logo, product image). |
| `palette <image> [--n 5]` | Extract dominant hex colors from an image. |
| `product <url>` | Parse a product page's JSON-LD into a JSON dict. |
| `generate <plan.json>` | Call nano-banana per slide (auto-prepends `HOT_IMAGERY.md` prior). |
| `compose <plan.json>` | Pillow composition: resize, gradient, text overlay, logo. |
| `publish <plan.json>` | Upload-Post photo carousel multipart POST. Logs to `post-history.jsonl`. |
| `mark-processed <url>` | Persist round-robin state. |
| `list-processed` / `new-cycle` | Round-robin admin. |
| `priors` | Dump current `HOT_HOOKS.md` + `HOT_IMAGERY.md` for the agent to read. |
| `log-candidate <plan.json>` | Append the agent's INITIAL plan proposal to `candidate-history.jsonl`. |
| `learn` | Weekly. Pull engagement, refresh both priors. |
| `reflect` | On-demand qualitative pass: candidates vs published. |

The agent decides **what** goes into `plan.json`; the script makes it real — and learns from what shipped.

---

## 🛠️ Manual setup

If you'd rather not delegate the install to an agent:

```bash
git clone https://github.com/mutonby/skill-autoecom ~/Documents/skill-autoecom
cd ~/Documents/skill-autoecom
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env: STORE_URL, GEMINI_API_KEY, UPLOAD_POST_API_KEY, UPLOAD_POST_PROFILE
```

Then, in a Claude Code / OpenClaw / Hermes session:

```
/autoecom
```

The agent walks through Steps 0–9 from `SKILL.md`: preflight → brand kit → pick → plan → generate → compose → visual QA → present → publish → mark-processed.

### Required keys

| Variable | Where to get it |
|---|---|
| `STORE_URL` | Your shop's homepage. |
| `GEMINI_API_KEY` | https://aistudio.google.com/apikey |
| `UPLOAD_POST_API_KEY` | https://app.upload-post.com → Settings |
| `UPLOAD_POST_PROFILE` | https://app.upload-post.com → Manage Users (profile name, **not** the social handle) |

---

## ⚙️ Configuration knobs

| Variable | Default | Meaning |
|---|---|---|
| `STORE_URL` | — | Homepage of the ecommerce store. |
| `GEMINI_API_KEY` | — | Required. Used for nano-banana image generation. |
| `GEMINI_IMAGE_MODEL` | `gemini-2.5-flash-image` | Override to pin a stable GA tag. |
| `UPLOAD_POST_API_KEY` | — | Required. Auth for the publishing endpoint. |
| `UPLOAD_POST_PROFILE` | — | Required. The profile name in Upload-Post's Manage Users. |
| `BRAND_FONT_PATH` | — | Absolute path to a `.ttf` for slide text. Falls back to Impact / Helvetica Bold. |
| `TIMEZONE` | `Europe/Madrid` | Used by Upload-Post if scheduling is added later. |

---

## 🌐 Compatibility

- **Python**: 3.11+.
- **Stores**: tested against WooCommerce. Shopify and other platforms work too as long as product pages expose `schema.org/Product` JSON-LD (most do — Google Shopping requires it). For non-WooCommerce stores, the agent's WebFetch handles the platform differences.
- **Image model**: `gemini-2.5-flash-image` (nano-banana). Override via `GEMINI_IMAGE_MODEL` in `.env`.
- **Publishing**: Upload-Post `/api/upload_photos` carousel endpoint. Free tier supports IG + TikTok photo posts.

---

## ⚠️ Limits & caveats

- **Product fidelity** — nano-banana can drift the product's look on stylized scenes. The agent visually QAs every slide and flags drift before showing it to you.
- **Carousel size** — Instagram caps at 10 slides. The skill caps at 10 automatically.
- **TikTok** — always uploaded as draft (`post_mode=MEDIA_UPLOAD`). You finish the post in the TikTok app.
- **Rate limits** — nano-banana has per-minute quotas. Generating a full 8-slide carousel in one run is fine; running 10+ products back-to-back may hit limits.
- **API keys in chat** — if you paste a key into the agent conversation, the key ends up in the conversation logs. Rotate it after testing.

---

## 🧠 Why a Skill (not a one-shot script)

The pipeline has explicit human-in-the-loop checkpoints (slide QA, carousel approval, dry-run before publish) and the brand-identity work benefits massively from running on a multimodal agent rather than a regex scraper. A regex picks the wrong logo when the homepage features other brands' logos; the agent can look at the page and identify the actual store logo unambiguously. A regex can't infer brand voice — the agent reads the homepage and writes a voice profile that matches.

That's why this is a Skill, and that's why it's designed first-class for **Hermes** and **OpenClaw**: harnesses that already have the daily-routine + messaging-bridge plumbing this workflow needs.

---

## 📜 License

MIT © [@mutonby](https://github.com/mutonby)
