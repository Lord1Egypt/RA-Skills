---
name: autoecom
description: "Turn any ecommerce store into daily Instagram & TikTok product carousels. AI pipeline: agent auto-extracts brand kit (logo, colors, font, voice) from the store URL via WebFetch + vision, picks the next bestseller round-robin, generates 3–8 stylized slide images with nano-banana (Gemini 2.5 Flash Image) using the real product photo as reference, composes branded slides with Pillow, you approve, Upload-Post publishes. Use when the user wants daily product carousels, mentions autoecom, ecommerce content, product slides, shop content automation, or asks for the daily carousel batch."
license: MIT
compatibility: "Requires Python 3.11+, google-genai SDK, Pillow, beautifulsoup4, lxml, requests, and internet access for the store URL, Gemini, and Upload-Post APIs. Designed to run inside an agent harness (openclaw / Claude Code) — works headless on a VPS as long as the agent has WebFetch."
metadata:
  author: mutonby
  version: "1.0.1"
  homepage: "https://github.com/mutonby/skill-autoecom"
  primaryEnv: UPLOAD_POST_API_KEY
  requires:
    bins: [python3]
    env: [STORE_URL, GEMINI_API_KEY, UPLOAD_POST_API_KEY, UPLOAD_POST_PROFILE]
  envVars:
    - { name: STORE_URL,            required: true,  description: "Storefront URL the agent crawls for brand kit + bestsellers (e.g. https://www.your-shop.com)" }
    - { name: GEMINI_API_KEY,       required: true,  description: "Google Gemini API key — used for both text (2.5 Flash) and image generation (nano-banana, 2.5 Flash Image)" }
    - { name: UPLOAD_POST_API_KEY,  required: true,  description: "Upload-Post API key (https://app.upload-post.com → Settings → API Keys)" }
    - { name: UPLOAD_POST_PROFILE,  required: true,  description: "Upload-Post profile name with the connected Instagram + TikTok accounts" }
    - { name: TIMEZONE,             required: false, description: "IANA timezone for daily scheduling (default: Europe/Madrid)" }
    - { name: OUTPUT_FOLDER,        required: false, description: "Absolute path where carousel output is written (default: <skill>/output)" }
    - { name: GEMINI_IMAGE_MODEL,   required: false, description: "Override the nano-banana image model (default: gemini-2.5-flash-image)" }
    - { name: GEMINI_TEXT_MODEL,    required: false, description: "Override the Gemini text model (default: gemini-2.5-flash)" }
    - { name: BRAND_FONT_PATH,      required: false, description: "Absolute path to a .ttf for slide text. Falls back to a system bold font if unset." }
---

# AutoEcom — Daily Product Carousel Pipeline

Pipeline tooling lives at `~/Documents/skill-autoecom/`. Each day this skill picks ONE product from the store's bestseller list, generates a 3–8 slide stylized carousel, shows it to the user for approval, and publishes it as a photo carousel to Instagram + TikTok via Upload-Post.

## Architecture: agent-driven, script-as-glue

This skill deliberately splits responsibilities:

- **You (the agent)** do the creative + identity work: identify the logo, pick brand colors, infer brand voice, pick which bestseller to feature, plan the slide structure, write the on-image text, write the post caption. You use `WebFetch`, `Read` (multimodal vision on images), and `Write` directly. **You are not delegating these to a closed Python script** — that's the whole point. A regex can mistake a featured-brand logo for the store's logo; you can't.
- **The Python script (`autoecom.py`)** handles only the mechanical bits you can't do yourself: download a URL, extract a hex palette from an image, parse JSON-LD, call the nano-banana API, run Pillow composition, post a multipart carousel to Upload-Post, persist state.

Every step below makes that split explicit. When you see "you do X" — write it / decide it directly. When you see a `python autoecom.py …` command — run it.

## Setup (only if not yet configured)

