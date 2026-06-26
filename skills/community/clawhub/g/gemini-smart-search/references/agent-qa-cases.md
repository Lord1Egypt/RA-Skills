# Agent QA Cases for `gemini-smart-search`

Date: 2026-03-12
Tester stance: adversarial / messy-agent usage, not happy-path only.

## Summary

I ran 10 cases across live calls, smoke checks, and controlled fallback simulation.

Overall status: **usable but doc-polish-needed**.

What looks solid:
- JSON success/error contract is mostly stable.
- Missing-key path is graceful and structured under `--json`.
- Fallback logic works for retryable upstream/model errors and stops on non-retryable local failures.
- `.env.local` is correctly gitignored.
- Direct Python entrypoint does load repo-local `.env.local`, matching current docs.

What is confusing or worth fixing:
- `python -m gemini_smart_search` works from `scripts/`, but this entrypoint is intentionally not supported for agents and should stay documented that way.
- Grounding citations come back as Google redirect URLs (`vertexaisearch.cloud.google.com/...`), not clean source URLs; this is valid but awkward for downstream agents/users.
- Fallback-chain reporting is good, but docs should stay explicit that `model_used` is the actual API id and may differ from display labels.

---

## Cases

### Case 1 — Non-destructive smoke suite
**Command**
```bash
bash skills/gemini-smart-search/scripts/smoke_test.sh
```
**Expected**
- parse all modes
- JSON missing-key path works
- `.env.local` ignore check passes
**Observed**
- PASS for `cheap`, `balanced`, `deep`
- PASS for `.env.local` gitignore
**Result**: PASS
**Lesson**: baseline smoke coverage is decent and quota-safe.

### Case 2 — Correct usage via shell wrapper + live cheap mode
**Command**
```bash
skills/gemini-smart-search/scripts/gemini_smart_search.sh \
  --query "BoundaryML context engineering" \
  --mode cheap \
  --json
```
**Observed**
- `ok: true`
- `model_used: gemini-2.5-flash-lite`
- citations populated
**Result**: PASS
**Lesson**: documented wrapper path works as advertised.

### Case 3 — Correct usage via direct Python + live balanced mode
**Command**
```bash
python3 skills/gemini-smart-search/scripts/gemini_smart_search.py \
  --query "BoundaryML context engineering" \
  --mode balanced \
  --json
```
**Observed**
- `ok: true`
- `model_used: gemini-2.5-flash`
**Result**: PASS
**Lesson**: Python really is a valid first-class entrypoint, not just an implementation detail.

### Case 4 — Weird realistic query + deep mode
**Command**
```bash
python3 skills/gemini-smart-search/scripts/gemini_smart_search.py \
  --query 'site:arxiv.org "3D Gaussian Splatting" "anisotropic" -pdf after:2025' \
  --mode deep \
  --json
```
**Observed**
- `ok: true`
- attempted models: `gemini-3-flash-preview` → `gemini-3-flash` → `gemini-2.5-flash`
- final `model_used: gemini-2.5-flash`
**Result**: PASS
**Lesson**: this was a real proof that mode routing/fallback is not purely theoretical.

### Case 5 — Missing-key behavior
**Command**
```bash
env -i PATH="$PATH" GEMINI_SMART_SEARCH_SKIP_LOCAL_ENV=1 \
  python3 skills/gemini-smart-search/scripts/gemini_smart_search.py \
  --query "missing key check" --mode cheap --json
```
**Observed**
- exit code `1`
- structured JSON error:
  - `type: missing_api_key`
  - clear setup message
**Result**: PASS
**Lesson**: good failure mode for orchestrators.

### Case 6 — Non-JSON mode output
**Command**
```bash
python3 skills/gemini-smart-search/scripts/gemini_smart_search.py \
  --query "BoundaryML context engineering" \
  --mode cheap
```
**Observed**
- human-readable answer
- source list printed below
**Result**: PASS
**Lesson**: workable for humans, but orchestration should continue to prefer `--json`.

