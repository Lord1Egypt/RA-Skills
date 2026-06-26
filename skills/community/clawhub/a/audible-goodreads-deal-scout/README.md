# Audible Goodreads Deal Scout

Never miss an Audible deal for a book you actually want to read.

Audible Goodreads Deal Scout is a **ClawHub / OpenClaw skill** that checks Audible promotions against Goodreads ratings, your Goodreads shelves, and optional reading-taste notes. It is built for people who want fewer random deal notifications and more "this is actually relevant to me" recommendations.

The goal is not to buy more audiobooks. The goal is to notice the few Audible deals that match books you already care about.

The skill reports opportunities only. It does not buy, reserve, check out, redeem credits, manage subscriptions, or complete purchases.

For a concise security and data-access summary, see [TRUST.md](TRUST.md).

## Use This Skill To

Use this skill to:

- Check today's Audible daily deal and get a short recommendation.
- See whether the deal is already on your Goodreads Want-to-Read shelf.
- Suppress books you already marked as read or currently reading.
- Scan your Goodreads Want-to-Read shelf for Audible titles with visible discounts.
- Rank discounted Want-to-Read matches by deal strength and Goodreads signal.
- Create highly personalized recommendations from your Goodreads shelves, ratings, reviews, and taste notes.
- Explain why a book may or may not fit your reading preferences, instead of only showing a generic score.
- Optionally check member-visible Audible cash prices with a local Audible auth token.
- Optionally deliver good matches to Telegram or another configured OpenClaw channel.

If you do not want personalization, the skill still works with public Goodreads ratings only.

## How To Get The Most Value

The skill works with public data only, but it gets much better when you give it a little personal context.

The best setup is:

1. Export your Goodreads library CSV.
   Use the official Goodreads library exporter from Goodreads' `Import and Export` page. This lets the skill know what you already read, what you are currently reading, and what is on your Want-to-Read shelf.
2. Add short taste notes.
   A few paragraphs are enough. You can write them yourself, dictate them quickly, or ask an AI to draft taste notes from your favorite books, disliked books, preferred genres, and reading habits. These notes help the skill explain whether a deal actually fits you, not just whether it is popular.
3. Optionally add Audible authentication for member prices.
   Anonymous Audible pages often hide cash prices or show credit-based buying options. If you provide a local Audible auth token, the skill can check member-visible cash prices for matched titles and produce a more useful Want-to-Read discount report.

With all three pieces, the skill can help keep track of:

- today's Audible promotion
- whether the book is already in your Goodreads library
- whether it is on your Want-to-Read shelf
- whether it looks like a good fit for your taste
- which Want-to-Read books are available on Audible
- which matched titles appear discounted or priced below list
- which deals are worth looking at first

If you are looking at this repository on GitHub, you are looking at the **source for a publishable ClawHub skill**, not a generic Python app or a standalone website.

If you want to re-implement the workflow without using the shipped skill directly, see [PROMPT_REQUEST.md](PROMPT_REQUEST.md). It captures the intention, scope, design guardrails, edge cases, and example prompt in one place.

## Install or publish

If you just want to use it in OpenClaw once it is published:

```bash
openclaw skills install audible-goodreads-deal-scout
```

Start a new OpenClaw session after install or after changing skill config so the fresh skill snapshot is picked up cleanly.

If you want to publish your own version from this repo:

```bash
clawhub login
clawhub publish . \
  --slug audible-goodreads-deal-scout \
  --name "Audible Goodreads Deal Scout" \
  --version 0.1.14 \
  --changelog "Harden OpenClaw CLI discovery, add installed-version diagnostics, and surface disabled cron jobs." \
  --tags latest
```

## 5-minute setup

If you want one straightforward setup path, use this:

1. Pick your Audible store. If you do nothing, it defaults to `us`.
2. Export your Goodreads library CSV if you want personalization.
3. Optionally create a short notes file with what you like and dislike.
4. Run:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh setup
```

The setup response includes `nextSteps` with ready-to-run commands for `doctor`, checking the daily deal, scanning Want-to-Read books when a CSV is configured, and optional Audible auth.

By default, the skill writes its config, state, and artifacts under `.audible-goodreads-deal-scout/` in the active OpenClaw workspace.

That storage lives in the workspace, not inside `skills/audible-goodreads-deal-scout/`, because `openclaw skills install` and `openclaw skills update --force` can replace the installed skill folder.

Only point `goodreadsCsvPath`, `notesFile`, `configPath`, and `stateFile` at files or directories you actually want this skill to read or write.

5. Then evaluate the current deal:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh prepare \
  --config-path .audible-goodreads-deal-scout/config.json
```

