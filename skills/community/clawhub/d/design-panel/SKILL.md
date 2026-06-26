---
name: design-panel
description: |
  Multi-persona design review. Dispatches 4 UX/UI designer personas in parallel against
  a live web app, then converges on the highest-impact changes via cross-persona voting.
  Outputs a ranked report and a machine-readable fix plan. Pairs with /design-review for
  shipping the top findings.
  Use when asked to "design panel", "multi-persona design review", "designer panel",
  "panel review", or after major design milestones.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Agent
---

# /design-panel — Multi-Persona Design Review

> Runs 4 UX/UI designer personas in parallel against a live app, then ranks findings
> via cross-persona voting. Outputs a report and a machine-readable fix plan.
> Pairs with /design-review for shipping the ranked fixes.

## ROLE

You are the **Panel Orchestrator**. You do not author findings yourself, do not score findings yourself, do not "improve" persona prompts on the fly. You:

1. Run pre-flight + arg parsing (Phase 0)
2. Detect app-type with a visible `DETECTED:` line (Phase 1)
3. Capture an evidence pack (Phase 2)
4. Select personas (Phase 3)
5. Dispatch all persona reviews in a single parallel Agent call (Phase 4)
6. Dispatch all voting subagents in a single parallel Agent call (Phase 5)
7. Compute ranking, write `report.md` + `fix-plan.md` (Phase 6)
8. Print artifact paths + an optional gstack hand-off tip (Phase 7)

The fix-plan is a data artifact. Anyone (including the user) can feed it to `/design-review` manually if they want to ship the fixes — this skill never invokes other skills automatically.

## Base directory for this skill

The harness exposes the skill's install directory via the "Base directory" line at the top of the loaded skill content. Persona files live at `<base-dir>/personas/<id>.md`. Reference that path explicitly in Phase 4/5 prompts — do not hardcode an absolute path.

---

## TELEMETRY PREAMBLE (run first)

```bash
# gstack-style telemetry preamble — inlined, not inherited.
_TEL=$(~/.claude/skills/gstack/bin/gstack-config get telemetry 2>/dev/null || echo "off")
_TEL_START=$(date +%s)
_SESSION_ID="$$-$(date +%s)"
_OUTCOME="success"  # default; abort/error gates override before epilogue
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "TELEMETRY: ${_TEL:-off}  SESSION: $_SESSION_ID  BRANCH: $_BRANCH"

# Pending marker — epilogue clears it; if the skill crashes the next gstack
# skill to start finalizes it as outcome=unknown.
mkdir -p ~/.gstack/analytics
echo '{"skill":"design-panel","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","session_id":"'"$_SESSION_ID"'"}' \
  > ~/.gstack/analytics/.pending-"$_SESSION_ID" 2>/dev/null || true

# Local analytics start row (gated on gstack telemetry tier)
if [ "$_TEL" != "off" ]; then
  echo '{"skill":"design-panel","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo unknown)'"}' \
    >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
fi

# Timeline event for skill start. Best-effort; failures are silenced.
if [ -x ~/.claude/skills/gstack/bin/gstack-timeline-log ]; then
  _TL_PAYLOAD=$(jq -nc --arg branch "$_BRANCH" --arg sid "$_SESSION_ID" \
    '{skill:"design-panel",event:"started",branch:$branch,session:$sid}' 2>/dev/null || echo '{}')
  ~/.claude/skills/gstack/bin/gstack-timeline-log "$_TL_PAYLOAD" 2>/dev/null &
fi

# Persist telemetry state to disk so the epilogue can recover it even after
# the shell context is lost (each Bash tool call is a fresh shell).
mkdir -p ~/.gstack/analytics
cat > ~/.gstack/analytics/.tel-design-panel-"$_SESSION_ID".sh <<EOF
export _TEL="$_TEL"
export _TEL_START="$_TEL_START"
export _SESSION_ID="$_SESSION_ID"
export _OUTCOME="$_OUTCOME"
EOF
echo "TEL_STATE: ~/.gstack/analytics/.tel-design-panel-$_SESSION_ID.sh"
```

**Note on gstack dependencies:** If `gstack-config` or `gstack-timeline-log` is missing, the bash blocks above silently fall through to `|| true` paths. The skill still runs, just without telemetry. That's intentional — gstack is recommended but not required.

---

## PHASE 0 — Pre-flight + arg parsing

### 0.1 Parse arguments

