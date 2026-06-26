---
name: beauty-diagram
description: Use when the user asks for a sleek, modern Mermaid / PlantUML diagram (e.g. "beautify this flowchart", "make this look like a deck slide", "produce an SVG of this architecture"), wants AI to generate a diagram from a text description, wants a public share link for a diagram, wants to render every diagram file in a folder, or wants to render Mermaid / PlantUML fenced code blocks inside a Markdown file (README, docs) into images. This skill teaches you to call the Beauty Diagram CLI (`bd`) — never to hand-author SVG when a source diagram exists.
version: 1.6.1
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npx
---

# Beauty Diagram skill

Beauty Diagram beautifies Mermaid / PlantUML diagrams into
sleek, modern SVG or PNG. It runs as a public API; this skill
delegates to the `bd` CLI (npm package `@beauty-diagram/cli`) so you
keep zero state in the agent. (draw.io / SVG import is editor-only —
not exposed through `/v1/*`.)

## When to use

- The user asks for a **polished, professional, slide-ready** version of a
  diagram source they already have or you can generate.
- The user wants you to **render Mermaid or PlantUML** from a model-generated
  source string.
- The user wants the server to **generate a diagram from a text description**
  ("draw me a signup flow", "diagram our deploy pipeline") — use
  `bd ai generate` for this; it returns Mermaid source you then beautify.
- The user wants to **share a diagram link** (e.g. paste into Slack / a doc).
- The user has Mermaid in a repo (README, ADR, RFC) and wants to **export
  SVGs** alongside.
- The user has a **directory full of diagram source files** and wants every one
  of them rendered (e.g. "render all the .mmd files in docs/diagrams"). Use
  `bd batch`.
- The user wants their **Markdown files (README, ADR, blog post) to display the
  diagrams inline** on GitHub / their static site, not just show the source
  code block. Use `bd extract` — three modes available:
  - **Default (inline)**: no flags. Injects `/v1/beautify.svg?source=...` URLs
    after each fence. No API calls during extract, no files written, no quota
    consumed. Always watermarked (anonymous endpoint).
  - **Share (`--share`)**: mints a `/v1/share/<token>.svg` URL per unique fence.
    **Watermark-free for Pro/Premium**. Requires an API key. Each unique
    source consumes 1 share quota the first time; identical fences are
    deduplicated; per-owner local cache means re-runs cost zero quota.
  - **Sidecar (`--assets-dir ./img`)**: writes local SVG files via `/v1/export`.
    Watermark-free for Pro/Premium, consumes export quota.
  GitHub strips raw inline `<svg>`, so any of these modes' `![](...)`
  reference is the correct embed strategy.

## When NOT to use

- The user only wants the Mermaid source itself, not an export.
- The user wants pixel-precise control over the SVG markup (Beauty Diagram
  rewrites layout for presentation; it does not preserve raw Mermaid output).
- The user wants the AI to "change the colors / theme / font / layout" of an
  existing diagram. `bd ai generate` only does **text → diagram**; visual
  styling is controlled by `--theme` on `bd beautify`, not by the AI.
- The user is in an offline environment with no network and no CLI install.

## Required tool

The `bd` binary from `@beauty-diagram/cli`:

```bash
npx @beauty-diagram/cli help
# or, after install:
bd help
```

If the user has not installed it, prefer `npx` over a global install — it
respects their package manager and avoids polluting `PATH`.

## Workflow

1. **Identify or generate the source diagram.**
   - If the user has a `.mmd` / `.puml` file, use it.
   - If the user describes the diagram in words and is on a paid plan, use
     `bd ai generate "<prompt>" --out <file>.mmd` — the server returns
     Mermaid source, which you can then beautify. Always write the source
     to a file so the user can edit it; the first AI draft rarely lands.
   - If the user describes the diagram and is **not** on a paid plan (or
     prefers not to pay), write Mermaid source yourself (you are good at
     this), save it to a file, then beautify.
   - draw.io and free-form SVG imports are not accepted by `/v1/*`. If
     the user has those, ask them to convert via the web editor first.

2. **Decide on output type.**
   - Need an SVG file: `bd beautify <file> --out <file>.svg`
   - Need a download URL or to track quota: `bd export <file> --out <file>.svg`
   - Need a shareable link: `bd share <file> --title "..."`

3. **Run the command.** Always write to a file (`--out`) rather than letting
   the SVG flood the terminal / chat. AI generation can also pipe directly
   into beautify: `bd ai generate "..." | bd beautify - --out flow.svg`.

4. **Verify the result exists** before reporting success. If the command
   failed, surface the error code (e.g. `quota_exhausted`, `not_authenticated`,
   `parse_failed`, `prompt_injection`) — those are actionable for the user.