## How to get your Goodreads CSV

If you use Goodreads, the skill gets much stronger when you export your library.

The usual path is:
1. Open `My Books`
2. Open `Import and Export`
3. Choose `Export Library`
4. Wait for Goodreads to generate the file
5. Download the CSV and point the skill at it with `goodreadsCsvPath`

Why the CSV matters:
- it tells the skill what you already marked as `read`
- it tells the skill what is already on your `to-read` shelf
- it gives the fit step access to your ratings and written reviews

If your export is old, the skill will warn you, but it can still run.

## If you do not use Goodreads

That is still a valid setup.

You can use a notes-only workflow:
- no Goodreads CSV
- one strong text file about your taste

The better the notes, the better the fit paragraph.

Good notes usually include:
- 5 to 15 books or authors you genuinely liked
- a few examples of books you disliked and why
- genres you seek out
- genres you avoid
- pacing preferences
- tone preferences
- what feels too sentimental, too slow, too commercial, too dark, too clever, too flat, and so on

A strong notes file sounds like you talking to a smart bookseller, not like metadata.

Useful:

```md
I like morally serious fiction, political tension, and books with ideas.
I often like Orwell, Ishiguro, Le Guin, Vonnegut, and literary sci-fi.
I lose interest when a book gets too sentimental or too plot-mechanical.
I like books that are sharp, unsparing, and a bit strange, but still readable.
```

Too weak:

```md
I like good books.
```

If you do not have Goodreads, the best setup is:
- a thoughtful notes file
- the default public Goodreads check
- `deliveryPolicy: positive_only`

## How the recommendation works

At a high level:
- the skill fetches the current Audible daily promotion
- it resolves the matching Goodreads page and public rating
- it applies your Goodreads shelf rules if you provided a CSV
- it uses your notes and/or Goodreads history to shape the fit paragraph
- it decides whether to deliver the result based on your delivery policy

### The default Goodreads threshold

The default threshold is `3.8`.

That means:
- a public Goodreads average rating of `3.80` or lower is treated as below your quality cutoff
- a rating above `3.8` is eligible

This is the **public Goodreads average**, not your own rating.

Good starting points:
- `4.0` if you want to be stricter
- `3.8` if you want a balanced default
- `3.6` or `3.7` if you want more titles to pass through

### Goodreads shelf rules

If you provide a Goodreads CSV:
- `read` => suppress
- `currently-reading` => suppress
- `to-read` => recommend immediately

That `to-read` override is intentional. If you already saved the book for later, that is treated as a strong positive signal and it can override the public Goodreads threshold.

## Scan your Want-to-Read shelf for Audible discounts

If you configured a Goodreads CSV, you can also run a manual audit of books on your Goodreads `to-read` shelf:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh scan-want-to-read \
  --config-path .audible-goodreads-deal-scout/config.json \
  --limit 40 \
  --offset 0 \
  --progress plain
```

This is intentionally an on-demand scan, not a scheduled monitor. It helps answer: "Which books I already want to read appear to have a visible Audible discount right now?"

Default behavior:
- scans Audible US only in this first version
- reads the current Goodreads CSV fresh each run
- searches the first Audible result page for each selected Goodreads book
- inspects the first three Audible result cards
- fetches a product page only when the search card already shows plausible numeric discount evidence
- prints compact Markdown to stdout
- writes scan progress to stderr by default, so long runs can be monitored without corrupting Markdown/JSON output
- keeps non-deals out of the default Markdown so the useful deals stay visible
- suppresses duplicate Audible product matches in the final report while preserving scanned-row counts

Useful batching pattern for larger shelves:

```bash
# Day 1
sh ./scripts/audible-goodreads-deal-scout.sh scan-want-to-read \
  --config-path .audible-goodreads-deal-scout/config.json \
  --scan-order newest \
  --limit 40 \
  --offset 0

# Day 2
sh ./scripts/audible-goodreads-deal-scout.sh scan-want-to-read \
  --config-path .audible-goodreads-deal-scout/config.json \
  --scan-order newest \
  --limit 40 \
  --offset 40
```

Useful output flags:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh scan-want-to-read \
  --config-path .audible-goodreads-deal-scout/config.json \
  --output-json .audible-goodreads-deal-scout/reports/want-to-read.json \
  --output-md .audible-goodreads-deal-scout/reports/want-to-read.md \
  --include-non-deals
```

