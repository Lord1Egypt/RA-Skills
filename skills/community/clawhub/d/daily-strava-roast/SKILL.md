---
name: daily-strava-roast
description: Generate a playful or sharp daily roast of recent Strava activity. Use when asked to roast, recap, tease, or humorously summarize a Strava workout or a recent day of training. Useful for scheduled daily activity roasts, playful fitness summaries, or lightly sarcastic post-workout commentary. Prefer the deterministic package/script for data prep and fallback; when running inside OpenClaw, use the connected/default runtime model only for the final paragraph if available, then fall back to the deterministic roast path on failure.
---

# Daily Strava Roast

Use this skill to turn recent Strava activity into a short roast-style summary.

## Default workflow

1. Use the deterministic implementation first to fetch and summarize activity.
2. If you are inside OpenClaw and want the V2 path, use the structured context/prompt output as model input for the **final paragraph only**.
3. If connected-model generation is unavailable or weak, fall back to the deterministic roast output.
4. Do not pretend the standalone Python package has a built-in OpenClaw connected-model API if it does not.

## What this skill does

This skill provides:
- deterministic Strava fetch + summary tooling
- adjustable tones and spice levels
- V1 roast fallback that is stable and testable
- V2 context/prompt building for better final-paragraph generation in the OpenClaw runtime

## Preferred commands

Use the packaged CLI for deterministic preparation and fallback:

```bash
uv run --project {baseDir} daily-strava-roast summary --json --pretty
uv run --project {baseDir} daily-strava-roast context --pretty
uv run --project {baseDir} daily-strava-roast prompt
uv run --project {baseDir} daily-strava-roast roast
```

Do not rely on the removed legacy script path. Use the packaged CLI commands only.

## Runtime guidance

When invoked inside OpenClaw for an actual roast reply:
- run deterministic preparation first
- use the connected/default runtime model only to write the final roast paragraph
- keep that paragraph to one short paragraph
- do not invent stats
- if generation fails, return the deterministic roast instead of erroring

### Runtime recipe

Use this sequence:

1. Build context JSON:

```bash
uv run --project {baseDir} daily-strava-roast context --pretty
```

2. Build the constrained prompt:

```bash
uv run --project {baseDir} daily-strava-roast prompt
```

3. Ask the connected/default OpenClaw runtime model to write the final paragraph from that prompt.
4. Before replying, sanity-check the generated paragraph:
   - exactly one paragraph
   - one or two sentences max unless unusually short
   - no bullet points
   - no invented stats
   - no stat dump; usually no more than two concrete metrics unless a third really earns its place
   - not generic AI filler
   - avoids banned phrases, stale identity/relationship jokes, pet phrases, and over-clever wording
   - avoids poetic or cosmic phrasing
   - tone matches requested spice/tone closely enough
5. If the paragraph fails those checks or generation is unavailable, fall back to:

```bash
uv run --project {baseDir} daily-strava-roast roast
```

### Fallback triggers

Fall back immediately if any of these happen:
- no connected/default runtime model is available
- generated output is empty
- generated output invents numbers, activities, or claims not present in the prompt/context
- generated output is multiple paragraphs or list-like
- generated output crams in too many stats without real comedic payoff
- generated output uses banned phrases or obvious close variants
- generated output leans on stale identity, relationship, or defining-trait jokes
- generated output leans on polished LLM-clever wording instead of dry mockery
- generated output drifts into poetic, cosmic, or overly ornate phrasing
- generated output is obviously generic, repetitive, or less readable than the deterministic roast

When falling back:
- do not apologize unless the user needs to know
- just return the deterministic roast text

When working purely from the repo/CLI:
- treat connected-model generation as a runtime concern, not a packaged-CLI feature
- keep the deterministic path working without extra runtime dependencies

## Inputs

By default the skill reads Strava app config from:

```bash
~/.openclaw/secure/strava_app.json
```

And by default the token file is:

```bash
~/.openclaw/workspace/agents/tars-fit/strava_tokens.json
```

Normal auth behaviour:
- treat `~/.openclaw/secure/strava_app.json` as the canonical app-credentials source
- if setup already exists, expired access tokens should refresh automatically using the refresh token
- if Strava still returns 401, retry once after a forced refresh
- if the token file is missing, invalid, or missing required fields, treat that as **initial setup required** and tell the user clearly
- if the token file exists but app credentials are missing or incomplete, return **config_incomplete** clearly
- if setup exists but refresh/reauthorisation is needed, return the reauth-required path instead of pretending it is a rest day
- avoid depending on sourced shell profiles for routine auth

Use this to inspect auth readiness:

```bash
uv run --project {baseDir} daily-strava-roast auth-url
```

Use JSON mode when another agent needs machine-readable status:

```bash
uv run --project {baseDir} daily-strava-roast roast --json --pretty
```

## Tones

Supported tones:
- `dry`
- `playful`
- `savage`
- `coach`

## Spice

Spice controls roast intensity:
- `0` — gentle
- `1` — light tease
- `2` — proper roast
- `3` — scorched earth

## References

Read as needed:
- `references/design.md` for roast heuristics and failure cases
- `docs/V2.md` for the V2 architecture and package/runtime boundary