### Case 7 — Invalid mode with `--json`
**Command**
```bash
python3 skills/gemini-smart-search/scripts/gemini_smart_search.py \
  --query x --mode turbo --json
```
**Observed**
- exit code `2`
- structured JSON error on stderr
- `error.type: invalid_arguments`
**Result**: PASS after fix
**Lesson**: `--json` now covers CLI argument validation failures too.

### Case 8 — Wrong entrypoint assumption: try to execute `SKILL.md` as Python
**Command**
```bash
python3 skills/gemini-smart-search/SKILL.md
```
**Observed**
- syntax error, obviously
**Result**: EXPECTED FAIL
**Lesson**: sounds silly, but agents do confuse skill docs with executable entrypoints. Keep invocation guidance very explicit and near the top.

### Case 9 — Agent-style misuse: assume module entrypoint name works
**Command**
```bash
cd skills/gemini-smart-search/scripts
python3 -m gemini_smart_search --query x --mode cheap --json
```
**Observed**
- surprisingly works
- returned valid JSON success
**Result**: PASS but undocumented
**Lesson**: agents may discover and rely on `python -m gemini_smart_search`. Decide whether to officially support it or warn against it.

### Case 10 — Simulated fallback boundary checks
I imported the Python module and monkeypatched `call_gemini` to verify behavior under controlled failures.

#### 10a. Retryable upstream/model errors should fallback
**Simulation**
- `gemini-2.5-flash-lite` → retryable 429
- `gemini-3.1-flash-lite-preview` → retryable model unavailable
- `gemini-3.1-flash-lite` → success
**Observed**
- final `model_used: gemini-3.1-flash-lite`
- attempted models recorded in order
**Result**: PASS

#### 10b. Local non-retryable bug should stop, not fallback forever
**Simulation**
- every call raises `SearchError(type='local_bug', retryable=False)`
**Observed**
- immediate failure after first attempted model
- no silent fallback to the rest of the chain
**Result**: PASS
**Lesson**: fallback boundary is implemented sensibly.

---

## Additional observations

### JSON contract check
Live success payload contained the expected top-level keys:
- `ok`
- `query`
- `mode`
- `model_used`
- `fallback_chain`
- `display_chain`
- `answer`
- `citations`
- `usage`
- `error`

This is slightly richer than the minimum contract in the skill doc and example output.

### API key precedence
By direct function check:
- if only `GEMINI_API_KEY` is present, it is used
- if `SMART_SEARCH_GEMINI_API_KEY` is also present, that one wins

This matches the documented policy.

### Citation URL quality
Citations often use Gemini/Vertex grounding redirect URLs instead of clean canonical URLs. This is not wrong, but it is awkward for:
- human reading
- deduplication
- downstream fetch steps
- storing references in notes/docs

---

## Recommended fixes

1. **Move Python invocation above wrapper invocation in `SKILL.md`.** ✅
2. **Document whether `python -m gemini_smart_search` is supported.** ✅ documented as unsupported for agents
3. **Clarify JSON guarantees.** ✅ `--json` now returns structured JSON for CLI argument validation errors too
4. **Document `model_used` as an API id, not a display label.** ✅
5. **Consider normalizing citation URLs.**
   - If grounding metadata exposes canonical URLs anywhere deeper in the response, prefer those over redirect links.
   - If not possible, at least document that redirect URLs are expected. ✅ documented; canonicalization still pending
6. **Add one automated fallback unit test harness.**
   - The simulated tests above were easy and high-signal; they belong in a checked-in test script eventually.

## Bottom line

The skill is already **practically usable**. The biggest remaining issues are not core logic failures; they are **agent ergonomics** and **contract clarity**:
- what exact entrypoints are supported,
- when JSON is guaranteed,
- and what kind of model/citation identifiers downstream agents should expect.