The scan is deliberately conservative. If Audible hides cash pricing behind credits, membership language, or extra buying-choice UI, the result is marked as hidden or unknown instead of guessing. If a title or author match is ambiguous, it is marked for review instead of being treated as a deal.

The Markdown report shows whether authenticated pricing was enabled, live request usage, cache hits/writes, and a suggested next `--offset` command when more selected Want-to-Read books remain.

Pricing fields now separate two ideas:
- `priceBasis` says where the price came from, for example `audible_public_cash` or `audible_member_cash`.
- `dealType` says what kind of opportunity it appears to be, for example `limited_time_sale`, `member_cash_below_list`, or `cash_price_below_list`.

Goodreads ratings:
- If your Goodreads CSV includes an average-rating column, the scan uses it for ranking.
- If the CSV does not include that column, the scan can enrich up to 20 discounted results from public Goodreads book pages when the CSV has Goodreads book ids.
- Use `--no-goodreads-rating-enrichment` if you want to avoid those public Goodreads rating lookups.
- Use `--goodreads-rating-limit N` to adjust the enrichment cap.

Progress output:
- `--progress plain` writes human-readable progress lines to stderr. This is the default CLI behavior.
- `--progress json` writes JSONL progress events to stderr for agents and log processors.
- `--progress none` disables progress output.
- `--progress-interval 5` controls the minimum seconds between item progress updates. Start, stop, and completion events are always emitted when progress is enabled.

For long OpenClaw-agent runs, prefer `--progress json` plus `--output-json` and `--output-md`. Progress goes to stderr, while the report files stay stable and can be read after the command finishes or stops early.

### Optional authenticated Audible price lookup

Anonymous Audible pages often hide cash prices. If you want the Want-to-Read scan to check member-visible pricing on a headless OpenClaw machine, you can create a local Audible auth file through an external-browser flow.

This does **not** put your Audible password in the skill config. The flow prints an Amazon login URL, you open it on another device, complete login there, and paste the final redirect URL back into the CLI.

The resulting auth file is powerful local state: the flow requests cookie-style Audible/Amazon credential types for compatibility, then persists the bearer access/refresh token fields needed for token refresh and member-visible product-price lookup. The skill confines authenticated use to token refresh plus validated Audible product-price lookups on allowlisted API hosts, and `audible-auth-status` reports readiness without printing token contents.

Start auth:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh audible-auth-start \
  --auth-path .audible-goodreads-deal-scout/audible-auth.json \
  --audible-marketplace us
```

Open the printed `loginUrl` in your own browser. After login, Amazon will land on an error or not-found page; copy that final address-bar URL and finish auth:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh audible-auth-finish \
  --auth-path .audible-goodreads-deal-scout/audible-auth.json \
  --redirect-url "<final-amazon-redirect-url>"
```

Then scan with authenticated price lookup:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh scan-want-to-read \
  --config-path .audible-goodreads-deal-scout/config.json \
  --audible-auth-path .audible-goodreads-deal-scout/audible-auth.json \
  --limit 40 \
  --max-requests 90
```

You can also save the auth path in `config.json` as `audibleAuthPath`, or set it during scripted setup with `--audible-auth-path`.

Authenticated scans usually spend one search request plus one authenticated price request for each matched Audible title. Use a higher `--max-requests` value than you would for anonymous scans. The authenticated price parser treats cash prices as the source of truth and ignores Audible credit prices such as `credit_price`.

Authenticated `discounted` means Audible returned a member-visible cash price below its list price for the product. It does not always prove a limited-time sale; check `dealType` in JSON if you need to distinguish `member_cash_below_list` from `limited_time_sale`.

You can test one known Audible ASIN first:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh audible-auth-test-price \
  --auth-path .audible-goodreads-deal-scout/audible-auth.json \
  --asin B08V8B2CGV
```

The test response should include `pricingStatus`, `currentPrice`, `listPrice`, and `discountPercent` when Audible returns visible member cash pricing for that ASIN.

Check auth readiness and file permissions without printing tokens:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh audible-auth-status \
  --auth-path .audible-goodreads-deal-scout/audible-auth.json
```

If the status reports broad file permissions on a local POSIX host, tighten them with:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh audible-auth-status \
  --auth-path .audible-goodreads-deal-scout/audible-auth.json \
  --fix-permissions
```