The user invocation may include:
- `<url>` — optional. If absent, attempt local dev server detection (see 0.2).
- `--personas <list>` — explicit roster (e.g. `a11y,brand,mobile,conversion`), `+id` to add to defaults, `-id` to remove.
- `--deep` — runs all 8 personas instead of the default 4.
- `--report-only` — skip the Phase 7 "next steps" suggestion.
- `--yes` — non-interactive. Auto-confirms the `--deep` cost prompt.

Capture into shell variables: `URL`, `PERSONAS_OVERRIDE`, `DEEP`, `REPORT_ONLY`, `YES`.

### 0.2 Detect project + dev server (only if no `<url>` given)

Read the current working directory for stack indicators. Infer:

1. The project framework (Next.js, Vite, Rails, Django, etc.)
2. The expected dev URL for that framework's defaults
3. The right command to start the dev server

Then probe the inferred URL. If reachable → use it. If not → tell the user the exact command to start it. Do not port-scan a generic list; do not interrogate the user when the project file already tells us what to do.

```bash
_PROJECT_TYPE="unknown"
_EXPECTED_URL=""
_DEV_CMD=""

if [ -f package.json ]; then
  # Package manager from lockfile
  if   [ -f bun.lockb ] || [ -f bun.lock ]; then _PM="bun"
  elif [ -f pnpm-lock.yaml ];                  then _PM="pnpm"
  elif [ -f yarn.lock ];                       then _PM="yarn"
  else                                              _PM="npm"; fi

  # Framework from deps
  if jq -e '(.dependencies // {}).next // (.devDependencies // {}).next' package.json >/dev/null 2>&1; then
    _PROJECT_TYPE="next";  _EXPECTED_URL="http://localhost:3000"
  elif jq -e '(.dependencies // {}).nuxt // (.devDependencies // {}).nuxt' package.json >/dev/null 2>&1; then
    _PROJECT_TYPE="nuxt";  _EXPECTED_URL="http://localhost:3000"
  elif jq -e '(.dependencies // {}).astro // (.devDependencies // {}).astro' package.json >/dev/null 2>&1; then
    _PROJECT_TYPE="astro"; _EXPECTED_URL="http://localhost:4321"
  elif jq -e '(.dependencies // {}).vite // (.devDependencies // {}).vite' package.json >/dev/null 2>&1; then
    _PROJECT_TYPE="vite";  _EXPECTED_URL="http://localhost:5173"
  elif jq -e '(.dependencies // {})["@remix-run/dev"] // (.devDependencies // {})["@remix-run/dev"]' package.json >/dev/null 2>&1; then
    _PROJECT_TYPE="remix"; _EXPECTED_URL="http://localhost:3000"
  elif jq -e '(.dependencies // {})["@sveltejs/kit"] // (.devDependencies // {})["@sveltejs/kit"]' package.json >/dev/null 2>&1; then
    _PROJECT_TYPE="sveltekit"; _EXPECTED_URL="http://localhost:5173"
  else
    _PROJECT_TYPE="node"; _EXPECTED_URL="http://localhost:3000"
  fi

  # Dev command — prefer scripts.dev, fall back to scripts.start
  _SCRIPT_KEY=$(jq -r 'if .scripts.dev then "dev" elif .scripts.start then "start" else empty end' package.json 2>/dev/null)
  if [ -n "$_SCRIPT_KEY" ]; then
    _DEV_CMD="$_PM run $_SCRIPT_KEY"
  else
    _DEV_CMD="$_PM run dev   # (no scripts.dev defined — add one to package.json)"
  fi

elif [ -f Gemfile ]; then
  _PROJECT_TYPE="rails"
  _EXPECTED_URL="http://localhost:3000"
  _DEV_CMD="bundle exec rails server"

elif [ -f manage.py ]; then
  _PROJECT_TYPE="django"
  _EXPECTED_URL="http://localhost:8000"
  _DEV_CMD="python manage.py runserver"

elif [ -f pyproject.toml ] || [ -f requirements.txt ]; then
  _PROJECT_TYPE="python"
  _EXPECTED_URL="http://localhost:8000"
  if grep -qiE '^fastapi' pyproject.toml requirements.txt 2>/dev/null; then
    _DEV_CMD="uvicorn main:app --reload"
  elif grep -qiE '^flask' pyproject.toml requirements.txt 2>/dev/null; then
    _DEV_CMD="flask run"
  else
    _DEV_CMD="python -m http.server 8000   # (adapt to your app's entry point)"
  fi

elif [ -f Cargo.toml ]; then
  _PROJECT_TYPE="rust"
  _EXPECTED_URL="http://localhost:8080"
  _DEV_CMD="cargo run"

elif [ -f go.mod ]; then
  _PROJECT_TYPE="go"
  _EXPECTED_URL="http://localhost:8080"
  _DEV_CMD="go run ."

elif [ -f mix.exs ]; then
  _PROJECT_TYPE="phoenix"
  _EXPECTED_URL="http://localhost:4000"
  _DEV_CMD="mix phx.server"
fi

echo "PROJECT: $_PROJECT_TYPE  EXPECTED: ${_EXPECTED_URL:-none}  DEV_CMD: ${_DEV_CMD:-none}"

# Probe the expected URL (2s timeout — local servers respond fast)
URL_FOUND=""
if [ -n "$_EXPECTED_URL" ]; then
  if curl -sf -m 2 -o /dev/null "$_EXPECTED_URL" 2>/dev/null; then
    URL_FOUND="$_EXPECTED_URL"
  fi
fi
echo "URL_REACHABLE: ${URL_FOUND:-none}"
```

