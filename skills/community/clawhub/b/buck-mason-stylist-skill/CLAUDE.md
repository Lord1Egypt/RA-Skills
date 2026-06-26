# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. The Codex-facing companion is `AGENTS.md`; keep durable repo rules aligned between the two, while leaving Claude-specific tool and sandbox notes here.

## What this repo is

A **Claude / Codex / agent skill** — markdown + JSON, no application code. The agent that loads `SKILL.md` becomes a Buck Mason personal shopper that talks to the public `pima.io/mcp/buckmason/*` endpoints. There is no server, no compiled artifact, no test suite, no CI. Editing this repo means editing prompt content and reference docs that an LLM consumes at runtime.

## Build / test / lint

- There is nothing to compile. Changes ship as soon as `clawhub publish` completes (see `PUBLISHING.md`).
- **`python -m pytest tests/`** runs the unit + smoke tests for the script bundle. Coverage: `parse_profile` (regex/format quirks), `score-calendar-event` (rubric worked examples), `validate-lookbook` (each L1–L10 gate with fixture deploy dirs), `verify-face` (threshold logic + JSON parsing, OpenAI mocked via local HTTP server), `build-html-lookbook` (smoke + marker enforcement). 45 tests as of v0.6.0; `pip install Pillow pytest` first.
- **CI runs on every push + PR** via `.github/workflows/tests.yml` — pytest matrix on Python 3.11 + 3.12, plus a `scripts-help` job that renders `--help` on every bundled script (catches argparse breakage and bash syntax issues independent of unit tests).
- "Live testing" means loading the skill into an agent (Claude Code, Codex, ChatGPT) and walking the relevant workflow end-to-end against `pima.io/mcp/buckmason/*`. Tests cover the deterministic plumbing; only live-walk the agent flows.
- Validate before publish: `python -c 'import json; json.load(open("clawhub.json"))'` and visually scan the YAML frontmatter at the top of `SKILL.md` for parser-breaking edits. The CI `validate clawhub.json + SKILL.md frontmatter` step also enforces the lockstep version invariant.
- Node ≥ 20.12 is required to run `clawhub` itself (see `.tool-versions` → `nodejs 20.20.2`). Nothing in the repo is Node code.

## Versioning is lockstep — bump in three places

Every substantive change to prompt content, references, or the MCP contract bumps the version in **all three** of these, in the same commit:

1. `clawhub.json#version`
2. `SKILL.md` frontmatter `version:`
3. The git commit message — convention from `git log` is `vX.Y.Z: <one-line summary>`

If you skip the bump, ClawHub installs will silently serve the prior version. Recent commits (`928d0d7`, `092c781`, `ac4a88f`) show the pattern.

## Architecture — the big picture

### Codex / OpenAI surfaces

Codex reads `AGENTS.md` for repo-editing guidance. The root `SKILL.md` remains the runtime skill entry point for every agent, and `agents/openai.yaml` supplies OpenAI/Codex UI metadata plus the default `$buck-mason-stylist` invocation prompt. When the skill name, description, user-facing prompt, or branding changes, update `agents/openai.yaml` in the same change.

### `SKILL.md` is the entry point

Everything a loaded agent reads first lives in `SKILL.md` at the root. Its YAML frontmatter declares the runtime contract (env vars, required binaries, optional CLIs) that ClawHub surfaces to operators at install time. The body declares **five workflows** the skill activates on:

1. **Stock check** — does Buck Mason have item X in my size, online + nearby store
2. **Wardrobe gap analysis** — capsule recommendations diffed against `wardrobe.md`
3. **AI try-on lookbook** — default gpt-image-2 virtual try-on in hosted `html` / `html-cart`, with Cloudflare voting enabled on deploy
4. **MPP checkout** — fully agent-driven checkout via `link-cli`, see below
5. **Order tracking + returns** — runs against the same `/api/*` that powers orders.buckmason.com

When changing a workflow, update both the prose in `SKILL.md` and the corresponding deeper reference in `references/`.

