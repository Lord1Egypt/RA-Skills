# QA Results — 2026-03-12

Focused CLI-level QA for the current `gemini-smart-search` implementation.

## Case matrix

| ID | Area | Invocation | Outcome | Notes |
| --- | --- | --- | --- | --- |
| T01 | JSON contract + env | Python, `GEMINI_SMART_SEARCH_SKIP_LOCAL_ENV=1`, no keys | PASS | Structured JSON error; `error.type=missing_api_key`; required top-level keys present. |
| T02 | Entrypoint consistency + env | Shell wrapper, `.env.local` temporarily hidden, no keys | PASS | Wrapper returns the same structured missing-key JSON shape as Python. |
| T03 | Env precedence | Python, both key vars set to invalid values | PASS | Behavior indicates `SMART_SEARCH_GEMINI_API_KEY` wins over `GEMINI_API_KEY`; first attempted model returns `INVALID_ARGUMENT`; no fallback on bad local auth. |
| T04 | CLI argument boundary | Python, invalid `--mode bogus --json` | PASS | Exit code `2`; structured JSON error is emitted on stderr with `error.type=invalid_arguments`. |
| T05 | Live cheap-mode contract | Python, cheap live query | PASS | Real call succeeded; `model_used=gemini-2.5-flash-lite`; JSON contract intact. |
| T06 | Wrapper vs Python live parity | Shell wrapper, same cheap live query | PASS | Wrapper and Python both succeed with the same model and equivalent JSON shape. |
| T07 | Citation output shape | Python, cheap live query | PASS with caveat | `citations` is always a list of `{title,url}` objects, but URLs are grounding redirect links (`vertexaisearch.cloud.google.com/...`) rather than canonical source URLs. |
| T08 | Routing metadata + fallback | Python, deep live query | PASS with caveat | Deep mode fell through `gemini-3-flash-preview` and `gemini-3-flash` before succeeding on `gemini-2.5-flash`; `usage.attempted_models` correctly records the route. |
| T09 | Secret file hygiene | `git check-ignore .env.local` | PASS | `.env.local` is ignored and not tracked. |

## Main findings

### Confirmed working

- Python and shell wrapper are consistent for both missing-key and live-query paths.
- JSON contract is stable across success and structured error paths when `--json` is used.
- Local missing-key handling is graceful and traceback-free.
- Fallback does **not** trigger on obvious local auth/config failure (`INVALID_ARGUMENT` bad key), which is the right boundary.
- `usage.attempted_models` is useful and currently accurate for auditing fallback behavior.

### Bugs / risks

1. **Citation URLs are redirect wrappers, not canonical source links**
   - Live citations consistently returned URLs like `https://vertexaisearch.cloud.google.com/grounding-api-redirect/...`.
   - This is valid as a URL field, but poor for downstream consumers expecting stable, human-meaningful source URLs.
   - Risk: link rot, poor UX, harder deduplication, harder post-processing.

2. **Deep-mode preferred Gemini 3 candidates look stale or unavailable in practice**
   - In live testing, `deep` mode attempted `gemini-3-flash-preview`, then `gemini-3-flash`, and only succeeded on `gemini-2.5-flash`.
   - This may reflect quota/model availability drift, but it means the nominal `deep` preference is not what users actually get today.
   - Risk: silent cost/performance mismatch versus documented mode intent.

3. **Error JSON omits explicit selected-key provenance**
   - QA could infer precedence behavior from outcome, but the script does not expose which key source was selected.
   - That keeps secrets safer, but it makes debugging env precedence slightly opaque.
   - Risk: slower diagnosis when both env vars exist and one is stale.

## Recommendations

- Normalize citations toward canonical source URLs if grounding metadata exposes them, or document clearly that current URLs are Google grounding redirects.
- Re-verify real Gemini 3 model IDs against the currently visible API inventory and refresh `MODEL_CANDIDATES` if needed.
- Consider adding a non-secret debug field such as `usage.api_key_source` with values like `SMART_SEARCH_GEMINI_API_KEY` / `GEMINI_API_KEY` only when `--json` is used, if easier env debugging is worth the extra contract surface.