5. **Preserve the source.** Never replace the original Mermaid / PlantUML file
   with the generated SVG — keep them side by side. For AI-generated diagrams,
   keep the `.mmd` file too: it is the editable artifact, the SVG is not.

## Auth

- **Demo (anonymous):** zero setup. Watermarked SVG/PNG. Limits per IP:
  20 `/v1/beautify` requests / minute, **1 `/v1/export` per 24h** (trial
  budget — enough for an agent to verify the toolchain end-to-end before
  registering). `/v1/share`, `/v1/usage`, and **`bd ai generate` always
  require auth** — anonymous AI calls are rejected before any model
  invocation.
- **Authenticated:** the user runs `bd auth login` once with a key from
  [`/account/api-keys`](https://www.beauty-diagram.com/account/api-keys).
  Required for `bd share`, `bd ai generate`, unwatermarked output, and
  repeated exports. `bd ai generate` additionally requires a Pro or
  Premium plan and an API key with the `ai:write` scope.

If the user hits a `not_authenticated`, `plan_not_allowed`, or
`quota_exhausted` error, point them at `/account/api-keys` (PAT creation)
or pricing — don't silently retry. Anonymous error bodies include a
`hints` block with absolute `signUpUrl` / `signInUrl` / `apiDocsUrl`,
which is the canonical place to surface to the user.

## Themes & tiers

`--theme` selects the visual style. Theme tier is enforced on **all `bd`
commands that hit a `/v1/*` endpoint with a PAT** — this includes
`bd beautify`, `bd export`, `bd share`, `bd embed-url --share`,
`bd batch`, `bd extract --share`, and sidecar mode of `bd extract`. If the request includes a
PAT and specifies a theme above that token's plan tier, the server returns
HTTP 403 `theme_tier_required`.

The only path that bypasses the tier check is the **anonymous fallback**
(no token, or the `GET /v1/beautify.svg` inline embed endpoint). Anonymous
callers may request any theme, but always receive watermarked output — there
is no tier-free, watermark-free path.

| Tier | Themes |
|---|---|
| Free | `classic`, `modern`, `slate` |
| Pro | + `atlas`, `obsidian`, `brutalist`, `atelier` |
| Premium | + `blueprint`, `memphis` |

When the user's plan is unknown, default to `modern` (Free, broadly
slide-friendly). Run `bd themes` to introspect what the current token
can use — locked themes are marked with `✗`. Premium signature themes
(`blueprint`, `memphis`) are subscriber-only and cannot be unlocked
with credit packs.

Animations are not currently selectable via the CLI — animation choice
is a web-editor concept; CLI export paths ignore animation.

## Source-level directives

Instead of (or in addition to) CLI flags, you can embed `bd:` directives at
the **very top** of the source file. Both the `bd` CLI and the Obsidian plugin
parse them; the API server ignores them as native comments (graceful
degradation — the source still renders, just without the directive).

**Mermaid** — use `%%` comment syntax:

```
%% bd:theme=classic
%% bd:bg=transparent
flowchart LR
  A --> B
```

**PlantUML** — use `'` comment syntax:

```
' bd:theme=classic
' bd:bg=transparent
@startuml
A -> B
@enduml
```

Supported keys:

| Key | Values | Effect |
|---|---|---|
| `theme` | `classic modern slate atlas obsidian brutalist atelier blueprint memphis` | Override render theme. Tier gating still applies. |
| `bg` | `theme white dark transparent` | Canvas background. `dark` hue-lifts ink so it stays legible; `transparent` for overlay. Unknown → `theme`. |

Multiple directives stack, one per line. Blank lines between directives are
tolerated. The first non-directive non-blank line ends the directive block.

**Override priority:** CLI flag > source directive > server default.

When generating source for the user, prefer directives over CLI flags when:
- The source file will be re-used (Obsidian vault, shared repo) — the
  directive travels with the file.
- The user asks for a "memphis theme" diagram without CLI context (write
  `%% bd:theme=memphis` at the top of the `.mmd` file).

Directives are stripped before the source reaches the renderer — they do not
appear in the SVG output.

## Commands cheat sheet