The auth file is sensitive. Keep it under `.audible-goodreads-deal-scout/` in your OpenClaw workspace, do not commit it, do not paste it into chat, and remove it if you no longer want the skill to have authenticated Audible API access.

## Supported marketplaces

Supported and fixture-tested marketplace keys:
- `us`
- `uk`
- `de`
- `ca`
- `au`

If you do nothing, the default is `us`.

Support here means the repo has fixture-backed coverage for:
- daily-promotion detection
- promotional price extraction
- book identity extraction

Live marketplace behavior can still vary. A supported store may still return:
- no active promotion
- a blocked page
- a page-layout drift error

Daily-promotion fetches use `audibleFetchBackend: "auto"` by default. That means the skill tries the built-in Python fetch path first and falls back to browser-like `curl` when Audible rejects the Python client with recoverable HTTP failures such as `503`. Use `"python"` or `"curl"` only when you deliberately want to force one backend.

The Want-to-Read discount scan is currently US-only. The daily-promotion workflow remains fixture-tested for the marketplace keys listed above.

If you want a non-US store, set `audibleMarketplace` to one of the keys above:

```json
{
  "audibleMarketplace": "uk",
  "audibleFetchBackend": "auto"
}
```

## Privacy and data use

This part should be explicit.

- The Python prep layer reads your Goodreads CSV locally.
- The Python prep layer also reads your notes file locally.
- The skill will read whatever file paths you configure, so keep those paths limited to the files you intend it to use.
- The model step may use fit-context data unless you set `privacyMode` to `minimal`.
- In `privacyMode: "minimal"`, the skill still uses local shelf logic, but it does **not** pass your personal CSV or notes content into the model fit step.
- Delivery targets are whatever you configure in your own OpenClaw runtime.

If you want the safest default for personal data sharing, use:

```json
{
  "privacyMode": "minimal"
}
```

## What a notes file should look like

It does **not** need strict structure. A short, honest, messy note is fine.

Example file: `examples/preferences.example.md`

Good notes usually include:
- books or authors you reliably like
- genres or tones you usually avoid
- pacing preferences
- whether you like literary, commercial, cerebral, emotional, satirical, dark, warm, and so on

Weak notes are still accepted, but they produce weaker fit output. For example, `I like good books` is valid input, but not very useful evidence.

## Delivery policies

`deliveryPolicy` controls how noisy the skill is:

| Policy | Best for | Behavior |
| --- | --- | --- |
| `positive_only` | most people | send only likely fits |
| `summary_on_non_match` | people who want visibility into skips | send full recommendations, but short summary cards for suppressions/errors |
| `always_full` | logging and audits | send every final result in full |

Recommended default:
- `positive_only`

That gives the best signal-to-noise ratio for most users.

## Telegram, WhatsApp, and other channels

This repository does **not** ship its own Telegram or WhatsApp connector.

Instead, it uses the OpenClaw message surface:
- `openclaw message send --channel ... --target ...`

That means delivery works whenever your OpenClaw environment already has a supported channel configured.

### Telegram

If your OpenClaw setup supports Telegram delivery, configure:

```json
{
  "deliveryChannel": "telegram",
  "deliveryTarget": "-1000000000000"
}
```

`deliveryTarget` is the Telegram chat or channel id you want to post into.

### WhatsApp

WhatsApp can work **only if** your OpenClaw install already exposes a WhatsApp-capable message channel.

In that case the pattern is the same:

```json
{
  "deliveryChannel": "whatsapp",
  "deliveryTarget": "<your-whatsapp-target>"
}
```

This repo does not create that WhatsApp channel. It only uses it if your OpenClaw runtime already provides it.

## What the output looks like

### Positive recommendation

```text
Audible US Daily Promotion — 2026-04-20

𝗦𝗹𝗮𝘂𝗴𝗵𝘁𝗲𝗿𝗵𝗼𝘂𝘀𝗲-𝗙𝗶𝘃𝗲 — Kurt Vonnegut (2015)
Price: $1.99 (-87%, list price $14.95)
Goodreads rating: 4.11 (1,364,737 ratings)
Length: 5:13 hrs
Genre: Literature & Fiction, Thought-Provoking, Fiction, Witty

Slaughterhouse-Five is the now famous parable of Billy Pilgrim...

Fit: Strong match, on your to-read shelf. You tend to respond well to fiction that is intellectually playful, structurally bold, and willing to smuggle serious ideas through wit. The main risk is that Vonnegut's emotional distance and satirical flatness may leave you admiring it more than fully feeling it.

Audible: https://www.audible.com/pd/...
Goodreads: https://www.goodreads.com/book/show/...
```