### 1. Python environment
```bash
cd ~/Documents/skill-autoecom && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

### 2. `.env`
File lives at `~/Documents/skill-autoecom/.env`. Required keys:

```
STORE_URL=https://www.your-shop.com
GEMINI_API_KEY=...
UPLOAD_POST_API_KEY=...
UPLOAD_POST_PROFILE=...
TIMEZONE=Europe/Madrid
```

If a required key is missing, ask the user for it before continuing.

### 3. Upload-Post account
- Sign up at https://upload-post.com → dashboard at https://app.upload-post.com.
- Connect Instagram (Business/Creator account linked to a Facebook Page) and TikTok via OAuth in the dashboard.
- In **Manage Users**, create a profile — its name is `UPLOAD_POST_PROFILE` (NOT the social handle).
- Generate an API key in **Settings**.
- Verify: `curl -H "Authorization: Apikey $UPLOAD_POST_API_KEY" https://api.upload-post.com/api/uploadposts/me`.

## Orchestration model

This skill is invoked **daily** by an agent harness (Hermes / openclaw / Claude Code), which also handles the messaging bridge (Telegram, WhatsApp, or whatever channel the user has configured). The skill itself does NOT talk to Telegram or any messenger directly — it just runs the pipeline and presents the carousel as text + absolute file paths. The harness forwards the slides to the user's phone, captures the user's reply, and feeds it back into the conversation.

If the skill is invoked outside a harness (e.g., user runs `/autoecom` directly in Claude Code), the same prompts work — they just appear in the terminal instead of on the phone.

### Two scheduled routines (REQUIRED — install on first run)

This skill is **not designed to be run on demand**. It only works as expected when the harness has two cron-style routines installed. **On the very first invocation, BEFORE running Step 0, the agent MUST verify both routines exist and offer to create whichever is missing.** Without these, the round-robin cycle stalls and the learning loop never fires.

| Routine | Cadence | Cron expression | What it does |
|---|---|---|---|
| **`/autoecom` daily** | every day, 09:00 local time | `0 9 * * *` | Runs Steps 0–9: pick next product → plan → generate → compose → present carousel **via the configured messenger** for approval → publish → mark-processed. |
| **`/autoecom-learn` weekly** | Mondays 09:00 local time | `0 9 * * 1` | Runs `python autoecom.py learn`, then **posts a summary in the same messenger channel** with the patterns Gemini extracted + sample sizes + a link to the audit file. |

**How to install** (pick the path that matches the harness):

- **Hermes**: ask Hermes to schedule a recurring routine — *"schedule `/autoecom` every day at 09:00, and `/autoecom-learn` every Monday at 09:00, both reporting to my Telegram"* (or WhatsApp / whatever channel is configured). Hermes will write the routine itself.
- **openclaw**: same pattern — openclaw has a built-in scheduler. Use its `schedule` / `routine` mechanism.
- **Claude Code (local-only)**: install via system crontab. Example:
  ```
  0 9 * * *  cd ~/Documents/skill-autoecom && ./venv/bin/python -c "import os; os.system('claude /autoecom')"
  0 9 * * 1  cd ~/Documents/skill-autoecom && ./venv/bin/python autoecom.py learn
  ```
  (For Claude Code without a messenger bridge, the daily run will surface the carousel in the terminal — which means the user has to be at their machine. Recommend Hermes / openclaw for hands-off operation.)

**On first invocation, do this BEFORE Step 0:**

1. Detect the harness (Hermes vs openclaw vs Claude Code) by looking at environment / available tools.
2. Ask the user once: *"¿Quieres que programe las dos rutinas (carrusel diario 09:00 + aprendizaje semanal lunes 09:00) en \<harness\>, enviando los carruseles a tu \<canal: Telegram/WhatsApp/etc.\>? Necesitarás dar el ok cada día desde tu móvil."*
3. If yes → install both routines and confirm. If no → continue but **warn explicitly**: *"OK, sin rutinas el ciclo round-robin no avanza si te olvidas de invocarme manualmente, y el `learn` semanal no se dispara — los priors quedarán congelados."*
4. If the user says they already have routines → trust them but show what you found (whatever the harness reports) so they can verify.

### Learn-day reporting (the agent MUST do this on every weekly learn run)

After `python autoecom.py learn` finishes, the agent reads `learnings/runs/learn-YYYY-MM-DD.md` and **sends a digest to the configured messenger** so the user understands what changed without opening files. Format:

> 📊 **Aprendizaje semanal — \<date\>**
>
> Cohorte: N carruseles con métricas (ventana \<soak\>–\<max-age\> días).
>
> **Top hooks** (de `HOT_HOOKS.md`):
> - bullet 1 — *evidencia: 4/5 winners, 0/5 losers*
> - bullet 2 — *…*
>
> **Top imagery** (de `HOT_IMAGERY.md`):
> - bullet 1 — *…*
> - bullet 2 — *…*
>
> Cambios respecto a la semana pasada: \<resumen breve de qué se añadió/quitó\>.
> Auditoría completa: `learnings/runs/learn-YYYY-MM-DD.md`.

If `learn` returned "not enough data" (<5 winners + 5 losers), say so honestly: *"Esta semana no hay suficientes datos para refrescar los priors (cohorte de N carruseles). Se necesitan al menos 10 con métricas maduras. Volveré a intentarlo el próximo lunes."*

This message is the user's only window into the learning loop — without it, the priors evolve invisibly and trust erodes. **Always send it.**

## Daily workflow

### Step 0 — Preflight (run on every invocation, do not skip)

Check that the environment is ready and ask the user for whatever is missing:

1. **venv** — does `~/Documents/skill-autoecom/venv/bin/python` exist? If not, run setup step 1. Mechanical, do it without asking.
2. **`.env` file** — verify each required key:
   - `STORE_URL` → if missing, ask: *"¿Cuál es la URL de tu tienda? (la home, no una ficha)."*
   - `GEMINI_API_KEY` → if missing, ask: *"Falta la API key de Gemini. Pégamela (la generas en https://aistudio.google.com/apikey)."*
   - `UPLOAD_POST_API_KEY` and `UPLOAD_POST_PROFILE` → if missing, ask: *"Necesito la API key de Upload-Post y el nombre del profile (Manage Users en https://app.upload-post.com)."*

If the user provides an API key in the conversation, write it to `.env` immediately, never echo it back, and **warn that the key is now in conversation logs and they should rotate it after testing.**

### Step 1 — Brand kit (you do this, with Python only as utility)

Goal: produce `state/brand_kit.json` with fields:

```json
{
  "store": "https://www.example.com",
  "fetched_at": "2026-05-06T12:00:00",
  "logo_url": "https://...",
  "logo_path": "/Users/.../skill-autoecom/state/logo.png",
  "primary_color": "#202828",
  "accent_color": "#f0a810",
  "palette": ["#202828", "#f0a810", "#f09810", "#202020", "#f0a010"],
  "font_family": "Roboto",
  "voice": {
    "language": "es",
    "tone": "professional, helpful, no-nonsense",
    "audience": "DIY-ers and small contractors",
    "positioning": "Affordable hardware delivered fast.",
    "do": ["short sentences", "concrete benefits", "use store name occasionally"],
    "dont": ["hype", "emojis everywhere", "salesy clichés"]
  }
}
```

**Cache check first.** If `state/brand_kit.json` exists and `fetched_at` is < 7 days old AND `store` matches `STORE_URL`, reuse it. Print a one-line confirmation and skip to Step 2. Otherwise:

