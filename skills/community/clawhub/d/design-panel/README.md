# /design-panel

A Claude Code skill that runs a multi-persona design review against a live web app. Four UX/UI designer personas review in parallel, then vote on each other's findings to surface the changes most worth shipping.

Sits naturally alongside `/design-review`: this skill diagnoses across multiple lenses, `/design-review` ships the fixes.

## What it does

Point it at a running web app (or just run it from your project root — it figures out the dev server from `package.json` / `Cargo.toml` / `pyproject.toml` / `Gemfile` / `go.mod`). Then:

1. Classifies the app as **LANDING** / **APP_UI** / **HYBRID**.
2. Captures an evidence pack — screenshots at multiple viewports, key interactions, computed CSS.
3. Dispatches 4 personas as parallel Claude subagents. Each reviews the same evidence from its own lens, returns structured findings.
4. Runs a voting round: each persona scores every other persona's findings 0–10 from its own perspective.
5. Ranks findings by `impact_score = mean_cross_score × severity_weight`. Three views: **Top 5** (the ship list), **Dissent watch** (where the panel disagreed), **Persona-only signal** (specialist insight that mean-ranking washes out).
6. Writes `report.md` (human-readable) and `fix-plan.md` (machine-readable, schema-versioned).

## Personas

| ID | Name | Lens |
|---|---|---|
| `a11y` | Accessibility Auditor | Contrast, focus order, ARIA, keyboard, touch targets, landmarks |
| `conversion` | Conversion Optimizer | CTA hierarchy, funnel friction, trust signals, form UX |
| `brand` | Brand & Visual Director | Typography, color system, premium feel, AI-slop patterns |
| `motion` | Motion & Interaction Designer | Microinteractions, perceived speed, feedback on action |
| `mobile` | Mobile-First Designer | Thumb zones, viewport, tap targets, horizontal scroll |
| `ia` | Information Architect | Wayfinding, breadcrumbs, page titles, content hierarchy |
| `trust` | Trust & Credibility Reviewer | Social proof, copy honesty, dark patterns, error empathy |
| `power` | Power-User Advocate | Keyboard shortcuts, density, bulk actions, efficiency |

Default selection (skill picks 4 of 8 based on app type):

- **LANDING** → `brand`, `conversion`, `trust`, `mobile`
- **APP_UI** → `ia`, `a11y`, `power`, `mobile`
- **HYBRID** → `brand`, `conversion`, `a11y`, `ia`

## Install

```bash
git clone https://github.com/kaicianflone/design-panel ~/repos/design-panel
ln -s ~/repos/design-panel ~/.claude/skills/design-panel
```

Or copy if you don't want a symlink:

```bash
mkdir -p ~/.claude/skills/design-panel
cp -r ~/repos/design-panel/* ~/.claude/skills/design-panel/
```

Claude Code discovers the skill on next session.

## Invoke

```
/design-panel                            # detect project + dev server from cwd
/design-panel http://localhost:3000      # explicit URL
/design-panel https://example.com        # remote/deployed URL
/design-panel --personas a11y,brand,mobile,conversion   # explicit roster
/design-panel --personas +motion         # add motion to defaults
/design-panel --personas -trust          # drop trust from defaults
/design-panel --deep                     # all 8 personas (confirms before spawning)
/design-panel --report-only              # skip the final hand-off tip
/design-panel --yes                      # non-interactive (skips --deep cost prompt)
```

## Project detection

When called without a `<url>`, the skill walks the current working directory looking for stack indicators and infers the dev URL. Supported out of the box:

| Stack indicator | Framework heuristic | Default URL |
|---|---|---|
| `package.json` with `next` dep | Next.js | `http://localhost:3000` |
| `package.json` with `vite` dep | Vite (React/Vue/Svelte/etc.) | `http://localhost:5173` |
| `package.json` with `nuxt` dep | Nuxt | `http://localhost:3000` |
| `package.json` with `astro` dep | Astro | `http://localhost:4321` |
| `package.json` (generic) | Falls back to `scripts.dev` port or 3000 | `http://localhost:3000` |
| `Gemfile` with `rails` | Rails | `http://localhost:3000` |
| `pyproject.toml` / `requirements.txt` | Python (FastAPI/Django/Flask common) | `http://localhost:8000` |
| `Cargo.toml` | Rust (probably axum/actix) | `http://localhost:8080` |
| `go.mod` | Go | `http://localhost:8080` |

If the inferred URL isn't reachable, the skill prints the right start command for your stack (e.g. `npm run dev`, `bundle exec rails server`) and stops — no port scanning, no AskUserQuestion roulette.

If you want a different URL or non-default port, pass it explicitly: `/design-panel http://localhost:<port>`.

## Outputs

Two files in `docs/design-panel/` of the project you're reviewing:

- `report-YYYY-MM-DD-HHMM.md` — human-readable with Top 5, Dissent watch, Persona-only signal, full findings collapsed at the bottom.
- `fix-plan-YYYY-MM-DD-HHMM.md` — `schema_version: 1` frontmatter, machine-readable. Each fix has `id`, `severity`, `title`, `where`, `change`, `verify` (required), plus optional `evidence_path`, `file_hint`, `impact_score`.

You can hand the `fix-plan` to `/design-review` as a direct fix list:

> "Read the fix plan at `docs/design-panel/fix-plan-2026-05-13-1442.md` and run your Phase 8 fix loop against the entries listed there."

`/design-review` reads the plan, locates each fix's source, applies the change, runs the verify check, and commits per its standard fix loop.

## Cost shape

- **Standard run (4 personas):** 8 subagent dispatches across 2 parallel waves. Expected wall-clock: 60–120s. Hard cap: 300s.
- **`--deep` run (8 personas):** 16 dispatches. Expected wall-clock: 180–300s. Hard cap: 600s. Always confirmed via AskUserQuestion unless `--yes`.

Each subagent is a billed Claude API call. Cost varies by account tier; typical run is a few cents.

## Exit codes

- `0` — clean run, both artifacts written.
- `1` — partial run (some personas/voters failed; report tagged accordingly).
- `2` — aborted (no URL reachable, all subagents failed, or duration cap hit).
- `3` — invalid input (unknown persona id, malformed flag).

## Requirements

- Claude Code (any recent version)
- A web app reachable via HTTP (local dev server or deployed URL)
- A browser surface: `$B` from [gstack](https://github.com/garrytan/gstack) or `mcp__browse__*` MCP tools. The skill detects which is available.
- Anthropic API key with billing enabled

## License

[MIT](./LICENSE)
