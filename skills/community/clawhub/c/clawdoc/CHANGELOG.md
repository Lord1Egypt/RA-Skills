# Changelog

All notable changes to clawdoc are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.12.0] — 2026-03-18

### Changed
- **SKILL.md rewritten** — removed all inline bash code blocks; all diagnostics now route through hardened scripts that require explicit user-provided paths. No more auto-discovery of session directories or workspace config files.
- **Demo scripts moved to `dev/`** — `generate-demo.sh` and `demo.sh` are no longer in shipped `scripts/` or `docs/` directories. Not included in `install.sh` output.
- **`.learnings/` writes are now opt-in** — `prescribe.sh` only writes to `.learnings/LEARNINGS.md` when `CLAWDOC_LEARNINGS=1` is set.

### Security
- **Removed all `eval` usage** — replaced with safe alternatives or eliminated entirely.
- **Removed all `bash -c` from shipped scripts** — `health-check.sh` now calls make targets directly.
- **Added confirmation prompts** before `rm -rf` in dev scripts (`convert-claude-sessions.sh`, `generate-stress-fixtures.sh`).
- **`convert-claude-sessions.sh` requires explicit input directory** — no longer defaults to `$HOME/.claude/projects`.
- **Temp files use `mktemp` + `trap` cleanup** — no more hardcoded `/tmp` paths without cleanup.

## [0.11.2] — 2026-03-17

### Fixed
- **Silent stderr noise on malformed JSONL** — `diagnose.sh` now suppresses `jq: parse error` messages when processing files with truncated or invalid JSON lines. All 19 process substitutions now include `2>/dev/null` on the inner `jq -s` call. Exit code remains 0 and output remains `[]` — behaviour unchanged, output now clean.

## [0.11.1] — 2026-03-16

### Added
- **`make demo`** — generates a synthetic broken session with 6 failure patterns and runs the full diagnostic pipeline, so new users can try clawdoc immediately without real session data
- **`scripts/generate-demo.sh`** — standalone demo generator with `--json-only` mode for piping raw JSONL
- **False positive/negative documentation** in README — every detector's known blind spots, with tuning guidance
- **Compaction threshold edge-case fixture** (`38-compaction-edge-35pct.jsonl`) — tests 35% drop below 40% threshold
- **File size guard** in `diagnose.sh` — warns on files >100MB (configurable via `CLAWDOC_MAX_FILE_SIZE`)
- `bc` declared as required dependency in `check-deps.sh`, `README.md`, and `SKILL.md`
- `check-deps.sh` added to `make lint` target

### Fixed
- **Version bumped to 0.11.1** across VERSION file and all 7 scripts (was stale at 0.9.0)
- **Stale detector counts** — diagnose.sh header, SKILL.md description, and pattern table now say 14 (was 11/12)
- **SKILL.md missing patterns 13+14** — unbounded walk and tool misuse now in pattern reference table
- **SKILL.md missing `version:` field** in frontmatter — now present
- **Critical vs High severity visual collapse** — prescribe.sh and headline.sh now use 🔴 for critical, 🟠 for high (was both 🔴)
- **headline.sh brief mode** now says "alert(s)" instead of "warning(s)" for critical+high findings
- **Demo temp file race condition** — removed EXIT trap so `--json-only` output file persists for follow-up commands
- **CONTRIBUTING.md** test count updated from 35 to 56
- Updated README: detection table now covers all 14 patterns, `bc` in requirements

---

## [0.11.0] — 2026-03-16

### Added
- **Pattern 14: Tool misuse detection** — two sub-detectors:
  - Redundant file reads: flags when the same file is read 3+ times without an intervening write/edit to that file
  - Duplicate searches: flags when the same Glob/Grep query is executed 3+ times with identical parameters
- 3 new test fixtures: `35-tool-misuse.jsonl`, `36-tool-misuse-negative.jsonl`, `37-tool-misuse-edge.jsonl`
- 3 new test assertions (56 total tests)

---

## [0.10.0] — 2026-03-16

### Added
- **Pattern 13: Unbounded walk detection** — two sub-detectors:
  - Recursive command spam: flags 3+ `exec` calls with unscoped recursive commands (`find /`, `grep -r /`, `ls -R`, `tree`) without scope limiters (`-maxdepth`, `| head`)
  - Exponential output growth: flags when toolResult text length doubles 3+ consecutive times
- 3 new test fixtures: `32-unbounded-walk.jsonl`, `33-unbounded-walk-negative.jsonl`, `34-unbounded-walk-edge.jsonl`
- 3 new test assertions (53 total tests)

## [0.9.1] — 2026-03-16