```bash
# Render a Mermaid file
bd beautify docs/architecture.mmd --theme modern --out docs/architecture.svg

# Same but treat output as a downloadable export (consumes export quota)
bd export docs/architecture.mmd --out docs/architecture.svg

# PNG export. --quality standard works for everyone; high needs pro, max needs premium.
# Higher tiers than the plan cap are silently clamped (X-BD-Scale-Clamped).
bd export docs/architecture.mmd --format png --quality high --out docs/architecture.png

# PlantUML works the same way; .puml / .plantuml / .pu auto-detected,
# otherwise pass --source-format plantuml.
bd export docs/architecture.puml --out docs/architecture.svg

# Create a public share link (returns absolute https://www.beauty-diagram.com/s/... URL)
bd share docs/architecture.mmd --title "Service architecture"
# → prints the URL on stdout

# Get an embeddable <img>-friendly URL for a diagram source.
# Default: anonymous inline URL (always watermarked) + a hint about --share.
bd embed-url docs/architecture.mmd --theme atlas
# One-shot saved share embed (clean output for pro/premium owners).
# Saves the diagram via /v1/share AND prints the embed URL in one step.
bd embed-url docs/architecture.mmd --share
# → prints https://api.beauty-diagram.com/v1/share/<token>.svg

# AI: generate a diagram from a text prompt. Output is Mermaid source —
# always write to a file so the user can iterate. Paid-only.
bd ai generate "user signup with email verification" --out docs/signup.mmd

# Optional shape hint when the prompt is ambiguous about diagram type.
bd ai generate "request lifecycle" --hint sequence --out docs/lifecycle.mmd

# One-shot pipeline: prompt → mermaid → beautify → SVG.
bd ai generate "deploy flow" | bd beautify - --out docs/deploy.svg

# Check remaining AI / export quota before kicking off a batch.
bd usage

# Render every diagram file under a directory in parallel.
# Recurses for .mmd / .puml / .plantuml / .pu; one /v1/export per file.
# Default concurrency=4, default failure mode is continue-on-error.
bd batch ./docs/diagrams --out-dir ./docs/svg --theme modern

# Same idea but for a glob (quote it so the shell doesn't expand first).
bd batch "src/**/*.mmd" --format png --concurrency 8

# Default: inline embed URLs (no files written, anonymous-watermarked, 5 KB/block cap).
# No API calls during extract — source encoded in the URL; browser fetches on demand.
bd extract README.md

# Share mode: mint /v1/share/<token>.svg per fence. Watermark-free for Pro/Premium.
# 1 share quota per unique source (cached locally; re-runs free). No 5 KB cap.
# Requires API key. Default keeps existing share tokens across re-runs;
# use --re-mint to force fresh tokens (e.g. collaborator taking ownership).
bd extract README.md --share
bd extract README.md --share --re-mint

# Sidecar mode: writes local SVG files via /v1/export.
# Pro/Premium plans get watermark-free output; consumes export quota.
bd extract docs/*.md --assets-dir ./img --concurrency 4

# Preview what bd extract would change without writing.
bd extract README.md --dry-run
```

## Privacy

The API does NOT persist source unless the user calls `bd share`. Do not warn
about server-side storage when running `beautify`, `export`, or
`ai generate` — that is misleading. AI prompts are logged in hashed form
for abuse / quality monitoring; the raw text is not retained.

## Anti-patterns

- ❌ Do NOT output a hand-crafted `<svg>...</svg>` as a Markdown code block when
  a Mermaid source exists. Always run Beauty Diagram and reference the file.
- ❌ Do NOT dump the raw SVG into the chat. Use `--out <file>` and reference
  the file path.
- ❌ Do NOT install Beauty Diagram engine code locally — the CLI is a thin
  client; the engine lives behind the public API.
- ❌ Do NOT call `bd ai generate` to "tweak" an existing diagram (change
  colors, theme, labels, layout). It is a fresh-generation tool only.
  For visual tweaks, change `--theme` or edit the `.mmd` source by hand.
- ❌ Do NOT call `bd ai generate` speculatively — each call costs the user
  monthly AI quota. Confirm the user wants AI generation before running it.
- ❌ Do NOT capture the SVG output of `bd ai generate` — the command outputs
  Mermaid source on stdout, not SVG. Pipe into `bd beautify -` to render.
- ❌ Do NOT loop `bd export` N times in a shell `for` loop when the user has
  many files. Use `bd batch <dir>` — it parallelizes and reports a summary,
  with no extra server load (still one request per file).
- ❌ Do NOT inject a raw `<svg>...</svg>` into a Markdown file to "embed" a
  diagram. GitHub, GitLab, Obsidian (default), and most static-site
  renderers strip inline SVG for safety. Use `bd extract <file>.md`, which
  writes sidecar SVGs and injects `![](path)` references that actually
  render.