1. **Identify the logo URL.** `WebFetch <STORE_URL>` and ask the response model: *"What is the EXACT URL of this store's own logo (not a featured brand or product), looking at the HTML? Return only the URL."* Cross-check that the URL contains the store's brand name in its filename — if it doesn't, fetch again with a more pointed prompt or look at `<img class="custom-logo">` (WordPress) / `<header> img` directly.
2. **Download the logo.** `python autoecom.py download <LOGO_URL> state/logo.png`. (For SVG logos, save with `.svg` extension instead — Pillow can't read SVG, but you'll fall back to the colors hex you read from the page.)
3. **Extract the color palette.** Two ways, run both and reconcile:
   - Mechanical: `python autoecom.py palette state/logo.png` → JSON list of hex colors.
   - Visual: `Read state/logo.png` yourself. Look at the image. Pick the **primary** color (the dominant brand color, what the user would call "the brand's signature color") and the **accent** (the contrast color, what's used for text on top of the primary). The mechanical palette tells you what colors EXIST in the logo; you decide which is primary vs accent based on what looks like the brand identity.
4. **Identify the font.** `WebFetch <STORE_URL>` again, ask: *"What font-family does this site use for headings? Look at Google Fonts `<link>` tags first, then inline CSS. Return just the family name."*
5. **Infer brand voice.** `WebFetch <STORE_URL>` once more, ask: *"From the homepage copy, summarize the brand voice as JSON with keys `language` (ISO 639-1), `tone` (one line), `audience` (one line), `positioning` (one sentence), `do` (3 bullets), `dont` (3 bullets). Be concrete."* Take the JSON.
6. **Write `state/brand_kit.json`** with the `Write` tool, combining all of the above plus `store`, `fetched_at` (today), and `logo_path` (absolute path of the file you just downloaded).

You can call WebFetch multiple times for the same page — it's cached for 15 minutes, so re-asking with different questions is cheap.

### Step 2 — Pick the product

Goal: identify the next product URL to feature, in round-robin order over the top bestsellers.

1. **Fetch the bestsellers listing.** WooCommerce: `WebFetch <STORE_URL>/tienda/?orderby=popularity` (Spanish stores) or `<STORE_URL>/shop/?orderby=popularity` (English). Ask: *"List the first 50 product URLs in order, one per line. Skip category links, search results, and 'add to cart' links. A product URL on this site looks like `/producto/<slug>/` or `/product/<slug>/`."*
   - If the prompt returns < 20 URLs, paginate: fetch page `&paged=2`, `&paged=3`, etc.
   - For non-WooCommerce stores, ask the user how their bestsellers page is structured.
2. **Read state.** `python autoecom.py list-processed` returns the current `processed.json`. Look at:
   - `cycle_started_at` (ISO timestamp).
   - `products[]`: each entry has `url`, `last_processed_at`, `cycles_count`.
3. **Pick.** First product URL from the bestsellers list whose `last_processed_at` is older than `cycle_started_at` (i.e. not yet processed in the current cycle). If every product in the list has been processed in the current cycle, run `python autoecom.py new-cycle` to start a new one, then pick the top bestseller. Mention this to the user briefly: *"Empezando un nuevo ciclo — ya hicimos un carrusel de este producto N veces, vamos a por un ángulo nuevo."*
4. **Confirm with the user briefly** before spending tokens on planning + image generation: *"Hoy toca: **\<product name\>** → \<URL\>. ¿Sigo o prefieres saltar?"* (Skip optional but recommended for the first few runs while the user calibrates the round-robin.)

### Step 3 — Plan the carousel (you write `plan.json` directly)

Goal: write `output/YYYY-MM-DD/<slug>/plan.json` with the full carousel plan.

0. **Pull the priors.** `python autoecom.py priors` returns `{"hooks": "...", "imagery": "..."}`. These are auto-managed `HOT_HOOKS.md` and `HOT_IMAGERY.md` files refreshed weekly by `learn` based on real engagement. **`hooks` is YOUR creative input** — read it before writing slide-1 `text_overlay` and treat its bullets as evidence-backed priors (e.g. "hooks <8 words convert 3x"). **`imagery` is auto-prepended by the script** to every nano-banana call inside `generate`, so you don't have to inject it manually — just be aware it's there. If both fields are empty (cold start), proceed without priors.
1. **Get the product data.** `python autoecom.py product <PRODUCT_URL>` returns the JSON-LD parsed dict (name, description, price, currency, images, rating, brand, sku). If it returns very thin data (no images, no description), `WebFetch <PRODUCT_URL>` and write the dict yourself.
2. **Decide the carousel structure.** 3–8 slides depending on substance. Slide 1 is always a **hook** that stops the scroll. Last slide is a **soft CTA**. Middle slides cover: feature/benefit, lifestyle/use-case, social proof (only if rating exists with reviews), spec/quality detail, "vs alternative" comparison if it makes sense.
3. **Write the on-image text** (`text_overlay`) for each slide. Hard rules:
   - ≤ 8 words per slide.
   - Match the brand's language (`brand.voice.language`).
   - Hook + CTA in uppercase work well — the composer auto-uppercases those roles.
   - Brand voice from `state/brand_kit.json` is the contract: hit the `do` bullets, avoid the `dont` bullets.
4. **Write the image generation prompt** (`image_prompt`) for each slide. The image model is nano-banana — it receives the **first product photo** plus this prompt. Hard rules:
   - **Always reference "the product in the attached photo"** so nano-banana keeps fidelity.
   - Then describe stylized scene, lighting, background, composition. Stylize but keep the product accurate and recognizable. (User policy: stylization is OK, drift that makes the product unrecognizable is not.)
   - You can override the reference image per slide with `"ref_image_index": N` (0-indexed into `product.images`) if a specific product photo fits better.
5. **Write the caption** — 2–5 sentences, brand voice, soft CTA at the end ("link en bio", "cómpralo en \<store domain\>", etc.).
6. **Write the hashtags** — 8–15, mix of broad + niche, matching the product category and brand language.
7. **Write `plan.json`** with the `Write` tool. Schema:

```json
{
  "url": "<PRODUCT_URL>",
  "created_at": "<ISO_TIMESTAMP>",
  "language": "es",
  "caption": "...",
  "hashtags": ["#...", "#..."],
  "slide_count": 5,
  "brand": {
    "primary_color": "#...",
    "accent_color": "#...",
    "logo_path": "/abs/path/to/state/logo.png"
  },
  "product": { "url": "...", "name": "...", "description": "...", "images": ["..."], "...": "..." },
  "slides": [
    {
      "role": "hook",
      "text_overlay": "BIG WORDS HERE",
      "image_prompt": "Detailed image-model prompt referencing the attached product photo.",
      "ref_image_index": 0
    },
    { "role": "feature", "text_overlay": "...", "image_prompt": "..." }
  ]
}
```

The `brand` block in `plan.json` is only the subset the composer needs (primary, accent, logo path). The rest of the brand kit (voice, font) was already used as input when YOU wrote the slide text — it doesn't need to be passed to the composer.

### Step 3.5 — Log the candidate (before user editing)

```bash
python autoecom.py log-candidate "output/YYYY-MM-DD/<slug>/plan.json"
```

This appends the INITIAL plan to `learnings/candidate-history.jsonl` so `reflect` can later compare what you proposed against what actually shipped (after any user edits in Step 6). **Run this exactly once, right after writing `plan.json` for the first time.** Do NOT re-run it after the user requests regenerations — that would muddy the learning signal. The script computes a `candidate_id` (sha1 of the plan); if the user publishes the carousel unchanged, the same id will appear in `post-history.jsonl` and `reflect` will count it as approved-unchanged. If they edit, the ids diverge and reflect counts the original as edited/rejected.

### Step 4 — Generate slide images with nano-banana

```bash
python autoecom.py generate "output/YYYY-MM-DD/<slug>/plan.json"
```

For each slide in the plan, calls `gemini-2.5-flash-image` with the referenced product image plus the slide's `image_prompt`. Saves raw outputs to `output/YYYY-MM-DD/<slug>/raw/slide_NN.png`. Skips slides already generated unless `--force` is passed.

This is the slow step (1–3 seconds per slide call). For a 5-slide carousel, expect ~10–15 seconds. Errors here are usually quota / rate limit issues — back off and retry.

### Step 5 — Compose final slides (Pillow overlay)

```bash
python autoecom.py compose "output/YYYY-MM-DD/<slug>/plan.json"
```

Per slide:
1. Resize the raw nano-banana image to fully cover the **1080×1350** (4:5) canvas with a center crop.
2. Add a subtle bottom gradient (45% of frame, fades to 70% black) so text is always legible.
3. Render `text_overlay` left-aligned, bottom of frame, with brand-driven font + colors (uppercase for `hook`/`cta` roles). Auto-shrinks the font size until it fits in 86% of the canvas width.
4. Paste the brand logo at bottom-left.

Outputs `slide_01.png` … `slide_NN.png` in the date/slug folder.

### Step 5.5 — Visual QA of the carousel (you do this yourself, no Gemini call)

You are multimodal. **Use that.** Before showing the carousel to the user, open every composed `slide_NN.png` with the **Read** tool — Claude / openclaw both view PNGs directly.

For each slide, evaluate:

1. Is the on-image text fully visible? Any letter clipped at the edges?
2. Is the product still recognizable in the stylized image? (nano-banana sometimes drifts — flag if the product looks wrong.)
3. Does the logo overlap with the text or the product?
4. Are accent marks / special characters (`á é í ó ú ñ ¿ ¡`) rendering correctly?
5. Does the slide order make narrative sense (hook → middle → cta)?
6. Any rendering glitch: garbled text, missing logo, gradient banding?

**Add a "QA" column to the Step 6 table** with one of:
- `✅` — clean
- `⚠️ <issue>` — flag the specific problem (e.g. `⚠️ producto irreconocible`, `⚠️ acento "ó" recortado`)

**Do NOT silently drop flagged slides** — show them to the user with the warning so they can decide whether to regenerate that single slide, regenerate the whole carousel, or ship as-is.

### Step 6 — Present to the user

Show a markdown table:

| # | Role | Text | QA | File |
|---|------|------|----|------|
| 1 | hook | "..." | ✅ | output/YYYY-MM-DD/<slug>/slide_01.png |
| 2 | feature | "..." | ⚠️ producto irreconocible | output/YYYY-MM-DD/<slug>/slide_02.png |
| … | … | … | … | … |

Then show the **caption** and **hashtags** below the table.

**Always include the absolute file paths in the table** — openclaw uses them to attach the actual slide images when it forwards the message to the user's messenger. Without absolute paths the user sees only metadata and cannot review the carousel visually.

Then ask:

> **¿Publico el carrusel? (`sí` para publicar, `no` para descartar, o dime qué slide regenerar.)**

Wait for the user's reply (it will arrive via openclaw from the user's phone).