### Added
- **12 edge-case test fixtures** (fixtures 20-31) — one per detector, each sitting just below the detection threshold to verify boundary behavior:
  - P1: 4 retries (threshold: 5), P2: 1 non-retryable error (threshold: 2), P3: tool names in text but not matching pattern, P4: 69% context (threshold: 70%), P5: 2 subagent replays (threshold: 3), P6: $0.49 max turn cost (threshold: $0.50), P7: test failures not matching skill-miss, P8: cron with cheap model, P9: cron with <2x token growth, P10: compaction with no repeated tools, P11: 14% workspace overhead (threshold: 15%), P12: same dirs post-compaction + 9 reads (threshold: 10)
- 12 new test assertions in `test-detection.sh` (50 total tests)

---

## [0.9.0] — 2026-03-14

### Added
- **Pattern 12: Task drift detection** — two sub-detectors:
  - Post-compaction directory divergence: flags when agent drifts to entirely new directories after context compaction (threshold: 3+ calls to new dirs comprising >50% of post-compaction activity)
  - Exploration spiral: flags when agent makes 10+ consecutive read/search tool calls without any edits
- 3 new test fixtures: `17-task-drift-compaction.jsonl`, `18-task-drift-exploration.jsonl`, `19-task-drift-negative.jsonl`
- 3 new test assertions (38 total tests)
- **Configurable cost spike thresholds** via environment variables:
  - `CLAWDOC_COST_TURN_HIGH` (default: 0.50) — per-turn cost for high severity
  - `CLAWDOC_COST_TURN_CRITICAL` (default: 1.00) — per-turn cost for critical severity
  - `CLAWDOC_COST_SESSION` (default: 1.00) — total session cost threshold
  - Raise these for Opus-class models where normal turns cost more

### Fixed
- **SIGPIPE crash** on session metadata extraction — `head -1` under `set -o pipefail` caused silent failures on some JSONL files; replaced with `read` builtin
- **Headline path leaking** — `headline.sh` now strips absolute paths (`/Users/name/...` → `~/...`) from evidence in headline output to avoid leaking filesystem info in shared Slack channels

### Improved
- **Contextual prescriptions** — all 12 detectors now produce prescriptions that reference the specific tool, turn, file, cost, and error from the diagnosis instead of generic advice
- **Richer evidence** — diagnoses now include turn ranges, error messages between retries, token growth trajectories, and narrative explanations of what happened

---

## [0.1.0] — 2026-03-13

Initial release.

### Added
- **11 pattern detectors** covering every major failure mode in OpenClaw sessions:
  - Pattern 1: Infinite retry loop (same tool called 5+ times consecutively)
  - Pattern 2: Non-retryable error retried (validation error → identical retry)
  - Pattern 3: Tool calls emitted as plain text (model/provider compatibility failure)
  - Pattern 4: Context window exhaustion (inputTokens > 70% of context limit)
  - Pattern 5: Sub-agent replay storm (duplicate completions delivered to parent)
  - Pattern 6: Cost spike attribution (turn > $0.50 or session cost unusually high)
  - Pattern 7: Skill selection miss ("command not found" after skill activation)
  - Pattern 8: Model routing waste (premium model on cron/heartbeat sessions)
  - Pattern 9: Cron context accumulation (session cost grows across sequential runs)
  - Pattern 10: Compaction damage (post-compaction tool call repetition)
  - Pattern 11: Workspace token overhead (baseline > 15% of context window)
- **6 shell scripts**: `examine.sh`, `diagnose.sh`, `cost-waterfall.sh`, `headline.sh`, `prescribe.sh`, `history.sh`
- **Tweetable headline output** with recoverable waste percentage
- **Brief mode** (`--brief`) for daily brief cron integration
- **self-improving-agent integration**: writes findings to `.learnings/LEARNINGS.md` with recurrence tracking and idempotent updates
- **Cross-session recurrence tracking** via `history.sh` with promotion suggestions at 3+ occurrences across 2+ sessions
- **13 synthetic test fixtures** covering all patterns plus multi-pattern and edge cases
- **35-test suite**: detection assertions, edge cases (empty session, malformed JSONL, single-turn), unit tests for all scripts, integration pipeline test
- **SKILL.md** for OpenClaw agent integration (`/clawdoc` slash command)
- `install.sh`, `check-deps.sh`, `Makefile`
- `--help` and `--version` on all 6 scripts
- Dependency checks on all scripts

---

## Future

See section 11 of `clawdoc-spec-v2.md` for planned extensions (plugin mode, OTEL integration, Canvas dashboard, auto-remediation).
