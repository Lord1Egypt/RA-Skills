# Headless / cron mode

How the skill behaves when no human is at the keyboard — scheduled `/loop` runs, calendar-triggered automations, OpenClaw routines, voice-only contexts where there's no chance to interject. The mode doesn't add new workflows; it constrains the existing ones to make autonomous execution safe and silent unless something blocks.

## When this mode applies

The agent operates in headless mode when **any** of these is true:

- `profile.md → preferred_lookbook_host_auto: true` (explicit opt-in)
- The invocation came from a recurring schedule (`/loop`, cron, OpenClaw routine), AND a prior interactive session opted into recurring deploys
- The invocation context has no chat surface (voice agent doing post-event playback; ambient assistant)

If none of these is set, the agent stays in interactive mode — that's the default. **Headless mode is opt-in**, never inferred from "the user seems busy."

## The five rules

### 1. No questions

The agent doesn't ask anything. If a decision needs to be made:

- Take the documented default (see § "Defaults" below).
- If no default exists for the decision and skipping it would block the run, **fail loudly to stderr / blocker channel** and stop. Don't guess.

A scheduled run that opens a clarification question is a bug — it just sits there waiting.

### 2. Use defaults

| Decision | Default in headless mode |
|---|---|
| Lookbook format | `html-cart` if MPP-reachable, else `html` (read-only); **never** `ppt` (no review surface) |
| Number of looks | 2–3 (skip the optional 4th–5th) |
| Output tier | One-shot/event lookbooks: Premium if `OPENAI_API_KEY` + ≥2 reference photos; otherwise Editorial, then Minimum. Recurring weekly newsletters: Editorial unless `weekly_lookbook_tier: premium` |
| Hosting transport | `profile.md → preferred_lookbook_host`, else the highest-ranked transport from the `references/hosting-options.md` probe |
| Hosting confirmation | **Skip** when `preferred_lookbook_host_auto: true`; otherwise abort the run with `BLOCKER: hosting needs interactive confirm` |
| Voting | On for Cloudflare Pages deploys. Resolve `lookbook_votes_kv_id` from `profile.md` or `$LOOKBOOK_VOTES_KV_ID`; missing id is a blocker unless the run was explicitly requested as read-only / `--no-voting` |
| Coupon / credit | Apply available customer credit (default in workflow #4); no coupon hunting |
| Pickup vs ship | Ship to `profile.md → shipping_address` |
| Out-of-stock pieces | Drop from the lookbook (note the drop in the run summary), don't substitute |

### 3. Premium try-on first for one-shot / event lookbooks

The normal one-shot or event-triggered lookbook default is Premium: gpt-image-2 try-on imagery placed on the customer. The Editorial tier (product imagery + flat-lays, no gpt-image-2 call) is the documented fallback when:

- `OPENAI_API_KEY` is unset, or
- Fewer than 2 `reference_photos` resolve, or
- gpt-image-2 returns a non-success status (rate limit, billing block, content-policy refusal — surface the reason in the run summary).

The minimum-viable-lookbook tier (text + links + stock + rationale) is the deeper fallback when even product imagery isn't reachable (e.g., MCP unreachable). Always produce *something*, but report the fallback reason in the run summary.

### 4. Deploy only if explicitly pre-authorized

Hosting an artifact publicly is a one-way action and the existing skill rule is "always confirm before publishing." Headless mode preserves the safety by requiring **explicit pre-authorization**:

- `profile.md → preferred_lookbook_host_auto: true` is the **only** way the agent skips the per-publish confirm.
- This flag should only be set after the customer has manually deployed at least once on the chosen transport (so they've seen the URL pattern + retention model).
- Even with `_auto: true`, the agent surfaces *what was deployed and where* in the run summary — silent success is allowed; silent failure is not.

If `_auto: true` is not set, headless mode produces the lookbook locally (under `~/.buck-mason-stylist/runs/<lookbook_id>/`) and emits a one-line run summary saying "ready to deploy — set `preferred_lookbook_host_auto: true` or run interactively to publish."

### 5. Silence unless there's a result or blocker

Headless mode emits **at most one message** per run, on one of these channels (in priority order — pick the first that's wired):

1. The customer's preferred notification channel (`profile.md → notify_url` if set — ntfy.sh, Slack incoming webhook, email-via-mailgun, etc.). Not yet a populated field; document it in the schema and ignore until set.
2. `~/.buck-mason-stylist/runs/<lookbook_id>/summary.md` — a file the customer reads later.
3. Stdout of the running process — picked up by whatever scheduler invoked the agent (cron, systemd timer, `/loop` log, OpenClaw routine output).

**No mid-run progress chatter.** No "I'm searching the catalog now…", no "Generated look 1, working on look 2…". Just the final summary or blocker.

## The run summary format

One markdown block, ≤ 25 lines, no preamble:

```markdown
# <Lookbook title> — <date>

✅ Deployed: <URL>
Tier: <Premium | Editorial | Minimum>
Looks: <N>
Pieces: <total count> · in stock <%>
Subtotal at pick: $<total>

Notes
- <one line per noteworthy thing — pieces dropped, low-stock warnings, fallback tier reasons>

Verify: opengraph.xyz/url/<encoded-url>
```

Failure form:

```markdown
# <Lookbook title> — <date>

❌ BLOCKER: <one-line reason>
Tier attempted: <Premium | Editorial | Minimum>
Stage failed: <fetch | tryon | build | validate-local | deploy | validate-deployed>

Detail
<short paragraph with the underlying error and what would unblock>
```

## Wiring it together — the canonical headless invocation

```bash
# Run as a /loop or cron job. The script bundle (scripts/) is deterministic
# and headless-safe by construction. Always invoke via the explicit
# interpreter — ClawHub installs may strip the executable bit on unpack.
python3 scripts/build-html-lookbook.py \
  --config "$RUN_DIR/config.json" \
  --picks  "$RUN_DIR/picks.json" \
  --look-images "$RUN_DIR/looks/" \
  --out "$RUN_DIR/deploy/"

bash    scripts/deploy-lookbook.sh "$RUN_DIR/deploy/" "$PROJECT_NAME" \
  --auto --no-overwrite --kv-id "$LOOKBOOK_VOTES_KV_ID"

python3 scripts/validate-lookbook.py --dir "$RUN_DIR/deploy/" \
  --url "https://${PROJECT_NAME}.pages.dev/"
```

The single canonical command that composes all of the above is **`scripts/run-headless-lookbook.py`** (orchestrator: discover → curate → build → deploy → validate → summary). For one-shot headless runs prefer that — see § "The end-to-end orchestrator" below. The orchestrator passes `profile.md → lookbook_votes_kv_id` through to the deploy wrapper; without that value or `$LOOKBOOK_VOTES_KV_ID`, the deploy blocks because voting is the default.

If any step's exit code is non-zero, the run summary file is the failure form. If all three succeed, the summary file is the success form and (if a `notify_url` is wired) the agent posts the summary to that channel.

## Recurring weekly newsletter

The canonical recurring use of headless mode: a once-weekly lookbook surfacing what's new on buckmason.com plus anything the customer hasn't been pitched yet. Cadence configurable; weekly is the default.

### What it shows

Per run, the agent assembles 4–6 pieces grouped into 1–2 looks, drawn from this priority order:

1. **`/seasonal?days=14`** — products set live on buckmason.com in the last two weeks. Primary source.
2. **General catalog** filtered to items **not present in `~/.buck-mason-stylist/wishlist.jsonl`** (by `sku`). Backfill when (1) is thin.
3. **Style-ethos / color-prefs filter** applied across both sources — keep only items that match the customer's `style_ethos` and `favorites` colors. Drop anything in their `avoid` list.

The output is **always Editorial tier** by default — no gpt-image-2 spend on a recurring artifact (~$0.40/week × 52 = $21/year, not justifiable for a newsletter that may or may not be opened). The customer can opt into Premium tier for the weekly via `profile.md → weekly_lookbook_tier: premium` if they want try-on imagery every week.

### URL stability is non-negotiable

Each weekly run gets **its own permanent Cloudflare Pages project** so the customer can refer back to any past edition forever. See `references/hosting-options.md` § "URL stability — one Pages project per permanent lookbook" for the full rule and the `--no-overwrite` flag. Project naming: `<lookbook_project_prefix>-weekly-<YYYY-WW>` (ISO week number).

### Dedup against the wishlist

`~/.buck-mason-stylist/wishlist.jsonl` is the long-term memory. Every piece proposed in any prior lookbook (whether the customer bought it or not) gets a row at proposal time:

```jsonl
{"sku":"BM13211.679NATL","name":"Natural Draped Linen Deuce Coupe Camp Shirt","size":"L","lookbook_id":"2026-05-09-mellow-la","lookbook_url":"https://buckmason-nick-2026-05-09-mellow-la.pages.dev/","proposed_at":"2026-05-09T14:32:00Z"}
```

Fields are added on top of the existing wishlist contract (item + size + qty + order_id + purchased_at):

- `proposed_at` — when the piece first appeared in any lookbook (UTC ISO timestamp). The dedup key for "have I shown this to the customer before?"
- `lookbook_url` — permanent URL of the lookbook that introduced the piece. Lets the agent answer "where did you suggest the camp shirt?" without re-fetching.
- `purchased_at` / `order_id` — set later (nullable until the customer actually buys via MPP checkout).

The newsletter dedupes on `sku` — if a piece was proposed last month and the customer didn't buy it, don't re-propose unless **both**: (a) it's been ≥ 8 weeks since `proposed_at`, AND (b) the agent has explicit reason to re-surface (price drop, restocked after sellout, customer asked for it). Default behavior: skip.

### Canonical invocation

```bash
# Discover candidates (deterministic — no LLM, no network beyond MCP).
python3 scripts/discover-weekly-candidates.py \
  --gender m \
  --since-days 14 \
  --wishlist ~/.buck-mason-stylist/wishlist.jsonl \
  > candidates.json

# Agent step (taste): read candidates.json, pick 4–6 items, group into 1–2
# looks, write picks.json + config.json with a unique lookbook_id.
# (No script for this — the agent's call.)

# Build, deploy with --no-overwrite for URL stability, validate.
RUN_DIR=~/.buck-mason-stylist/runs/weekly-2026-19
python3 scripts/build-html-lookbook.py --no-tryon \
  --config "$RUN_DIR/config.json" --picks "$RUN_DIR/picks.json" \
  --out    "$RUN_DIR/deploy/"

PROJECT="${LOOKBOOK_PROJECT_PREFIX}-weekly-2026-19"
bash scripts/deploy-lookbook.sh "$RUN_DIR/deploy/" "$PROJECT" \
  --auto --no-overwrite --kv-id "$LOOKBOOK_VOTES_KV_ID"

# Append every proposed piece to the wishlist with proposed_at + lookbook_url.
# (Either inline or via a future scripts/log-proposal.py — keep agent-side.)
```

## The end-to-end orchestrator

Use `scripts/run-headless-lookbook.py` for a single canonical headless invocation. It composes the deterministic chain (score → discover → curate → build → deploy → validate → summary), selects Premium for one-shot/event lookbooks when `OPENAI_API_KEY` and at least two reference photos are available, keeps recurring weekly runs Editorial unless opted into Premium, and writes a run-summary file at `~/.buck-mason-stylist/runs/<lookbook_id>/summary.md`.

```bash
# Weekly newsletter
python3 scripts/run-headless-lookbook.py --weekly --profile ~/agent-workspace/profile.md

# Event-driven (auto-scored; skips on hard-veto)
python3 scripts/run-headless-lookbook.py --event /path/to/event.json --profile ~/agent-workspace/profile.md
```

The orchestrator never deploys without `preferred_lookbook_host_auto: true` in the profile; when deploy authorization is missing it produces the lookbook locally (under `~/.buck-mason-stylist/runs/<lookbook_id>/deploy/`) and writes a summary saying "ready to deploy — set `_auto: true` or run interactively to publish." That preserves the deploy-authorization rule even when an event scores 7–10 and would otherwise auto-generate AND auto-deploy.

The run summary (per § "The run summary format" above) reports the URL, the count of new products surfaced, and any reason items got dropped (out of stock, ethos mismatch, already proposed within 8 weeks).

### Cadence + opt-out

- Default cadence: weekly, Monday morning local time. Configurable via `profile.md → weekly_lookbook_cadence: "weekly" | "biweekly" | "monthly" | "off"`.
- `off` disables the recurring lookbook entirely; the agent still runs event-driven (calendar) lookbooks per `references/event-suitability.md`.
- The first weekly run after install is the "welcome" lookbook — it can use the entire `/recommend` capsule (not just recently-live), since the customer has no wishlist history yet.

## Per-run dev logging

Every orchestrator run writes two timing artifacts to its run directory:

```
~/.buck-mason-stylist/runs/<lookbook_id>/
├── _timings.jsonl    one JSON line per phase, machine-readable
└── _run.log          human-readable chronological trace + slowest-phases summary
```

Plus a one-line stderr summary at end-of-run:

```
[timings] total 15.9s · slowest: discover_candidates 10.2s | build 5.7s | validate_local 0.0s
```

### What gets timed

| Phase | What's measured | Typical range |
|---|---|---|
| `parse_profile` | YAML/markdown parse of `profile.md` | <0.1s |
| `score_event` (event mode only) | `scripts/score-calendar-event.py` regex pass | <0.1s |
| `discover_candidates` | `scripts/discover-weekly-candidates.py` — MCP `/products?recently_live` + backfill + per-candidate `/products/<id>` detail calls | 5–30s (depends on candidate count and MCP latency) |
| `build` | `scripts/build-html-lookbook.py` — thumbnail downloads (curl per piece) + og.jpg generation + HTML render | 3–10s |
| `verify_face` (Premium tier only, per look) | `scripts/verify-face.py` — GPT-4o-vision call | 5–15s per look |
| `validate_local` | `scripts/validate-lookbook.py --dir` | <0.1s |
| `deploy` (when `_auto: true`) | `scripts/deploy-lookbook.sh` — wrangler probe + (idempotent) project create + upload + post-deploy validate | 10–30s |
| `validate_deployed` | `scripts/validate-lookbook.py --url` (D1–D6 checks) | 2–5s |
| `wishlist_append` | JSONL append to `~/.buck-mason-stylist/wishlist.jsonl` | <0.1s |

### When to look at the log

- **Run took longer than expected** — check `_run.log`. Top-3 slowest phases are at the bottom; the chronological list is in the middle.
- **Phase consistently slow** — grep across many runs:
  ```bash
  jq -s 'map(select(.phase == "discover_candidates")) | sort_by(.duration_s) | reverse | .[0:5]' \
    ~/.buck-mason-stylist/runs/*/_timings.jsonl
  ```
- **Phase failed** — entries with `"ok": false` carry an `error` field with the exception class + first 200 chars. Same data shows in `_run.log` with a `✗` mark.

### What's NOT in the orchestrator's timing

- **`gpt-image-2` generation for Premium-tier runs.** That call lives outside the deterministic chain — the agent makes it between the first orchestrator pass (which exits with `READY_FOR_PREMIUM_IMAGE_STEP`) and the second pass (which resumes via `--resume-build`). If a "full Premium run" feels like 5+ minutes, the time is likely there: gpt-image-2 high-quality 1024×1536 takes ~30–60s per look × 2 looks = 1–2 minutes, plus the `verify_face` overhead (10–30s for two looks). The orchestrator's `_run.log` only spans the orchestrator's portion of work.
- **Wrangler interactive prompts.** First-time `wrangler login` for a fresh machine isn't timed (it's outside the orchestrator).
- **Per-candidate MCP `/products/<id>` calls** inside `discover_candidates` — currently rolled up into the parent phase. If `discover_candidates` is the bottleneck, the next instrumentation level is to add timings inside `discover-weekly-candidates.py` itself.

## What headless mode does NOT do

- **Doesn't run MPP checkout autonomously.** Even with `_auto: true`, MPP requires the customer's push-approval in their Link app — that's the consent step. A scheduled run produces a lookbook + handoff prose, but checkout always waits for the customer.
- **Doesn't email customers from the agent's address.** Sending email or chat messages on the customer's behalf is a separate authorization (`notify_url` wires the final summary; it doesn't email "your stylist suggests…" to anyone).
- **Doesn't bootstrap accounts.** If `wrangler` / `link-cli` / OPENAI key is missing, the run produces a blocker summary asking the customer to set it up next time they're interactive — the agent never tries to sign up on their behalf.

## Composition with other docs

- `references/hosting-options.md` — the deploy-authorization rules originate there (`preferred_lookbook_host_auto` field). Headless mode is the surface that consumes it.
- `references/acceptance-checklist.md` — every headless run gates on the validator. Failed gate → blocker summary.
- `templates/profile.schema.json` — defines the fields headless mode reads (`preferred_lookbook_host*`, `link_payment_method`, `notify_url` once wired).