**If the user replies `no`** (rejects the carousel), skip directly to Step 8 and `mark-processed` with `--slides 0`. This consumes the product so tomorrow's run picks the next one — otherwise the same rejected product would surface again. If the user wants to retry the same product later, they can manually remove its entry from `state/processed.json`.

**If the user asks to regenerate slide N**, edit `plan.json` (you may rewrite the `image_prompt`, `text_overlay`, or `ref_image_index`), delete `raw/slide_NN.png`, then re-run `generate` (it will only regenerate the missing slide unless `--force`) and `compose`. Re-present.

### Step 7 — Publish

```bash
python autoecom.py publish "output/YYYY-MM-DD/<slug>/plan.json" \
    --platforms instagram,tiktok \
    --tiktok-mode draft \
    --dry-run
```

**Always run with `--dry-run` first** and show the user the exact request payload. Only execute the real publish (without `--dry-run`) after explicit "go".

The publish call uploads the composed `slide_*.png` files (sorted, max 10) as a **photo carousel** via `POST /api/upload_photos`. The caption from `plan.json` plus hashtags is sent as the `caption` field. TikTok mode is `draft` by default per project policy (`MEDIA_UPLOAD` → goes to TikTok inbox, never auto-publishes).

### Step 8 — Mark product as processed

```bash
python autoecom.py mark-processed "<PRODUCT_URL>" --slides <N> --store "<STORE_URL>"
```

