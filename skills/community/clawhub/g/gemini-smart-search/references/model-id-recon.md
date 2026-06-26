# Gemini model ID reconnaissance

Date: 2026-03-12
Repo: `skills/gemini-smart-search`
Branch: `dev`

## Goal

Verify which Gemini Developer API model IDs are currently usable for this skill, especially where the Gemini UI / human-facing labels do **not** match the actual callable API model IDs.

## Method

Used the repo-local key path indirectly through the skill repo's local environment:

- sourced `skills/gemini-smart-search/.env.local`
- called `GET https://generativelanguage.googleapis.com/v1beta/models`
- probed candidate IDs with `:generateContent`
- sanity-checked the skill's own Python entrypoint for `cheap` / `balanced` / `deep`

No secrets are recorded here.

---

## 1. Models listed by the Gemini Developer API for this account

Relevant entries returned by `ListModels`:

- `models/gemini-2.5-flash`
- `models/gemini-2.5-flash-lite`
- `models/gemini-flash-latest`
- `models/gemini-flash-lite-latest`
- `models/gemini-3-flash-preview`
- `models/gemini-3.1-flash-lite-preview`
- `models/gemini-3-pro-preview`
- `models/gemini-3.1-pro-preview`

Also listed but less relevant to this skill:

- `models/gemini-2.0-flash`
- `models/gemini-2.0-flash-001`
- `models/gemini-2.0-flash-lite`
- `models/gemini-2.0-flash-lite-001`
- `models/gemini-2.5-flash-lite-preview-09-2025`
- image / tts / audio / embedding variants

---

## 2. Verified callable IDs

These IDs accepted `generateContent` successfully during probing.

### Stable / directly usable

- `gemini-2.5-flash-lite`
- `gemini-2.5-flash`
- `gemini-flash-lite-latest`
- `gemini-flash-latest`

### Preview / directly usable

- `gemini-3-flash-preview`
- `gemini-3.1-flash-lite-preview`

Notes:

- `gemini-3-flash-preview` is the correct callable ID behind the human-facing label **Gemini 3 Flash**.
- `gemini-3.1-flash-lite-preview` is the correct callable ID behind the human-facing label **Gemini 3.1 Flash Lite**.
- `gemini-flash-latest` and `gemini-flash-lite-latest` are valid aliases, but they are moving targets, so they are better as optional aliases than as primary pinned routing IDs.

---

## 3. Rejected / not-callable-as-typed IDs

These either failed `generateContent` or are not appropriate primary targets.

### Not found as raw UI labels

- `gemini-3-flash`
  - Result: `404 NOT_FOUND`
  - Meaning: the UI-style label is **not** the API ID; use `gemini-3-flash-preview` instead.

- `gemini-3.1-flash-lite`
  - Result: `404 NOT_FOUND`
  - Meaning: the UI-style label is **not** the API ID; use `gemini-3.1-flash-lite-preview` instead.

### Listed but not a good current target

- `gemini-2.5-flash-lite-preview-09-2025`
  - Result: `404 NOT_FOUND`
  - Error indicated it is no longer available to new users.
  - Meaning: do **not** use this preview-suffixed historical ID in routing.

---

## 4. Ambiguous / quota-limited during probing

These models are listed by `ListModels`, but live invocation was quota-limited in this session, so they should be considered **listed and likely callable**, not fully verified by successful response here.

- `gemini-3-pro-preview`
  - `ListModels`: present
  - Probe: `429 RESOURCE_EXHAUSTED`

- `gemini-3.1-pro-preview`
  - `ListModels`: present
  - Probe: `429 RESOURCE_EXHAUSTED`

Because the error was quota exhaustion rather than not-found / unsupported, these IDs are probably valid for this account, but this recon task focused on Flash / Flash-Lite routing.

---

## 5. Skill-level routing sanity check

Observed behavior from the current Python skill implementation:

### cheap

Current chain:

- display: `gemini-2.5-flash-lite` → `gemini-3.1-flash-lite` → `gemini-2.5-flash`
- API candidates expand to:
  - `gemini-2.5-flash-lite`
  - `gemini-3.1-flash-lite-preview`
  - `gemini-3.1-flash-lite`
  - `gemini-2.5-flash`

