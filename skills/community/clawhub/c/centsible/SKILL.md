---
name: centsible
description: >-
  Manage repository-specific micro-facts, inspect token optimization status,
  and record reusable discoveries to minimize context bloat and token consumption.
---

# Centsible Skill 🪙

This skill allows the agent and user to manage experience-driven micro-facts and token optimization.

## When to Use
- User asks about token optimization status or active facts (`centsible status`, `centsible facts list`).
- You resolved a non-trivial repo quirk (e.g. non-standard test runner, mandatory environment flag, path alias) that future turns will need.
- Testing pattern matching against prompts.

## Commands

### 1. Check Status & Token ROI Stats
```bash
centsible status
centsible stats
centsible stats --transcript <path_to_transcript.jsonl> --json
```

### Loop Guard Thresholds & Reflection
Pick a mode preset, or fine-tune thresholds and reflection modes.
- Modes (errors / identical calls): `ultra` 2/3, `normal` 3/4 (default), `weak` 4/5.
- Reflection modes:
  - `inline` (default): in-turn reflection, agent saves facts before final response; zero extra turns, answers never collapsed in UI.
  - `hook`: Stop hook reflection; blocks session termination to force a continuation turn.
  - `off`: disables reflection prompts.
```bash
centsible config mode ultra
centsible config reflect inline # In-turn reflection without extra turns (default)
centsible config reflect hook   # Force extra continuation turn on wrap-up
centsible config reflect off    # Disable reflection nudges
centsible config list
centsible config set max_consecutive_errors 4
centsible config unset max_consecutive_errors
```
Keys: `mode`, `reflect`, `max_consecutive_errors`, `max_identical_calls`. Env vars `CENTSIBLE_LOOP_MODE`, `CENTSIBLE_REFLECT`, `CENTSIBLE_MAX_*` override the file.

### 2. List Micro-Facts
```bash
centsible facts list
```

### 3. Add a Micro-Fact
Always keep the fact to a single, direct sentence without conversational padding:
```bash
centsible facts add --pattern "<regex_pattern>" --fact "<one_line_fact>"
```
Examples:
```bash
centsible facts add --pattern "pytest.{0,40}(fail|error|slow)" --fact "Run unit tests with 'pytest tests/ -q --tb=short'."
centsible facts add --pattern "docker.{0,30}(build|compose)" --fact "Pass --progress=plain to docker build to keep logs short."
centsible facts add --pattern "auth/login\.py" --fact "Never mutate token keys directly."
```

The pattern decides when the fact is injected, so it must describe the *situation*, not a keyword. Saving is
rejected (exit 2) for a lone short word (`pytest`, `bruno`, `pip`), for generic words only (`run.*test`), and for
facts over 240 characters. Anchor on, in order of strength:
1. an identifier: file, script, table, API path or flag (`deploy_staging`, `run-e2e`, `a/b.py`);
2. a tool plus a symptom (`pytest.{0,40}(fail|error)`);
3. an action plus object plus context (`(create|book).{0,12}order.{0,40}(uat|stg)`).

Before saving, check a couple of prompts that must not match with `centsible facts test "<prompt>"`.
`--force` overrides the check; use it only when the pattern is deliberately broad.

### 4. Test Fact Matching
Verify what facts trigger for a specific user prompt:
```bash
centsible facts test "How do I run the bruno tests?"
```

### 5. Remove Stale Fact
```bash
centsible facts remove <id_or_pattern>
```

### 6. Harvest Golden Facts (Agentic Multi-Turn Discovery)
When working in a new repository or after a fresh install, discover 5–8 golden architectural facts:
```bash
centsible harvest
centsible harvest --prompt
```
- In Claude Code: type `/centsible-harvest`
- In Antigravity: ask your agent `"Run centsible harvest to discover golden facts for this repo"`