Updates `state/processed.json` so tomorrow's `pick` skips this product. **Run this even if `--slides 0`** (the user rejected the carousel) — a rejected product is still consumed.

### Step 9 — Final summary

Print one line: product name, number of slides published, platforms, and the carousel folder path.

## Learning loop (`learn` weekly, `reflect` on demand)

This skill **gets smarter over time**. Two priors are maintained automatically and refreshed from real engagement data:

- **`learnings/HOT_HOOKS.md`** — patterns of slide-1 hook copy that converted. You read this in **Step 3.0** when writing `text_overlay` for the hook slide.
- **`learnings/HOT_IMAGERY.md`** — image-prompt patterns (lighting, composition, framing) that performed well. **Auto-prepended by `generate` to every nano-banana call** — no agent action needed.

Two priors instead of one (vs. autoshorts) so the engine can isolate what's working visually from what's working textually.

### `learn` — weekly, metrics-driven

```bash
python autoecom.py learn
# optional flags: --soak-days 7 --max-age-days 90 --top-pct 0.20 --bottom-pct 0.20
```

Pulls Upload-Post analytics for every carousel in `post-history.jsonl` whose age is in `[soak-days, max-age-days]`. Computes a composite z-score per carousel (`0.6·z(views) + 0.4·z(engagement_rate)`), takes the top 20% as winners and bottom 20% as losers, then makes **two separate Gemini calls** — one per prior:

1. Refresh `HOT_HOOKS.md` from winners' vs losers' `hook_text`.
2. Refresh `HOT_IMAGERY.md` from winners' vs losers' `image_prompts`.

