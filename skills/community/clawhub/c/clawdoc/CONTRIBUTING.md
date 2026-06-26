# Contributing to clawdoc

## How to add a new pattern detector

1. **Add a fixture** in `tests/fixtures/` — one JSONL file that exercises the new pattern. Name it `NN-pattern-name.jsonl`. Make it 20-150 lines, realistic timestamps, realistic token counts.

2. **Add the detector function** in `scripts/diagnose.sh`:
   ```bash
   detect_my_pattern() {
     # Extract signals with jq
     local signal
     signal=$(jq -s '...' "$JSONL")

     [ -z "$signal" ] && return

     add_finding "$(jq -nc \
       --arg evidence "..." \
       --arg prescription "..." \
       --argjson cost_impact 0.0 \
       '{pattern:"my-pattern", pattern_id:12, severity:"medium",
         evidence:$evidence, cost_impact:$cost_impact, prescription:$prescription}')"
   }
   ```
   Call it at the bottom of the detector list.

3. **Add the pattern** to `templates/patterns.json` with the same `id`, `name`, `severity`, and `description`.

4. **Add the pattern** to the Pattern reference table in `SKILL.md`.

5. **Add a test assertion** in `tests/test-detection.sh`:
   ```bash
   check "NN-pattern-name.jsonl" "My pattern description" "12" ""
   ```

6. **Run the test suite**: `make test` — all tests must pass.

7. **Update CHANGELOG.md** with what you added.

## Detector design principles

- **Deterministic only** — no LLM calls, no network, no random. Same input = same output always.
- **False negatives > false positives** — a missed finding is better than a wrong one. Users lose trust from incorrect alarms.
- **Evidence is specific** — "exec called 25 times with 'bash daily-report.sh'" not "exec called many times". Include the actual value.
- **Prescription is actionable** — tell the user the exact config key to change, the exact command to run, or the exact file to edit.
- **Severity is cost-calibrated**:
  - 🔴 critical: active money loss or session failure right now
  - 🔴 high: significant money loss or repeated silent failure
  - 🟡 medium: preventable waste or degraded reliability
  - 🟢 low: best-practice gap, no urgent impact

## Detection thresholds

Current thresholds and their rationale (change only with evidence):

| Detector | Threshold | Rationale |
|----------|-----------|-----------|
| 1 (infinite retry) | 5+ consecutive same-tool calls | <5 is plausible legitimate retry; >5 is almost always a loop |
| 4 (context exhaustion) | 70% of context window | Leaves 30% buffer; >90% upgrades severity to high |
| 6 (cost spike) | $0.50/turn high, $1.00/turn critical, $1.00/session (configurable via `CLAWDOC_COST_TURN_HIGH`, `CLAWDOC_COST_TURN_CRITICAL`, `CLAWDOC_COST_SESSION`) | Defaults calibrated for Sonnet-class; raise for Opus-class models |
| 8 (model routing waste) | cron/heartbeat + opus/sonnet/gpt-4o | Haiku is 20-50x cheaper for identical simple tasks |
| 9 (cron accumulation) | 2x token growth | 20% growth is noise; 2x signals structural accumulation |
| 11 (workspace overhead) | 15% of context window | Industry guidance; >15% meaningfully shrinks working space |
| 12 (task drift) | 3+ calls to new dirs (>50% of post-compaction) OR 10+ consecutive reads | Post-compaction: agent touching entirely new directories signals lost context. Exploration: 10+ reads without editing means no forward progress |

## Code style

- `set -euo pipefail` at the top of every script — no exceptions
- Functions for each detector: `detect_infinite_retry()`, `detect_non_retryable()`, etc.
- All stdout is valid JSON (parseable by `jq`) except `headline.sh` and `prescribe.sh`
- Use stderr (`>&2`) for progress/debug messages
- No Python, no Node, no external packages beyond jq

## Running tests

```bash
make test          # all 57 tests
make lint          # shellcheck (requires: brew install shellcheck)
make check-deps    # verify jq, awk, bash versions
```

## Submitting

1. Fork the repo
2. Create a branch: `git checkout -b add-pattern-NN-my-pattern`
3. Add fixture + detector + test + SKILL.md entry + CHANGELOG entry
4. `make test && make lint` must pass
5. Open a PR with the fixture output, detector output, and before/after test results in the description