Observed result:

- succeeded immediately on `gemini-2.5-flash-lite`

### balanced

Current chain:

- display: `gemini-2.5-flash` → `gemini-3-flash` → `gemini-2.5-flash-lite`
- API candidates expand to:
  - `gemini-2.5-flash`
  - `gemini-3-flash-preview`
  - `gemini-3-flash`
  - `gemini-2.5-flash-lite`

Observed result:

- succeeded immediately on `gemini-2.5-flash`

### deep

Current chain:

- display: `gemini-3-flash` → `gemini-2.5-flash` → `gemini-3.1-flash-lite`
- API candidates expand to:
  - `gemini-3-flash-preview`
  - `gemini-3-flash`
  - `gemini-2.5-flash`
  - `gemini-3.1-flash-lite-preview`
  - `gemini-3.1-flash-lite`

Observed result:

- one direct probe earlier succeeded on `gemini-3-flash-preview`
- during the full skill run, `deep` failed because of quota exhaustion after prior probes
- non-preview labels again failed as `404 NOT_FOUND`

Interpretation:

- the routing concept is correct
- the preview fallbacks are essential
- the non-preview raw IDs for Gemini 3 Flash and Gemini 3.1 Flash Lite should remain fallback probes only if you want defensive future-proofing, but they are currently dead weight and generate predictable 404s

---

## 6. Recommended mapping updates

## Recommended human-label → API-ID mapping

### cheap

Preferred display chain:

1. `gemini-2.5-flash-lite`
2. `gemini-3.1-flash-lite`
3. `gemini-2.5-flash`

Recommended API candidate mapping:

- `gemini-2.5-flash-lite` → `gemini-2.5-flash-lite`
- `gemini-3.1-flash-lite` → `gemini-3.1-flash-lite-preview`
- `gemini-2.5-flash` → `gemini-2.5-flash`

### balanced

Preferred display chain:

1. `gemini-2.5-flash`
2. `gemini-3-flash`
3. `gemini-2.5-flash-lite`

Recommended API candidate mapping:

- `gemini-2.5-flash` → `gemini-2.5-flash`
- `gemini-3-flash` → `gemini-3-flash-preview`
- `gemini-2.5-flash-lite` → `gemini-2.5-flash-lite`

### deep

If this skill must stay Flash / Flash-Lite only:

1. `gemini-3-flash` → `gemini-3-flash-preview`
2. `gemini-2.5-flash` → `gemini-2.5-flash`
3. `gemini-3.1-flash-lite` → `gemini-3.1-flash-lite-preview`

If the skill later wants a truly stronger `deep` tier and quota/billing permit it, consider a separate design decision to introduce:

- `gemini-3-pro-preview`
- or `gemini-3.1-pro-preview`

But that would be a product decision, not just an ID-correction change.

---

## 7. Concrete recommendations for the codebase

### Keep

- probing `gemini-3-flash-preview` for the display label `gemini-3-flash`
- probing `gemini-3.1-flash-lite-preview` for the display label `gemini-3.1-flash-lite`

### Remove or demote

Strong recommendation: drop these second-stage probes unless you specifically want future API auto-healing:

- `gemini-3-flash`
- `gemini-3.1-flash-lite`

Why:

- they currently produce predictable `404 NOT_FOUND`
- they add latency and noisy failures in fallback logs
- `ListModels` already exposes the preview IDs directly, so the correct IDs are knowable

### Optional aliases

Useful but optional fallback aliases:

- `gemini-flash-latest`
- `gemini-flash-lite-latest`

These should not replace pinned primary IDs unless you explicitly want rolling behavior.

---

## Bottom line

For this account and current Gemini Developer API behavior:

- **Gemini 3 Flash** in UI maps to **`gemini-3-flash-preview`**
- **Gemini 3.1 Flash Lite** in UI maps to **`gemini-3.1-flash-lite-preview`**
- the raw non-preview labels **`gemini-3-flash`** and **`gemini-3.1-flash-lite`** are currently **not callable**
- **`gemini-2.5-flash`** and **`gemini-2.5-flash-lite`** are stable callable IDs
- `*-latest` aliases exist and work, but are optional moving-target aliases rather than the best pinned defaults