### Two endpoint families

The skill speaks to two distinct API surfaces, used in different workflows. Don't mix them up:

| Surface | Host | Auth | Used for | Reference |
|---|---|---|---|---|
| `/mcp/buckmason/*` | `pima.io` | none (public) | Catalog, stock, locations, recommend, MPP checkout | `references/mcp-api.md` |
| `/api/*` | `www.buckmason.com` / `orders.buckmason.com` | JWT or `?order_code=<code>` | Account, order history, tracking, returns | `docs/advanced/pima-api.md` |

**Purchasing happens through the MCP only.** The agent never POSTs to an `/api/*` purchase path.

### Checkout path — MPP agent-driven

| Path | Endpoint | Consent model | Surface needed |
|---|---|---|---|
| MPP fully-agent-driven | `POST /mcp/buckmason/checkout` (HTTP 402 + Stripe SPT) | Customer push-approves the spend in their Link app on their phone via `@stripe/link-cli` | None (works headless) |

Workflow #4 in `SKILL.md` covers the prose; `references/mpp.md` covers the two-phase request lifecycle, the `acknowledged_total_cents` echo guardrail, idempotency, coupon/credit envelope, and the `X-Agent-Identity` / `X-Agent-Model` headers. **Read `references/mpp.md` before editing anything in workflow #4 step 3.**

### Three opt-in capability gates

The default install has all high-risk capabilities turned **off** by construction. Each gate requires both a missing dependency to be installed AND an explicit per-conversation user opt-in:

| Capability | Gate | Reference |
|---|---|---|
| AI try-on lookbook (sends photos to OpenAI) | `OPENAI_API_KEY` + verified org for `gpt-image-2` | `references/image-generation.md` |
| Lookbook voting deploy (public Pages URL + KV-backed comments) | `wrangler` auth + Cloudflare KV namespace id (`lookbook_votes_kv_id` or `LOOKBOOK_VOTES_KV_ID`) + publish confirmation / headless auto-publish opt-in | `references/voting.md` |
| MPP fully-agent-driven checkout | `npm i -g @stripe/link-cli` (operator) + customer has a Stripe Link account with a linked payment method (`profile.md → link_payment_method: confirmed`) + per-purchase user opt-in | `references/mpp.md` |
| Email magic-link account linking | Authorized email MCP + retrieval-method confirmation | `SKILL.md` workflow #5c |

Preserve this property when editing. The opt-in matrix is documented in `SECURITY.md` and is load-bearing for ClawScan / VirusTotal Code Insight reviews. If you add a new capability that touches money, photos, mail, or shipping address, add a row to the opt-in matrix.

### ClawHub manifest schema — load-bearing for the listing UI

`clawhub.json` is read by **two** consumers with different schemas:

1. **The listing UI** at `clawhub.ai/<owner>/<slug>` reads `env`, `requires.optional_clis`, `requires.binaries`, `requires.python` and renders them in the *Runtime requirements* panel. It expects each one to be a **flat array of strings** — passing objects renders as `[object Object]` (caught and reverted in v0.1.7).
2. **OpenClaw / ClawScan** want richer per-item metadata (purpose, format, where to obtain, verification notes).

Reconcile by keeping both: the canonical names stay flat, structured metadata lives in *sibling maps keyed by name*:

```jsonc
{
  "env": ["OPENAI_API_KEY"],                          // listing UI reads this
  "envDetails": {                                     // scanners + reviewers read this
    "OPENAI_API_KEY": { "purpose": "...", "obtain_url": "...", ... }
  },
  "requires": {
    "optional_clis": ["@stripe/link-cli"]             // flat
  },
  "optionalCliDetails": {                             // structured
    "@stripe/link-cli": { "install": "...", "publisher": "...", ... }
  }
}
```