Old priors are backed up as `HOT_HOOKS.YYYYMMDD-HHMMSS.md.bak` and `HOT_IMAGERY.YYYYMMDD-HHMMSS.md.bak`. A full audit lands in `learnings/runs/learn-YYYY-MM-DD.md`.

**When to run**:
- Manually, on demand: `python autoecom.py learn`.
- Scheduled, weekly via cron / openclaw / Hermes: `0 9 * * 1 cd ~/Documents/skill-autoecom && ./venv/bin/python autoecom.py learn`.
- Skip if `post-history.jsonl` has fewer than ~10 entries — `learn` will short-circuit and write a "not enough data" note.

### `reflect` — on demand, qualitative

```bash
python autoecom.py reflect --window-days 30
```

Compares `candidate-history.jsonl` (initial agent proposals, logged in Step 3.5) against `post-history.jsonl` (final carousels that shipped) within the window. A candidate is "approved-unchanged" if its `candidate_id` appears in posts; otherwise it's "edited or rejected". Sends both buckets to Gemini and asks for **two sets of observations** — hook patterns + imagery patterns — that explain the user's filter.

Output goes to `learnings/runs/reflect-YYYY-MM-DD-HHMM.md` and is **NOT auto-promoted** to `HOT_HOOKS.md` or `HOT_IMAGERY.md`. Reflect can lock in your past biases ("I always reject question hooks") rather than what actually performs, so it stays observational. Read it, copy whatever's useful into `learnings/insights/` (manual notes), and let `learn` keep refreshing the actual priors based on engagement.

### Why this is better than autoshorts' learning loop

- **Two priors, not one**: hook and imagery are independent variables; mixing them masks signal.
- **Auto-prepended imagery prior**: the agent doesn't have to remember to inject it — `generate` does it silently.
- **Edit-as-rejection signal**: `reflect` uses `candidate_id` collision to detect whether the user shipped your plan unchanged or revised it. That's a stronger signal than the binary approve/reject autoshorts uses.

### Don'ts

- Do not edit `HOT_HOOKS.md` or `HOT_IMAGERY.md` by hand AND keep running `learn` — `learn` will overwrite. Manual rules go in `learnings/insights/`.
- Do not delete `post-history.jsonl`, `candidate-history.jsonl`, or `metrics.jsonl` — they're append-only memory.
- Do not run `learn` more than once a week — Gemini will just churn the same patterns.
- Do not call `log-candidate` more than once per planning session — only the FIRST plan, before any user editing.

## Carousel format constraints

- **Aspect ratio**: 1080×1350 (4:5). IG carousel native. TikTok photo posts accept 4:5 fine.
- **Slide count**: 2–10 (Instagram caps carousels at 10). The planner targets 3–8.
- **TikTok always draft** (`post_mode=MEDIA_UPLOAD`). The user always reviews on the phone before publishing on TikTok.
- **No Reels / Shorts video output** — this skill is image-only. For vertical video clips, use the `autoshorts` skill instead.

## Files & layout

```
skill-autoecom/
├── SKILL.md            # this file
├── autoecom.py         # utility CLI: download, palette, product, generate, compose, publish, state
├── README.md           # human-readable setup
├── requirements.txt
├── .env
├── input/              # currently unused (reserved for brand assets the user wants forced in)
├── output/
│   └── 2026-05-06/
│       └── <slug>/
│           ├── plan.json
│           ├── raw/
│           │   ├── _ref.jpg
│           │   └── slide_NN.png  # raw nano-banana output
│           ├── slide_NN.png      # final composed slide
│           └── publish.json
├── state/
│   ├── brand_kit.json
│   ├── logo.png
│   └── processed.json
└── learnings/
    ├── HOT_HOOKS.md             # auto-managed by `learn`, read by agent in Step 3.0
    ├── HOT_IMAGERY.md           # auto-managed by `learn`, auto-prepended in `generate`
    ├── candidate-history.jsonl  # every initial plan proposal (Step 3.5)
    ├── post-history.jsonl       # every carousel that shipped (written by `publish`)
    ├── metrics.jsonl            # snapshots from Upload-Post post-analytics
    ├── runs/
    │   ├── learn-YYYY-MM-DD.md
    │   └── reflect-YYYY-MM-DD-HHMM.md
    └── insights/                # MANUAL notes (not used by the pipeline)
```