### Decision tree

1. **`URL` was passed explicitly** → use it. Skip the detection prints (already shown above; that's fine — they're informational, not an interaction).
2. **`URL_FOUND` non-empty** → use it. Project detection confirmed and reachable.
3. **`_EXPECTED_URL` known but unreachable**:
   - Print:
     ```
     DETECTED: <project_type> project. Expected URL: <_EXPECTED_URL>
     NOT_RUNNING: <_EXPECTED_URL> is not reachable.
     Start your dev server first:
       <_DEV_CMD>
     Then re-run /design-panel.
     ```
   - With `--yes`: exit 2.
   - Without `--yes`: AskUserQuestion with three options:
     - A) I started it — re-probe and continue
     - B) Use a different URL (then ask for URL)
     - C) Cancel (exit 2)
4. **`_PROJECT_TYPE` is `unknown`** (no recognized stack indicator in cwd):
   - With `--yes`: print `ERROR: no <url> arg, no recognized project in cwd (looked for package.json, Gemfile, manage.py, pyproject.toml, Cargo.toml, go.mod, mix.exs). Re-run with an explicit URL.` exit 2.
   - Without `--yes`: AskUserQuestion: "No recognized project in cwd. Paste the URL you want me to review, or start your app and re-run."

### Notes

- Detection is heuristic. The `_DEV_CMD` printed in not-running messages is a best-guess for the framework's defaults. If the user has a custom port or non-standard launcher, they should pass `<url>` explicitly.
- Monorepos: the skill reads the cwd's `package.json` only. If you're in a monorepo with workspace-relative apps, `cd` into the app's directory before invoking.
- Remote URLs (deployed staging/prod): always pass `<url>` explicitly. Detection only helps with local dev.

### 0.3 Print duration estimate

Before starting any expensive work, print one line so the user knows the time budget:

```
EXPECTED DURATION: ~90s (standard, 4 personas). Use --yes to skip --deep cost prompts.
```

If `--deep` was passed without `--yes`, AskUserQuestion:

> "Run all 8 personas? Cost: ~16 subagent dispatches, expected 180–300s wall-clock.
> A) Yes  B) Standard run (4 personas) instead  C) Cancel"

If `--yes` and `--deep`, skip the confirmation; log "--deep accepted via --yes" to telemetry.

### 0.4 Hard duration caps

- Standard run: 300s ceiling. If exceeded, abort and write partial findings with `[aborted-at-cap]` tag.
- `--deep` run: 600s ceiling. Same partial-write behavior.

Implement via wall-clock checks at each phase boundary, not signal handlers.

---

## PHASE 1 — App-type detection (with visibility contract)

Fetch the URL via `$B navigate` (gstack browse binary) or `mcp__browse__*` if `$B` isn't on PATH. Pull the DOM via snapshot.

Classify as one of:

- **LANDING** — no auth UI detected, has hero+CTA pattern, `<main>` content is marketing sections (testimonials, pricing, feature grids).
- **APP_UI** — login/auth flow detected, OR sidebar/topbar app chrome present, OR routes match patterns like `/dashboard`, `/settings`, `/projects/...`.
- **HYBRID** — marketing homepage with authenticated product behind a CTA.

Ambiguous results default to HYBRID (most conservative roster). Log heuristic scores in the report header for transparency.

### Visibility contract — Phase 1 ALWAYS prints one of:

```
DETECTED: http://localhost:3000  (APP_UI, confidence 0.82)
```

…or, if URL is missing:

```
NO_URL: no <url> arg and no local dev server found. Asking…
```

This guarantees the user knows within a few seconds whether the skill is on the right target — no silent screenshot phase against the wrong URL.

---

## PHASE 2 — Evidence pack capture

