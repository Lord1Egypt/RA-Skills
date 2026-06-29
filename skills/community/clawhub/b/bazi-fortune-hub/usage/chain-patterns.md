# Snippet: Chain Patterns (t1 → t2 → t3 → t4)

> Audience: external agent LLM. Load on demand when the user opens a fortune query.
> Field schemas → `../SKILL.md`. This snippet is **chain behavior only**.

## Why this snippet exists

The 4 fortune tools form a **strict chain**. Mis-ordering or re-calling t1/t2 wastes
credits and ~25–90s of wall time. The most common LLM mistake is **re-running t1/t2
to regenerate inputs that a previous step already produced** — pass the prior output
through instead.

## The chain (4 steps, sequential, paid, OneShot)

```
t1 bazi_basic_analysis          → base_context             (sub-second, pure algorithm)
   ↓
t2 bazi_pattern_analysis        → pattern_result           (~25s, 1 LLM call)
   ↓
t3 bigluck_year_analysis        → year_analysis_result     (sub-second, pure algorithm)
   ↓
t4 bigluck_year_fortune_eval    → final narrative          (~30–90s, 1 LLM call)
```

**Total wall time: ~90–120s.** Cost per tool is **live** (fetched at runtime from the
pricing database) — call m2 `get_user_credits` for the current numbers; never hardcode them. Set the client
tool-call timeout to **≥ 120s** (t4 tail latency). The hub's `maxDuration=300` covers it
server-side; the limit you feel is your client.

## OneShot — there is no resume

**Every fortune tool returns the complete result in a single `tools/call`.** There is
**no** `done` flag, **no** `job_id`, and **no** polling.


- If a step fails, you do **not** "resume" it — you **re-run that step** with the same
  inputs (the outputs of the earlier steps you already hold). See "Failure inside the
  chain" below.

## The 3 rules

### Rule 1 — Sequential, never parallel

t2 takes t1's `base_context` (**not** the raw birth fields). t3 needs `base_context` +
`pattern_result` (both derived from t2's output) + `target_year`. t4 needs
`year_analysis_result` (t3's whole result) + `pattern_result`. **You cannot parallelize
the chain.** Calling t3 before t2 finishes fails with `INVALID_INPUT`; the
`details.issues[]` array (each entry `{ path, message }`) names the missing field — here
`pattern_result`.

### Rule 2 — Pass outputs through; don't regenerate them

t1 and t2 are the expensive inputs (t2 has an LLM call). Once you have `base_context`
and `pattern_result`, reuse them for t3 and t4. Re-calling t1/t2 re-charges credits and
produces fresh objects that you'd just be throwing the old ones away for.

### Rule 3 — One call per step, read the full result

```jsonc
// Single call to t3 — returns the complete year_analysis_result
POST /api/mcp  { "method": "tools/call", "params": { "name": "bigluck_year_analysis",
  "arguments": {
    "base_context":   { /* from t1 */ },
    "pattern_result": { /* from t2 */ },
    "target_year":    2026
  } } }

// Response (complete, OneShot — no done flag, no token)
{ "result": { "content": [ { "type": "text", "text": "{ ...year_analysis_result... }" } ] } }
```

The same applies to t4.

## Pseudocode (agent-agnostic, pseudo-Python)

> `r.data` below is the tool payload (REST: the object under `data`; MCP:
> `JSON.parse(result.content[0].text)`). The payload has a **single** `data` layer — read
> `r.data.base_context`, not `r.data.data.base_context`.

```python
state = {}

# Step 1 — pure algorithm, sub-second. Takes the raw birth fields.
r1 = call("bazi_basic_analysis", {
    "birth_year": 1985, "birth_month": 7, "birth_day": 15,
    "birth_hour": 14, "birth_minute": 30, "gender": "male",
    "location": {"city_name": "Beijing"},
})
state.base_context = r1.data["base_context"]

# Step 2 — LLM ~25s, OneShot. Takes t1's base_context (NOT the birth fields).
r2 = call("bazi_pattern_analysis", {
    "base_context": state.base_context,
})
# t2 returns { final_result, partial }
state.pattern_result = r2.data["final_result"]["pattern_result"]
state.base_context   = r2.data["partial"]["base_context"]   # context carried forward

# Step 3 — pure algorithm; pass t1 + t2 through. Returns { final_result, partial }.
r3 = call("bigluck_year_analysis", {
    "base_context":   state.base_context,
    "pattern_result": state.pattern_result,
    "target_year":    user_target_year,
})

# Step 4 — LLM ~30-90s; takes t3's whole result + pattern_result (NOT base_context).
# year_analysis_result must keep t3's `partial` inline alongside final_result's fields.
r4 = call("bigluck_year_fortune_eval", {
    "year_analysis_result": { **r3.data["final_result"], "partial": r3.data["partial"] },
    "pattern_result":       r3.data["partial"]["pattern_result"],
})
state.final = r4.data["final_result"]
```

> Note on t1 vs t2 inputs: **t1 takes the raw birth fields; t2 takes t1's `base_context`.**
> `../references/12-tools.md` is authoritative for field-level schemas — follow it.

## Reuse across turns — don't re-call t1/t2

If the user opens a follow-up in the same conversation (e.g. "What about 2027 instead of
2026?"):

- **Do not** re-call t1 or t2. The `base_context` and `pattern_result` are still valid
  for the same person.
- Re-call **only t3** (with `target_year: 2027`), then **t4** with the new
  `year_analysis_result` + the cached `pattern_result`.

## When to call only t1 / only t1 + t2

- **Basic chart only** ("What is my BaZi?"): call t1 alone. Do not call t2/t3/t4.
- **Pattern reading** ("我是什么格局"): call t1 then t2. Skip t3/t4 unless the user asks
  about a specific year.

## Failure inside the chain

- **t1 fails** (`INVALID_INPUT` / `UPSTREAM_ERROR` / `REST_ERROR`): nothing downstream to do.
  Surface the error; do not call t2/t3/t4 (they have no inputs).
- **t2 fails**: same — surface, do not continue.
- **t3 fails** (5xx / `UPSTREAM_TIMEOUT`): **re-run t3** with the same
  `base_context` + `pattern_result` you already hold. Never restart from t1. There is no
  token to pass — it's a fresh OneShot call.
- **t4 fails**: **re-run t4** with the same `year_analysis_result` + `pattern_result`.
- **t4 client timeout** (the call blocks past your 120s client limit): the server may
  still be finishing (`maxDuration=300`). Wait ~30s, then **re-run t4** with the same
  inputs (a fresh OneShot call). There is no token to pass and no partial state to recover.

## What the user sees

You don't have to dump the whole chain output on the user. A good pattern:

1. After t1: "Got your basic chart — your day master is X, your dayun starts Y."
2. After t2: "Your pattern is X — short one-line interpretation."
3. After t3: (no narration; t3 is structural)
4. After t4: the actual reading. This is what the user came for.

If the chain fails partway, narrate the partial result you have and what failed in the
next step — never silently retry.