Mirror the same shape in `SKILL.md` frontmatter under `metadata.openclaw.requires.*` (flat) and `metadata.openclaw.env_details` / `metadata.openclaw.optional_cli_details` (structured). When adding a new env var or optional CLI, **always add to the flat list AND the details map in the same edit**, in both files.

The verbose human-readable copy (gpt-image-2 verification, npm verified-publisher pinning, etc.) lives in prose in `SKILL.md § Environment`, `README.md § Required setup`, and `SECURITY.md` — not in the manifest.

### `references/` is loaded on demand

The agent doesn't load every reference file at session start — `SKILL.md` points at them ("Read `references/mpp.md` before invoking…") and the agent reads on demand. This keeps the entry-point context small. When adding a new reference doc:

1. Put it in `references/` (or `docs/advanced/` for non-stylist surfaces like the `/api/*` reference).
2. Add a one-line entry in `SKILL.md` § "Files in this skill".
3. Add the same entry in `README.md` § Files.
4. Reference it from the relevant workflow with explicit "read this before X" prose.

### `scripts/` is the deterministic spine

For work that's fragile to reconstruct from prose (build, deploy, validate, score), the skill ships actual scripts under `scripts/`. The agent invokes them directly rather than re-deriving the logic each session. Current set:

- `scripts/build-html-lookbook.py` — config + picks JSON → deploy directory (idempotent, no AI calls; gpt-image-2 outputs are supplied via `--look-images`).
- `scripts/deploy-lookbook.sh` — Cloudflare Pages wrapper (probe → idempotent project create → deploy → post-deploy validate). Use `--auto` only when `profile.md → preferred_lookbook_host_auto: true`.
- `scripts/validate-lookbook.py` — runs every gate in `references/acceptance-checklist.md` against a local dir and/or a deployed URL. Exit code: `0` pass, `1` local fail, `2` deployed fail.
- `scripts/score-calendar-event.py` — implements `references/event-suitability.md`. JSON in, `{score, breakdown, action}` out, side-effect-free.