### Short non-match summary

```text
Audible US Daily Promotion — 2026-04-20

𝗦𝗹𝗮𝘂𝗴𝗵𝘁𝗲𝗿𝗵𝗼𝘂𝘀𝗲-𝗙𝗶𝘃𝗲 — Kurt Vonnegut (2015)

Fit: You marked it as read on Goodreads.

Audible: https://www.audible.com/pd/...
```

## One complete walkthrough

If you want to see the whole flow once from start to finish, this is the cleanest path.

1. Write a config and optional notes/delivery settings:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh setup \
  --non-interactive \
  --config-path .audible-goodreads-deal-scout/config.json \
  --audible-marketplace us \
  --audible-auth-path .audible-goodreads-deal-scout/audible-auth.json \
  --threshold 3.8 \
  --goodreads-csv "/absolute/path/to/goodreads_library_export.csv" \
  --notes-file "/absolute/path/to/preferences.md" \
  --delivery-channel telegram \
  --delivery-target "-1000000000000" \
  --delivery-policy positive_only
```

2. Prepare today's deal:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh prepare \
  --config-path .audible-goodreads-deal-scout/config.json
```

That always writes the current prep result to `.audible-goodreads-deal-scout/artifacts/current/prepare-result.json`, including error or suppress outcomes. Ready outcomes also include:
- `runtime-input.json`
- `runtime-prompt.md`
- `runtime-output-schema.json`

3. Let the OpenClaw runtime produce a `runtime-output.json` file that matches the schema from step 2. A typical successful output looks like:

```json
{
  "schemaVersion": 1,
  "goodreads": {
    "status": "resolved",
    "url": "https://www.goodreads.com/book/show/1",
    "title": "Signal Fire",
    "author": "Jane Story",
    "averageRating": 4.15,
    "ratingsCount": 9501
  },
  "fit": {
    "status": "written",
    "sentence": "Fit: Likely to work if you want sharp, idea-driven speculative fiction. The main risk is that it may feel more cerebral than emotionally warm."
  }
}
```

4. Finalize the public result contract:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh finalize \
  --prepare-json .audible-goodreads-deal-scout/artifacts/current/prepare-result.json \
  --runtime-output /tmp/runtime-output.json
```

5. If you configured delivery, send the finished message:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh run-and-deliver \
  --config-path .audible-goodreads-deal-scout/config.json \
  --prepare-json .audible-goodreads-deal-scout/artifacts/current/prepare-result.json \
  --runtime-output /tmp/runtime-output.json
```

If you just want to inspect the decision locally, stop after `finalize`.

## Troubleshooting

Three issues cause most confusing runs:

- Wrong notes path: if `notesFile` or `preferencesPath` points at a missing file, the prep step now returns `error_missing_notes_file` instead of silently continuing.
- Wrong CSV header override: `--csv-column role=Header` must match the Goodreads export header exactly. If you are unsure, run `show-csv-headers` first.
- Stale Goodreads export: if the CSV is old, the skill can still run, but read status, shelf state, and fit evidence may lag behind your actual library.
- Stale scheduled artifact: scheduled `run-and-deliver` refuses error prep results and stale `prepare-result.json` files whose `metadata.storeLocalDate` no longer matches the current Audible marketplace date.
- Stale downstream artifacts: every fresh `prepare` removes old `runtime-output.json`, `run-and-deliver-result.json`, and `mark-emitted-result.json` from the current artifact directory before writing the new prep result.
- Transient Audible daily-deal pages: the prep step retries transient fetch failures and temporary no-active-promotion parses before returning a suppression or error. With `audibleFetchBackend: "auto"`, it can recover from Python-client rejections by retrying the same URL through browser-like `curl`.