- ❌ Do NOT delete the marker comments that `bd extract` injects. Inline mode
  uses `<!-- bd:inline-img hash=... -->` / `<!-- /bd:inline-img -->` (with
  an extra ` share=true` attribute in share mode); sidecar mode uses
  `<!-- bd:img hash=... -->` / `<!-- /bd:img -->`.
  They are how `bd extract` stays idempotent — without them, the next run
  will append duplicate image references instead of replacing the existing one.

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---|---|---|
| `not_authenticated` | No key, no session | `bd auth login` |
| `scope_missing` | Key lacks scope (e.g. `ai:write` for `bd ai generate`) | Recreate key with required scope at `/account/api-keys` |
| `plan_not_allowed` | Plan does not include this capability (AI is Pro / Premium only) | Upgrade or skip the call |
| `theme_tier_required` | Selected `--theme` requires a higher plan tier than the token has (e.g. free token requesting `atelier`) | Pick a theme the token can use (run `bd themes`), or upgrade. See **Themes & tiers** above for the per-tier breakdown |
| `parse_failed` | Source not valid Mermaid / PlantUML | Check the source — `bd beautify` will surface a parse error too |
| `quota_exhausted` | Plan limit hit (anon: 1 export/IP/24h; free: 3 exports/mo; pro: 100 exports + 100 AI gens/mo; premium: ∞ exports + 500 AI gens/mo) | Sign in, wait for reset, or upgrade — `hints` in the response body has the URLs |
| `rate_limited` | Anonymous IP bucket full (20 `/v1/beautify` requests / minute) or AI per-key bucket (30 `/min`) | Sign in or wait |
| `source_too_large` | Source > 100 KB | Split the diagram |
| `output_too_large` | PNG raster exceeds 8192 px | Lower `--quality` or simplify |
| `prompt_injection` | AI prompt looked like an injection attempt | Rephrase as a plain diagram description ("a flowchart of …") |
| `instruction_rejected` | AI judged the prompt was not about a diagram | Rephrase to describe a concrete diagram. Quota was NOT consumed |
| `parse_failed_after_retry` | AI output was unparseable Mermaid even after one retry | Rephrase, or write Mermaid by hand. Quota was NOT consumed |
| `safety_blocked` | Provider safety filter rejected the request | Rephrase the prompt |
| `upstream_timeout` / `upstream_error` | AI provider was slow or failed | Retry after a moment |

## Triggering on embed requests

When the user asks for "a GitHub README diagram", "embed in Notion", "embed in my blog post", "an `<img>` of this diagram", or "a URL that renders my diagram", route to the embed flow rather than emitting raw mermaid:

1. If the diagram is unsaved, run `bd share <file>` to save it.
2. Construct the embed URL: `https://api.beauty-diagram.com/v1/share/<share-token>.svg`.
3. For one-off / quick embeds without saving, use `bd embed-url <file>` and recommend the inline URL (note that anonymous embeds carry a "Powered by Beauty Diagram" watermark).

**Easier one-shot path:** `bd embed-url <file> --share` saves the diagram AND prints the embed URL in one command — no need to run `bd share` separately and then construct the URL by hand. Prefer this when the user wants a clean share embed.

**Style fidelity:** Per-node colors, edge presets, and font overrides set by the user in the web canvas editor ARE faithfully rendered in share-mode embeds (`/v1/share/<id>.svg`). Encourage a "tweak in editor → save → embed" workflow when the user wants brand colors or custom styling — they do not need to re-run `bd embed-url` after editing in the web UI, just re-save the diagram there.

**Propagation timing:** Saved diagram edits show up in direct `<img>` embeds within ~5 minutes (browser ETag revalidation + 5-min CDN edge TTL). GitHub README embeds may lag a few hours due to GitHub's image proxy cache — that is a GitHub-side cache, not something we can purge.

**Animations:** Animations do NOT play in `<img>`-loaded SVGs in any browser. Do not tell the user their animated diagram will appear animated in a README or Notion embed.

**Slack / Discord / Twitter / iMessage previews**: share links (`https://www.beauty-diagram.com/s/<slug>`) auto-unfurl with a diagram thumbnail card on these platforms — no need to manually attach a screenshot. The OG image is generated server-side from the diagram itself.

**Owner-tier fallback on embed URLs**: if the share's owner downgraded their plan AFTER saving the diagram (e.g. saved with Atelier on Pro, then downgraded to Free), `GET /v1/share/<id>.svg` returns a 200 response with a brand-fallback SVG instead of the real content. Embeds must stay 200 for `<img>`-mounted unfurls to render at all, so 403 is not used here. The owner can restore the original render by re-upgrading or switching to a free-tier theme and re-saving.

## Example

User: "Add a beautified version of this mermaid block to my README."

Agent steps:
1. Use the one-step path: `bd embed-url ./architecture.mmd --share`
   → saves the diagram and prints the embed URL, e.g.
   `https://api.beauty-diagram.com/v1/share/abc12345xyz0.svg`
2. Replace the raw mermaid block in README with:
   `![Architecture](https://api.beauty-diagram.com/v1/share/abc12345xyz0.svg)`
3. (Optional) Confirm with the user that watermark behavior matches their plan
   (free owner → watermarked; pro/premium owner → clean).

## Examples

See `examples/` for runnable sources you can adapt:

- `examples/flowchart.mmd`
- `examples/sequence.mmd`

And `scripts/` for shell wrappers you can copy into the user's repo:

- `scripts/beautify.sh`
- `scripts/export.sh`
- `scripts/ai-generate.sh` — prompt → `.mmd` source → `.svg` render