**Location:** `~/.gstack/sessions/$SESSION_ID/design-panel/evidence/`

```
evidence/
├── manifest.json                  # routes, viewports, captures performed
├── screenshots/
│   ├── home_desktop.png           # 1440×900
│   ├── home_mobile.png            # 390×844
│   ├── home_tablet.png            # 768×1024  (only with --deep)
│   ├── <route>_desktop.png        # one set per significant route
│   └── <route>_mobile.png
├── interactions/
│   ├── hover_primary_cta.png      # key hover/focus states
│   ├── nav_open_mobile.png        # mobile nav opened
│   └── form_filled.png            # form mid-state if present
└── computed.json                  # CSS vars, font stacks, palette,
                                   # breakpoints, motion durations
```

**Capture strategy:**

- **Routes:** homepage always. Up to 4 additional routes auto-detected, in this priority order:
  1. Routes listed in `/sitemap.xml` if present, capped at 4.
  2. Otherwise, the first 4 unique same-origin `<a href>` targets in the primary `<nav>` element.
  3. Otherwise, homepage only.
- **Viewports:** desktop (1440) + mobile (390) always. Tablet (768) only with `--deep`.
- **Interactions:** primary CTA hover, mobile nav open, first form's filled state — captured if present, silently skipped otherwise.
- **`computed.json`:** small data file pulled from the live page (CSS custom properties, font-family stacks, used colors, defined breakpoints, transition durations).

**Authenticated apps:** If the target redirects to `/login`, halt with the auth failure path (see Failure modes).

**Why disk, not inline:** subagent prompts pass file paths; same artifacts are read by all review and voting subagents; user can sanity-check what the panel saw.

**Cleanup:** session dir is reaped by gstack's existing 120-minute mtime cleanup (or accumulates harmlessly if gstack isn't installed).

---

## PHASE 3 — Persona selection

### Roster (8 personas, files at `<base-dir>/personas/<id>.md`)

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

### Default selection (4 of 8, picked by app type)

| App type | Default 4 |
|---|---|
| LANDING | `brand`, `conversion`, `trust`, `mobile` |
| APP_UI | `ia`, `a11y`, `power`, `mobile` |
| HYBRID | `brand`, `conversion`, `a11y`, `ia` |

Bumping from 3 to 4 personas-by-default exists for statistical reasons: at N=3 each finding has only 2 cross-voters; at N=4 it has 3, which gives meaningful agreement signal instead of coin-flip stdev. Cost trade: ~33% more subagent dispatches per run.

### Override syntax

- `--personas brand,a11y,motion,trust` — explicit list (skips auto-selection).
- `--personas +motion` — add to defaults.
- `--personas -trust` — remove from defaults.
- `--deep` — run all 8 (confirmed via AskUserQuestion unless `--yes`).
- Unknown persona ids hard-fail with exit code 3 and the valid id list.

### Output

Log the final persona list to the report header. Example:

```
PERSONAS: ia, a11y, power, mobile  (APP_UI default)
```

---

## Shared schemas (used by Phase 4 and Phase 5 prompts)

### Finding schema (Phase 4 output — one entry per finding)

```json
{
  "persona_id": "a11y",
  "id": "a11y-001",
  "title": "Primary CTA fails 4.5:1 contrast on hero",
  "severity": "high",
  "evidence": ["screenshots/home_desktop.png"],
  "where": "hero section, .btn-primary",
  "why_from_my_lens": "Users with low vision can't read the most important action on the page.",
  "suggested_fix": "Darken --color-primary from #6B8AFD to #4A6BE8 (passes 4.7:1).",
  "file_hint": "src/styles/tokens.css or wherever --color-primary is defined"
}
```

- `severity`: enum `critical | high | medium`.
- `id`: persona-prefixed for cross-merge uniqueness.
- `evidence`: paths RELATIVE to the evidence pack root.

### Score schema (Phase 5 output — one per voting persona)

```json
{
  "voter_persona_id": "brand",
  "scores": [
    { "finding_id": "a11y-001", "score": 7, "reason": "Better contrast also reads more premium." },
    { "finding_id": "conversion-003", "score": 9, "reason": "Hero anchor is the brand's whole pitch." }
  ]
}
```

- `score`: integer 0–10.
- A persona does NOT score its own findings (filter on the voter side; the orchestrator also defends with a filter in Phase 6).

---

## PHASE 4 — Parallel persona reviews

For each selected persona, build a dispatch prompt. The prompt has four parts:

1. **The persona's full markdown content** — Read from `<base-dir>/personas/<id>.md` and include verbatim. This is the persona's role + rubric.
2. **The evidence pack path** — `~/.gstack/sessions/$SESSION_ID/design-panel/evidence/`. Tell the subagent to read `manifest.json` first to know what's available.
3. **The Finding schema (above)** — Include the schema definition verbatim so the subagent emits the exact shape.
4. **The output path** — Tell the subagent to write its findings JSON to `~/.gstack/sessions/$SESSION_ID/design-panel/findings/<persona_id>.json`.

### Dispatch rule

Dispatch ALL N Agent calls in a **single orchestrator message**. They run in parallel. Do NOT call them sequentially — that defeats the parallel design.

For each persona, the Agent call has:
- `subagent_type: "general-purpose"`
- `model: "sonnet"` (taste + judgment for review work; haiku is too thin for this)
- `description: "design-panel review: <persona_id>"`
- `prompt`: the four-part prompt above
- No `isolation` flag — these are read-only reviews, no commits.

### Subagent prompt template

```
You are the {persona.name} from /design-panel. Read your full role/rubric below, then review the live app via the evidence pack at the path provided.

## Your role and rubric (verbatim from persona file)

{full content of <base-dir>/personas/<persona_id>.md}

## Evidence pack

Path: ~/.gstack/sessions/{SESSION_ID}/design-panel/evidence/

Start by reading manifest.json to see what was captured. Then inspect screenshots and computed.json relevant to your lens. Do NOT navigate the live URL — you review only what's in the evidence pack.

## Required output

Return findings as a JSON object matching this exact schema:

{
  "persona_id": "{persona_id}",
  "findings": [
    {
      "id": "string (must start with '{persona_id}-' followed by a 3-digit number, e.g. '{persona_id}-001')",
      "title": "string (one-line label, <80 chars)",
      "severity": "critical | high | medium",
      "evidence": ["string (path relative to evidence/, e.g. 'screenshots/home_desktop.png')"],
      "where": "string (component, section, or selector)",
      "why_from_my_lens": "string (one sentence from YOUR lens, not generic)",
      "suggested_fix": "string (concrete proposed change)",
      "file_hint": "string (likely source path, optional — leave as empty string if unknown)"
    }
  ]
}

Write the result to: ~/.gstack/sessions/{SESSION_ID}/design-panel/findings/{persona_id}.json

## Rules

- 3–10 findings. Quality over quantity. Don't pad.
- Every finding's evidence array must reference at least one real file in the evidence pack.
- Severity rubric is in your role above. Use it.
- Stay in your lens. If you find something outside your lens (e.g. you're a11y and you notice a brand issue), DO NOT include it. Other personas cover those.
- Write the JSON file before returning.
```

### After dispatch

Wait for all returns. Tag each persona's result: success / failed (timeout) / malformed-output (JSON parse failure). If <2 personas succeed, abort the run with the "all reviews failed" failure mode.

---

## PHASE 5 — Cross-persona voting

Concatenate all findings into `~/.gstack/sessions/$SESSION_ID/design-panel/all_findings.json`:

```json
[
  { /* finding from persona A */ },
  { /* finding from persona A */ },
  { /* finding from persona B */ },
  ...
]
```

IDs are persona-prefixed so duplicates indicate a subagent bug — surface them in the report header, do not silently merge.

### Dispatch rule (same as Phase 4)

For each persona, build a voting prompt and dispatch all N Agent calls in a **single message**. Each voter gets:

- Its own persona markdown file (for consistent voice)
- The full `all_findings.json` content
- The rule "score only findings from OTHER personas"
- The Score schema

Each voting Agent call:
- `subagent_type: "general-purpose"`
- `model: "sonnet"` (judgment matters)
- `description: "design-panel voting: <persona_id>"`
- `prompt`: the voting prompt
- No `isolation` flag.

### Voting prompt template

```
You are the {persona.name} from /design-panel, now in voting mode.

## Your role and lens (verbatim from persona file)

{full content of <base-dir>/personas/<persona_id>.md}

## Findings to score

Below are findings from the OTHER personas on this panel. For each one, score 0–10 how impactful you think this change would be from YOUR lens (where 10 = ships a meaningfully better product, 0 = irrelevant or wrong from where you sit).

Include a one-sentence reason per score.

Do NOT re-review the app. Do NOT add new findings. Score only what's given.

Do NOT score findings where persona_id == "{persona_id}" (your own). Skip those entirely — the orchestrator filters them too, but you should also filter to keep your output clean.

## Findings

{contents of all_findings.json}

## Required output

Return JSON matching this schema:

{
  "voter_persona_id": "{persona_id}",
  "scores": [
    { "finding_id": "string (id from the findings above)", "score": <integer 0-10>, "reason": "string (one sentence)" }
  ]
}

Write the result to: ~/.gstack/sessions/{SESSION_ID}/design-panel/scores/{persona_id}.json
```

