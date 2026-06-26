# Gemini Smart Search QA Test Plan

Focus on the first implementation only. Keep tests non-destructive and JSON-first.

## Scope

Validate these behaviors before calling the first implementation "usable":

1. repo-local env loading
2. JSON contract stability
3. fallback behavior boundaries
4. ignored secret file behavior
5. non-destructive smoke execution

## High-priority findings from scaffold review

- Python is now intended to be the canonical entrypoint.
- Repo-local `.env.local` should be loaded consistently by Python, with the shell wrapper remaining a convenience layer.
- QA should keep checking that direct Python invocation and wrapper invocation behave equivalently for env resolution.

## Test matrix

### 1) Local env loading

Goal: confirm repo-local `.env.local` is loaded only through the intended entrypoint, or move loading into Python if direct invocation must remain supported.

Checks:
- Wrapper invocation loads `.env.local` and exposes the preferred key.
- Direct Python invocation behavior is explicitly defined and tested.
- Precedence is correct:
  1. `SMART_SEARCH_GEMINI_API_KEY`
  2. `GEMINI_API_KEY`
- Missing-key path returns structured JSON, not a traceback.
- `GEMINI_SMART_SEARCH_SKIP_LOCAL_ENV=1` is treated as a **Python-entrypoint** test control only; wrapper parity tests must account for the wrapper sourcing `.env.local` before exec.

Suggested assertions:
- `error.api_key_present` flips predictably under controlled env conditions.
- No key value is ever echoed into stdout/stderr.

### 2) JSON contract

Goal: keep orchestrator-facing output stable.

Required top-level keys:
- `ok`
- `query`
- `mode`
- `model_used`
- `fallback_chain`
- `answer`
- `citations`
- `error`

Also verify:
- `usage.provider == "gemini"`
- `usage.grounding` is boolean
- `citations` is always a list
- `fallback_chain` is always a list
- error responses remain JSON when `--json` is used
- success responses set `error: null`

### 3) Fallback behavior

Goal: fallback only on model/provider-side issues, not on local bugs.

Must fallback on:
- 429 / quota exceeded
- model unavailable / unsupported
- transient upstream failure

Must not fallback on:
- invalid CLI arguments
- local import/config bugs
- malformed local response parsing

Suggested implementation-time tests:
- stub model call results to simulate `429`, `503`, and permanent local exceptions
- assert attempted model order matches mode chain
- assert final JSON includes the full attempted chain or enough detail to audit routing

### 4) Ignored secret file behavior

Goal: secret-bearing local config stays untracked.

Checks:
- `.env.local` is matched by `.gitignore`
- `git check-ignore .env.local` succeeds
- `git status --short --ignored` shows `.env.local` as ignored, not tracked
- no sample key is stored in tracked files

### 5) Non-destructive smoke tests

Goal: basic confidence without spending quota or mutating state.

Smoke tests should avoid real web calls by default.

Recommended minimum smoke set:
- parse CLI args for all three modes
- emit valid JSON with `--json`
- wrapper path works without traceback
- missing-key path stays graceful
- ignored-file check passes
- use `GEMINI_SMART_SEARCH_SKIP_LOCAL_ENV=1` so missing-key smoke checks stay quota-free even when a local `.env.local` exists

Optional live smoke gate:
- run a single cheap-mode query only when an explicit opt-in flag is set
- keep query harmless and low-cost
- log model used and citation count, never the API key

## Release gate for v1

Do not call v1 ready until all of these are true:
- wrapper/direct-entrypoint behavior is documented and intentional
- JSON contract is validated in automation
- fallback triggers are tested with stubs or fixtures
- `.env.local` remains ignored
- default smoke tests are non-destructive and quota-free

## Recommended next implementation move

Chosen direction:

1. **Python is the supported entrypoint**
   - `.env.local` loading should happen in Python
   - shell remains a thin convenience wrapper
   - test both, but treat Python as canonical

That choice removes the earlier entrypoint mismatch and should stay stable unless the skill is later promoted into a plugin/tool.