When adding a new script: ship deterministic logic only (no LLM calls inside the script — those happen *around* the scripts in the agent's flow), add a one-line entry in SKILL.md § "Files in this skill" + README.md § Files, and gate it with the matching reference doc that explains the *why*.

### Keeping `references/mpp.md` in sync with Pima

`references/mpp.md` is essentially API documentation for `pima.io/mcp/buckmason/checkout`. Pima moves under it; if the doc drifts, every agent loaded from this skill misbehaves on real money. Verify periodically (and any time you touch the workflow #4 / MPP prose):

- **Production host is always `pima.io`.** There is no `staging.pima.io` mentioned anywhere in the skill — every example URL in references/mpp.md and SKILL.md points at production. The manifest's `environment` field (`GET /mcp/buckmason/manifest` → JSON body, `ENV['PIMA_ENVIRONMENT'] || 'production'`) confirms.
- **Confirmed-true MPP server behavior** (verified against `pima-master/app/services/mcp/checkout.rb`; re-verify against the live manifest before assuming):
  - The `/checkout` Phase-1 preview total **includes sales tax** via TaxJar — estimated against `fulfillment_address` for ship items and the pickup_location for pickup items. Phase 2 then re-runs `Order#update_taxes!` against the persisted Order, so the customer-acked `acknowledged_total_cents` must match the with-tax total or Phase 2 returns `total_mismatch` and cancels.
  - **Two-phase coupon model.** Phase 1 always issues the 402 challenge regardless of coupon validity — `coupon_status.error` surfaces `coupon_not_found` / `not_applicable` / etc. at preview time, but the challenge is still produced (so the customer can see the un-discounted total and decide). Phase 2 preflight is **strict for any non-blank coupon code**: it builds a real pending Order, runs `Coupon#applicable?` (POS's 25+ rules), and on any failure raises `PreflightFailed → 422 coupon_not_applicable` with `error.message` carrying the reason verbatim. No Stripe call. Surface the reason directly to the customer.
  - **Pickup is supported at top-level + per-item** on `/checkout` — `pickup_location_slug` / `pickup_location_id` at checkout level applies as default; per-item `pickup_location_{slug,id,name}` overrides for mixed ship+pickup requests. Pickup-disabled locations error as `pickup_disabled`.
  - **Customer credits actually debit** via `CustomerCreditTransaction#complete!` (DB-locked, capped at live balance) inside `OrderMaterializer.finalize!`. The Phase-1 `CreditResolver` balance check is informational only. Drained codes surface `credit_no_balance` in `credit_status[]`.
  - **Checkout line items use resolved SKUs.** `/checkout` accepts `{ sku: <sku-name>, quantity }` directly and **does not read `size`**. The `html-cart` handoff schema matches `/checkout`; resolve product name + size to SKU before preflight.
  - Live MPP works end-to-end against Buck Mason production (Stripe SPT preview is allowlisted; merchant `network_id` is exposed in the live manifest at `/mcp/buckmason/manifest` — don't hard-code it in tracked docs). Real charges have been confirmed.
- **Quick smoke check** — `curl -sS https://pima.io/mcp/buckmason/manifest | jq .environment` should return `"production"`. The MPP block in the manifest body (`mpp.spec`, `mpp.base_url`, `mpp.agent_tools`, `mpp.dry_run_param`) lists the agent tooling and dry-run flag — make sure `references/mpp.md` still matches.

When any of these facts change upstream, update references/mpp.md in the same commit + bump the version in all three places per the lockstep rule above.

### `templates/` get copied into the user's workspace

`profile.example.md`, `wardrobe.example.md`, `events.example.md` are not loaded by the skill — they're handed to the customer to copy into *their* workspace and fill in. Edits to these change the data shape every loaded skill instance reads from.

## Editing conventions

- **Buck-Mason–specific by design.** Do not genericize away store names (Abbot Kinney, Century City, Bloomingdale's), product taxonomy (Como Cashmere, Capitola Linen, OG-107 Fatigue, Hollywood Pleated), tone, or hard-coded `pima.io` host. `PUBLISHING.md` § "What stays Buck-Mason-specific" enumerates this.
- **Cents → dollars on display.** Pima returns prices in cents (`9720`); the agent always shows `$97.20`. Don't surface raw cents to the customer.
- **Permissions are declared, not inferred.** Every external host the skill speaks to must be listed in `clawhub.json#permissions.network` with a `purpose`. Adding a new host means updating the manifest *and* `SECURITY.md`'s data-flow table.
  - **Opt-in egress** (only reached when the operator wires a dep — `OPENAI_API_KEY`, `wrangler`, `@stripe/link-cli`) gets `opt_in: true` + `trigger` + `via` fields on the manifest entry, and a row in SECURITY.md's "What an operator opts into" matrix.
  - **Operator-driven alternatives** that the skill *documents* (e.g. the menu of HTML lookbook hosts in `references/hosting-options.md`: Surge, Netlify, Vercel, Gist, S3, 0x0.st) but does NOT invoke go in `permissions.network_alternatives_documented_only`, not `permissions.network`. Listing them under `network` would falsely claim egress the skill itself never initiates; omitting them entirely fails ClawScan's "Cascading Failures" check. The split closes both gaps.
- **The purchase path is MPP checkout**. Only proceed when the customer explicitly opts into agent-driven payment in the same turn, with the total restated in plain English and Link approval handled through `link-cli`.
- **Never persist a Stripe SPT, full PAN, or CVV to disk.** SPTs are one-time-use; if a retry is needed, mint a fresh one. This is a hard rule from `SECURITY.md` § Threat model.

## Publishing

`clawhub skill publish .` from the repo root, after the lockstep version bump above. Full flow in `PUBLISHING.md`. Live listing: <https://clawhub.ai/nickmerwin/buck-mason-stylist-skill>. Visibility is controlled by `clawhub.json#visibility` (currently `public`).

### CLI quirks worth remembering

- **`clawhub skill publish` requires `--version <semver>` explicitly** (e.g., `--version 0.1.7`). Without it, it errors `--version must be valid semver` even though the version is in `clawhub.json`. Pass it on the command line every time, matching the manifest.
- **There is no `--visibility` flag on publish.** Visibility is read from `clawhub.json#visibility`. Earlier docs that suggested `--visibility public` are wrong; remove on sight.
- **Non-browser auth**: `clawhub login --token <token> --no-browser` is the headless path. `clawhub auth status` confirms `authenticated: true` + the token's user. **`whoami` reflects the token owner — that's also who owns any skill published with it.**
- **Orgs are not first-class for publishing.** `clawhub.ai` orgs exist for membership/UX, but skills are per-user (npm-style flat namespaces, not GitHub-style). `clawhub transfer request <slug> <handle>` only accepts user handles — passing an org handle returns `toUserHandle required`. To get a skill under an org slug, that handle has to also be a real user account; otherwise leave it under the publisher's user namespace and link to `pima-io` via the `homepage`/`repository` fields.
- **Node ≥ 20.12 is required**: clawhub CLI uses `import … with { type: 'json' }`, which crashes on 20.9 with `SyntaxError: Unexpected token 'with'`. `.tool-versions` pins `nodejs 20.20.2` for this reason — don't downgrade.

### Sandbox / permission patterns observed in this skill's own dev loop

When making changes via Claude Code itself, expect these to be blocked by default and need an explicit `! <cmd>` user-runs-it shortcut, or per-tool permission rules:

- `git push origin main` — blocked even with prior in-conversation authorization. Auth is per-push, not standing.
- `clawhub skill publish .` (the first time, especially with `--visibility public`) — flagged as "Create Public Surface."
- Reading `.env` files outside the working tree — blocked unless using the `Read` tool (not Bash `cat`/`grep`).
- Writing `.claude/settings.local.json` to grant the agent its own future permissions — flagged as Self-Modification.

### Scanner-tripwire patterns to avoid

Two patterns in this skill's history have tripped automated scanners that aren't actual security issues — call them out so we don't reintroduce them:

- **Inline `\x..` escape sequences in Python sources** trip ClawHub's static-analysis scanner as `suspicious.obfuscated_code` even when they're plain test fixtures (e.g. a minimal JPEG header). Move multi-byte literals to a real file under `tests/fixtures/` and `shutil.copy` them in. Done in v0.6.5 for the JPEG SOI/JFIF/EOI fixture used by `test_validate_lookbook.py` and `test_verify_face.py`.
- **Unicode zero-width / format / bidi codepoints** (U+200B, U+202A–U+202E, U+2060–U+2064, U+FEFF, etc.) anywhere in markdown/JSON/YAML trip ClawScan's `unicode-control-chars` prompt-injection detector and force the verdict to "Review" regardless of the actual content. Don't paste content that may carry zero-widths from Slack / Notion / Google Docs into reference docs without stripping. A one-liner check before publish: `python3 -c "import sys, pathlib; cps={*range(0x200B,0x2010),*range(0x202A,0x202F),*range(0x2060,0x2065),0xFEFF,0x2028,0x2029}; [print(p, ln, repr(c)) for p in pathlib.Path('.').rglob('*') if p.is_file() and p.suffix in {'.md','.json','.yaml','.yml','.txt','.py'} for ln,line in enumerate(p.read_text(errors='ignore').splitlines(),1) for c in line if ord(c) in cps]"`.

### Security review floor

VirusTotal Code Insight will land any skill with **payments + photo upload + PII files** at "Review / suspicious" by default — that's the floor for the capability surface, not a defect. `SECURITY.md` softens the verdict by making the threat model explicit (data-flow table, opt-in matrix, "what the skill DOES NOT do") but doesn't clear it. ClawScan likewise flags MPP + magic-link as Notes/Concerns even when guardrails are correct. The right response is to keep guardrails honest and document them, not to chase a "clean" rating that isn't achievable for this capability set.