### After dispatch

Wait for all returns. Drop any voter that returns malformed JSON. If <2 voters survive, fall back to severity-only ranking and tag the report `[no cross-vote]`.

---

## PHASE 6 — Ranking + write artifacts

### Ranking math

For each finding `f`:

```
severity_weight  = { critical: 1.5, high: 1.0, medium: 0.6 }[f.severity]
cross_scores     = scores from all OTHER personas (self excluded)
mean_cross_score = mean(cross_scores)        # 0..10
agreement_spread = max(cross_scores) - min(cross_scores)  # 0..10
impact_score     = mean_cross_score × severity_weight
```

Sort by `impact_score` descending. Ties broken by lower spread (consensus wins over divisive picks).

### Statistical caveats by N

- **N=4 standard run** — 3 cross-voters per finding. Mean is meaningful. Spread is directional. The Dissent watch flags findings where spread ≥ 5 points.
- **N=8 `--deep` run** — 7 cross-voters per finding. Both mean and spread are meaningful. Dissent watch uses spread ≥ 4.
- **N=3 (only reachable via `--personas a,b,c`)** — 2 cross-voters per finding. Stats are thin; Dissent watch is suppressed and the report header is tagged `[N=3 — voting signal directional only]`.
- **N<3 (only reachable via `--personas a,b` after failures)** — voting round is skipped entirely. Ranking falls back to severity-only and the report header is tagged `[no cross-vote]`.

### Three views in the report

- **Top 5** — highest `impact_score`. The ship list.
- **Dissent watch** — top 3 findings by `agreement_spread` (threshold above). Divisive findings often reveal taste/strategy tradeoffs, not bugs.
- **Persona-only signal** — for each persona, the highest-rated finding *only they cared about* (where cross-voters scored it ≤ 4 but the originator marked it ≥ high). Captures specialist insight that mean-ranking washes out.

### Artifact 1: `docs/design-panel/report-YYYY-MM-DD-HHMM.md`

Human-readable. Skeleton:

```markdown
# Design Panel Review — <date>

**App type:** APP_UI
**Personas:** Information Architect, Accessibility Auditor, Power-User Advocate, Mobile-First Designer
**Pages reviewed:** /, /dashboard, /settings
**Evidence pack:** ~/.gstack/sessions/<id>/design-panel/evidence/
**Schema version:** 1

## Top 5 (ship list)

### 1. Primary CTA fails 4.5:1 contrast on hero — impact 12.4
- **Flagged by:** Accessibility Auditor (severity: high)
- **Cross-scores:** IA 7, Power-User 6, Mobile 7 (mean 6.7, spread 1 — high agreement)
- **Top dissent reason:** "Better contrast also reads more premium" — IA
- **Suggested fix:** Darken `--color-primary` from `#6B8AFD` to `#4A6BE8`.
- **Where to look:** `src/styles/tokens.css`
- **Evidence:** ![](../../<evidence-pack-path>/screenshots/home_desktop.png)

[... entries 2–5 ...]

## Dissent watch (panel disagreed)

[Top 3 findings by spread — useful for taste/strategy calls]

## Persona-only signal

- **Information Architect's solo pick:** Breadcrumbs missing on /settings/* — only IA flagged it; worth a look if site grows.
- **Accessibility Auditor's solo pick:** ...
- **Power-User Advocate's solo pick:** ...
- **Mobile-First Designer's solo pick:** ...

## All findings (collapsed)

<details>
<summary>26 findings total</summary>

[Full list, grouped by persona]

</details>
```

### Artifact 2: `docs/design-panel/fix-plan-YYYY-MM-DD-HHMM.md`

Machine-readable. Header is YAML frontmatter; body is a checkbox list with structured sub-bullets.

```markdown
---
schema_version: 1
source: design-panel
generated_at: 2026-05-13T14:42:00Z
source_report: docs/design-panel/report-2026-05-13-1442.md
n_personas: 4
n_findings: 5
---

# Fix Plan — <date>

## Fixes (top 5, impact-ordered)

- [ ] **a11y-001** Primary CTA contrast
  - severity: high
  - where: hero section, .btn-primary
  - change: `--color-primary: #6B8AFD` → `#4A6BE8`
  - verify: contrast ≥ 4.5:1 against `--color-background`
  - evidence_path: screenshots/home_desktop.png
  - file_hint: src/styles/tokens.css
  - impact_score: 12.4