Useful checks:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh doctor --config-path .audible-goodreads-deal-scout/config.json
sh ./scripts/audible-goodreads-deal-scout.sh show-csv-headers "/absolute/path/to/goodreads_library_export.csv"
sh ./scripts/audible-goodreads-deal-scout.sh publish-audit --version 0.1.14 --tags latest
```

`doctor` checks the configured config, CSV, notes, auth file, cache directory, delivery settings, cron settings, Audible fetch backend, local OpenClaw binary, bundled shell wrapper, and installed skill version. Add `--check-cron` when you want it to query live OpenClaw cron jobs; disabled related jobs are reported separately from missing jobs.

Add `--check-audible-fetch` when you want a live daily-deal fetch probe from the current host. This is opt-in because it makes a network request to Audible.

If your OpenClaw install strips executable bits from bundled scripts, run the wrapper through `sh` exactly as shown above and in `SKILL.md`.
- Scheduled runs cannot stop for interactive exec approval. If your OpenClaw host keeps `exec` in `allowlist` mode, allowlist the launcher your host expects for `sh .../scripts/audible-goodreads-deal-scout.sh` before enabling daily automation, for example `/bin/sh` when that is the shell your host uses.
- Before enabling `dailyAutomation` or `--register-cron`, confirm the configured delivery channel and target are the ones you actually want the skill to use through your local OpenClaw runtime.

## Advanced CLI usage

If you prefer scripted setup instead of interactive setup:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh setup \
  --non-interactive \
  --config-path .audible-goodreads-deal-scout/config.json \
  --audible-marketplace us \
  --threshold 3.8 \
  --goodreads-csv "/absolute/path/to/goodreads_library_export.csv" \
  --notes-file "/absolute/path/to/preferences.md" \
  --delivery-channel telegram \
  --delivery-target "-1000000000000" \
  --delivery-policy positive_only
```

Useful helper commands:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh doctor --config-path .audible-goodreads-deal-scout/config.json
sh ./scripts/audible-goodreads-deal-scout.sh show-csv-headers "/absolute/path/to/goodreads_library_export.csv"
sh ./scripts/audible-goodreads-deal-scout.sh measure-context --goodreads-csv "/absolute/path/to/goodreads_library_export.csv" --output /tmp/fit-context.json
sh ./scripts/audible-goodreads-deal-scout.sh publish-audit --version 0.1.14
```

Finalize and deliver in one step:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh run-and-deliver \
  --config-path .audible-goodreads-deal-scout/config.json \
  --prepare-json .audible-goodreads-deal-scout/artifacts/current/prepare-result.json \
  --runtime-output /tmp/runtime-output.json
```

## Repository structure

- `SKILL.md`: agent-facing runtime instructions
- `TRUST.md`: security, data-access, and no-purchase behavior summary
- `agents/openai.yaml`: interface metadata and default prompt for OpenClaw agent surfaces
- `scripts/audible-goodreads-deal-scout.sh`: bundled shell wrapper for local CLI and OpenClaw installs that may not preserve executable bits
- `audible_goodreads_deal_scout/core.py`: prep/orchestration logic
- `audible_goodreads_deal_scout/audible_fetch.py`: guarded Audible HTTP fetching, browser-like headers, and curl fallback
- `audible_goodreads_deal_scout/audible_auth.py`: optional headless Audible auth and API price lookup helpers
- `audible_goodreads_deal_scout/audible_catalog.py`: Audible catalog search and conservative price parsing
- `audible_goodreads_deal_scout/cli_errors.py`: structured CLI error payload helpers
- `audible_goodreads_deal_scout/diagnostics.py`: local doctor/status checks
- `audible_goodreads_deal_scout/goodreads_rating.py`: optional public Goodreads rating enrichment for Want-to-Read reports
- `audible_goodreads_deal_scout/want_to_read_scan.py`: Goodreads Want-to-Read scan orchestration and report rendering
- `audible_goodreads_deal_scout/runtime_contract.py`: runtime input, prompt, schema, and prepare-result artifact writing
- `audible_goodreads_deal_scout/rendering.py`: card rendering and delivery planning
- `audible_goodreads_deal_scout/delivery.py`: config, cron, and delivery helpers
- `audible_goodreads_deal_scout/public_cli.py`: setup and CLI entrypoint
- `config.example.json`: public config example
- `examples/preferences.example.md`: sample notes file
- `docs/release-checklist.md`: release checklist for publishable builds

## Publish to ClawHub

Before publishing, run:

```bash
sh ./scripts/audible-goodreads-deal-scout.sh publish-audit --version 0.1.14 --tags latest
```

For public auditability, create a matching Git tag and GitHub release for each ClawHub version, for example `v0.1.14`.

## Why this is worth publishing

The value is not just “show me today’s Audible promotion.”

The real value is:
- filtering instead of promo noise
- combining public quality with personal fit
- respecting `read`, `currently-reading`, and `to-read`
- optional proactive delivery into a real channel
- graceful handling of suppressions and lookup failures
