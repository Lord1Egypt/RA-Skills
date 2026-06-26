---
name: gemini-smart-search
description: Search the web using Gemini with Google Search grounding through a local script, with model routing and quota fallback across Gemini Flash-Lite / Flash variants. Use when web research should stay inside the Gemini family, when dynamic model switching is needed without restarting the OpenClaw gateway, when a separate Gemini API key/quota pool should be used, or when repeated search tasks need cheap/balanced/deep modes with structured JSON output.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "primaryEnv": "SMART_SEARCH_GEMINI_API_KEY"
      }
  }
---

# Gemini Smart Search

Use this skill when Gemini should be the search backend, but gateway-level `web_search` config is too static or too disruptive to change.

## Purpose

This skill is a **script-backed search workflow**, not a gateway tool override.

It exists to provide:
- dynamic Gemini model selection
- quota-aware fallback
- a separate Gemini API key path if desired
- structured JSON output
- no gateway restart requirement for model changes

## Modes

Model routing is split into two layers:
- **display chain**: human-facing preferred model family labels
- **candidate API ids**: the actual model ids to probe, especially for 3.x preview-era models

Current display chains:

- **cheap**
  - Prefer `gemini-2.5-flash-lite`
  - Then `gemini-3.1-flash-lite`
  - Then `gemini-2.5-flash`
- **balanced**
  - Prefer `gemini-2.5-flash`
  - Then `gemini-3-flash`
  - Then `gemini-2.5-flash-lite`
- **deep**
  - Prefer `gemini-3-flash`
  - Then `gemini-2.5-flash`
  - Then `gemini-3.1-flash-lite`

For 3.x models, do not assume the UI label is the raw API id. Probe candidate ids such as preview-suffixed names when needed.

## Invocation

Run the Python script or the shell wrapper via `exec` and request JSON output.

Python is now the canonical entrypoint because it also loads repo-local `.env.local` when present. The shell wrapper remains a convenience layer.

Primary example (preferred):

```bash
python3 skills/gemini-smart-search/scripts/gemini_smart_search.py \
  --query "BoundaryML context engineering" \
  --mode cheap \
  --json
```

Wrapper example (convenience only):

```bash
bash skills/gemini-smart-search/scripts/gemini_smart_search.sh \
  --query "BoundaryML context engineering" \
  --mode cheap \
  --json
```

`python -m gemini_smart_search` may work when run from the `scripts/` directory, but it is **not** a supported interface for agents right now. Do not depend on it.

## Output contract

Expect JSON with at least:
- `ok`
- `query`
- `mode`
- `model_used`
- `fallback_chain`
- `display_chain`
- `answer`
- `citations`
- `error`
- `escalation`

Notes:
- `model_used` is the **actual probed API model id** (for example `gemini-3-flash-preview`), not the human-facing display label.
- Citation URLs may initially be Google/Vertex grounding redirect URLs instead of canonical source URLs; treat that as a known current limitation.
- With `--json`, supported runtime paths should return structured JSON on both success and error. Invalid CLI arguments now also return JSON when `--json` is present.

## API key policy

The script should prefer a dedicated key path for this skill, then fall back to the standard Gemini key.

Required key resolution order:
1. `SMART_SEARCH_GEMINI_API_KEY` (primary declared env)
2. `GEMINI_API_KEY` (compatibility fallback)

If neither key is present, the agent must explicitly ask the human for a Gemini API key before claiming setup is complete.

Do not store the key in tracked repository files. Prefer a repo-local, gitignored file such as `.env.local`.

See `references/config.md`.

## When to use this skill instead of built-in `web_search`

Use this skill when:
- you want Gemini-only search
- you want to test or isolate quota pools
- you want model routing without touching gateway config
- you want predictable JSON output for downstream orchestration

Do **not** use this skill when:
- a normal built-in `web_search` is sufficient
- you need non-Gemini providers
- you only need to fetch and read a known URL (`web_fetch`)
- you need logged-in or JS-heavy page interaction (`browser`)

## Fallback policy

Fallback only for errors like:
- quota exceeded / 429
- model unavailable
- transient upstream failure

Do not silently fallback on obvious local/script bugs or invalid arguments.

## References

- `references/config.md` — environment variables and design notes
- `references/qa-test-plan.md` — focused QA scope for v1 behavior and release gates
- `references/qa-results-2026-03-12.md` — CLI-oriented QA outcomes from the current release cycle
- `references/agent-qa-cases.md` — adversarial agent-style misuse review
- `references/model-id-recon.md` — verified callable Gemini model IDs and mapping notes
- `references/escalation-design.md` — when to return a GitHub issue URL for human escalation
- `references/release-checklist.md` — artifact release checklist with current completion status
- `references/development-goals-v0.1.1.md` — next small version scope and artifact policy
- `references/release-notes-v0.1.1.md` — release notes for the current artifact
- `assets/example-output.json` — expected response shape
- `scripts/smoke_test.sh` — non-destructive local smoke checks for the scaffold
- `scripts/prepare_artifact.sh` — deterministic clean artifact export helper

## Status

Python implementation is now wired for a first real version:
- direct Gemini API call path
- Google Search grounding enabled
- mode-based model routing
- Python-side repo-local `.env.local` loading
- fallback across Gemini Flash-Lite / Flash variants for retryable upstream errors
- structured JSON output for orchestration

This is still intentionally minimal: it does not yet expose advanced tuning flags, caching, or richer citation post-processing.

Before publishing an artifact, consult `references/release-checklist.md`, review `references/development-goals-v0.1.1.md`, run `scripts/prepare_artifact.sh`, and publish the release note in `references/release-notes-v0.1.1.md` alongside the artifact.