- [ ] **conversion-003** Hero value-prop buried below fold on mobile
  - severity: high
  - where: hero, primary CTA section
  - change: move tagline above feature grid on viewports < 768px
  - verify: tagline visible in mobile screenshot above the fold
  - evidence_path: screenshots/home_mobile.png
  - file_hint: src/components/Hero.tsx
  - impact_score: 11.8

[... etc ...]
```

**Required fields per entry:** `id`, `severity`, `title` (implicit in the heading), `where`, `change`, `verify`.

**Optional fields per entry:** `evidence_path`, `file_hint`, `impact_score`.

Anyone consuming this file (a future tool, a human, or hand-fed into another skill) reads the YAML frontmatter for the version, then iterates entries. Unknown fields are ignored. Schema is intentionally narrow.

---

## PHASE 7 — Handoff (or stop, depending on flags)

Print the artifact paths first, always:

```
Design Panel complete.

  Report:    docs/design-panel/report-2026-05-13-1442.md
  Fix plan:  docs/design-panel/fix-plan-2026-05-13-1442.md

  Top finding: Primary CTA fails 4.5:1 contrast (impact 12.4)
  Panel disagreed on:  2 findings (see Dissent watch)
```

### If `--report-only`

Stop here. Exit 0.

### Otherwise — gstack hand-off tip

Print one suggestion (one-line):

```
If you use gstack, you can hand-feed the fix-plan to /design-review:
  "Read the fix plan at docs/design-panel/fix-plan-2026-05-13-1442.md and run your
   Phase 8 fix loop against the entries listed there."
```

The skill does NOT invoke `/design-review` automatically. No AskUserQuestion. The fix-plan is data; what the user does with it is their call.

Exit 0.

---

## FAILURE MODES

Every failure mode follows the **problem + cause + fix** template — the user sees what broke, why, and the next command to run.

| Scenario | Exit | User sees |
|---|---|---|
| No URL given, no local dev server detected | — | `NO_URL: no <url> arg and no local dev server found.` → AskUserQuestion for URL |
| Browse can't reach URL (network, 5xx, JS error) | 2 | `ERROR: could not reach <url> (<reason>). Is your dev server running? Re-run with: /design-panel <url>` |
| App requires auth, no cookies imported | 2 | `BLOCKED: <url> redirected to /login. /design-panel needs an authenticated session for APP_UI. Fix: import cookies for the domain (gstack: /setup-browser-cookies), then re-run.` |
| App-type detection ambiguous | — | Defaults to HYBRID with `WARNING: app-type detection inconclusive (LANDING 0.41, APP_UI 0.39, HYBRID 0.45). Using HYBRID. Override with --personas if wrong.` |
| Unknown persona id in `--personas` | 3 | `ERROR: unknown persona id '<id>'. Valid: a11y, conversion, brand, motion, mobile, ia, trust, power. Fix: check spelling.` |
| One review subagent fails | 1 | `WARNING: persona '<id>' review failed (<reason>). Continuing with N-1/N personas. Report tagged [partial].` |
| Voting subagent returns malformed JSON | 1 | `WARNING: persona '<id>' voting output unparseable. Dropping voter. Remaining: <N> voters.` |
| <2 voters survive | 1 | Falls back to severity-only ranking. Report header tagged `[no cross-vote]`. |
| All review subagents fail | 2 | `ERROR: all <N> review subagents failed. No findings to report. If you use gstack, try /design-review on the same URL for a single-reviewer pass.` |
| Evidence capture partial (e.g., mobile screenshot failed) | — | Proceeds. Each persona's prompt notes which evidence is missing so it can flag any reasoning that depends on it. |
| `--deep` requested without `--yes` | — | AskUserQuestion: "Run all 8 personas? Cost: ~16 subagent dispatches, expected 180–300s. (A) Yes  (B) Standard run (4) instead  (C) Cancel" |
| `--deep` requested with `--yes` | — | Skips confirmation. Logs `--deep accepted via --yes` to telemetry. |
| Duration cap hit (300s standard / 600s deep) | 1 | `ABORTED at duration cap. Partial findings written: <K>/<N> personas completed. Report tagged [aborted-at-cap].` |
| `docs/design-panel/` doesn't exist in target repo | — | Created silently. |

---

## ORCHESTRATOR HARD RULES

- You are the Panel Orchestrator. You do NOT author findings, do NOT score findings, do NOT edit persona prompts on the fly.
- Phase 4 and Phase 5 each dispatch ALL Agent calls in a single message (parallel tool calls). Sequential dispatch is a bug.
- Personas always read from the evidence pack only. They never navigate the live URL during review.
- The skill never invokes `/design-review` automatically. The fix-plan is data; users decide what to do with it.
- Unknown persona ids hard-fail. No silent fallback.
- If <2 review subagents succeed, abort the run. Cross-voting against 1 reviewer is meaningless.
- Honor `--yes` strictly: no AskUserQuestion if `--yes` is set. Auto-confirm the `--deep` cost prompt.

---

## OPERATIONAL BEHAVIOR

- **Voice:** match gstack voice if available (no AI vocabulary, no em dashes, lead with the point, be concrete). The skill is gstack-flavored; persona reviews should be too.
- **Telemetry epilogue:** before exit, run the standard end-row write. Mirror the preamble's pattern, using the `.tel-design-panel-<sid>.sh` file for state recovery.
- **`PROACTIVE: false` respect:** if the user's gstack config has `proactive: false`, the skill does not auto-suggest itself anywhere. (This skill is invoked explicitly anyway, but the rule applies to error messages that suggest re-running.)
- **`EXPLAIN_LEVEL: terse` respect:** if gstack's `explain_level` is `terse`, strip the duration-estimate prose, persona list announcement, and gstack hand-off tip — print only what's strictly needed (the DETECTED line, error messages, final artifact paths).
- **Learnings hook (if gstack present):** at the start of the skill, run `~/.claude/skills/gstack/bin/gstack-learnings-search --limit 3` and include any prior `/design-panel` findings from the same repo. Marks them as `Prior learning applied:` in the report.
- **Telemetry event format:**
  ```json
  {"skill":"design-panel","personas":["ia","a11y","power","mobile"],"app_type":"APP_UI","n_findings":26,"top_impact":12.4,"duration_s":87,"outcome":"success"}
  ```

### Telemetry epilogue (run last, before exit)

```bash
# Source recovered state if the shell context was lost.
# Substitute the literal TEL_STATE path printed by the preamble.
source ~/.gstack/analytics/.tel-design-panel-"$_SESSION_ID".sh 2>/dev/null || true

_TEL_END=$(date +%s)
_TEL_DUR=$(( _TEL_END - ${_TEL_START:-$_TEL_END} ))
rm -f ~/.gstack/analytics/.pending-"$_SESSION_ID" 2>/dev/null || true

if [ -x ~/.claude/skills/gstack/bin/gstack-timeline-log ]; then
  _TL_BR=$(git branch --show-current 2>/dev/null || echo unknown)
  _TL_PAYLOAD=$(jq -nc --arg branch "$_TL_BR" --arg sid "$_SESSION_ID" --arg outcome "$_OUTCOME" --argjson dur "$_TEL_DUR" \
    '{skill:"design-panel",event:"completed",branch:$branch,outcome:$outcome,duration_s:$dur,session:$sid}' 2>/dev/null || echo '{}')
  ~/.claude/skills/gstack/bin/gstack-timeline-log "$_TL_PAYLOAD" 2>/dev/null || true
fi

if [ "$_TEL" != "off" ]; then
  echo '{"skill":"design-panel","duration_s":"'"$_TEL_DUR"'","outcome":"'"$_OUTCOME"'","session":"'"$_SESSION_ID"'","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
fi

[ -n "${_SESSION_ID:-}" ] && rm -f ~/.gstack/analytics/.tel-design-panel-"$_SESSION_ID".sh 2>/dev/null || true
```

---

## COST SHAPE

- **Standard run (4 personas):** 8 subagent dispatches across 2 parallel waves (4 review + 4 voting), plus one browse session. Expected wall-clock: **60–120s**. Hard cap: 300s.
- **`--deep` run (8 personas):** 16 dispatches across 2 waves. Expected wall-clock: **180–300s**. Hard cap: 600s. Always confirmed via AskUserQuestion unless `--yes`.
- Voting prompts are smaller than review prompts (no screenshots; just the JSON findings array). Wave 2 is typically 30–50% of wave 1's wall-clock.

---

## START

Run the TELEMETRY PREAMBLE. Then Phase 0 (arg parse + URL detect + duration estimate). Then Phase 1 (DETECTED line). Then Phase 2 (evidence pack). Then Phase 3 (persona selection). Then Phase 4 (parallel reviews — single Agent message). Then Phase 5 (parallel voting — single Agent message). Then Phase 6 (rank + write artifacts). Then Phase 7 (print + optional gstack tip). Then the telemetry epilogue.

Do NOT skip Phase 1's DETECTED line. Do NOT dispatch sequentially. Do NOT invoke `/design-review`.
