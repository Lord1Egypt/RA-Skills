# 🩻 clawdoc

Diagnose AI agent sessions. Find failures. Prescribe fixes.

[![CI](https://github.com/openclaw/clawdoc/actions/workflows/ci.yml/badge.svg)](https://github.com/openclaw/clawdoc/actions/workflows/ci.yml)

clawdoc detects 14 common failure patterns in AI agent sessions — retry loops, context exhaustion, cost spikes, task drift, and more. It works with **any agent** that produces JSONL session logs, and ships with first-class [OpenClaw](https://github.com/openclaw) integration.

## Quick start

**Try it instantly** — no agent sessions required:
```bash
git clone https://github.com/openclaw/clawdoc.git && cd clawdoc
make demo
```
This generates a synthetic broken session with 6 failure patterns and runs the full diagnostic pipeline.

**Diagnose any JSONL session file**:
```bash
bash scripts/diagnose.sh session.jsonl | bash scripts/prescribe.sh
```

**Per-turn cost breakdown**:
```bash
bash scripts/cost-waterfall.sh session.jsonl | jq '.[0:5]'
```

### OpenClaw integration

If you use [OpenClaw](https://github.com/openclaw), clawdoc also installs as a skill with slash commands and natural language triggers:

```bash
# Install as an OpenClaw skill
clawhub install clawdoc
# Or manually:
bash install.sh
```

```
/clawdoc              → headline health check
/clawdoc full         → complete diagnosis with prescriptions
/clawdoc brief        → one-liner for daily brief crons
```

Natural language also works: *"What went wrong?"*, *"Why was that so expensive?"*, *"Give me a full diagnosis"*

OpenClaw sessions live at `~/.openclaw/agents/<agentId>/sessions/`. For multi-session health checks:
```bash
bash scripts/headline.sh ~/.openclaw/agents/main/sessions/
bash scripts/history.sh ~/.openclaw/agents/main/sessions/
```

### Using with other agent frameworks

clawdoc works with any JSONL file that follows this structure:

```json
{"type":"session","sessionId":"...","model":"...","sessionKey":"..."}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","name":"read","input":{"path":"src/main.ts"}}],"usage":{"inputTokens":5000,"outputTokens":30,"cost":{"total":0.01}}}}
{"type":"message","message":{"role":"toolResult","content":[{"type":"text","text":"file contents..."}]}}
```

The required fields per message are:
- `type`: `"session"` (first line) or `"message"` (all others)
- `message.role`: `"assistant"`, `"user"`, or `"toolResult"`
- `message.content[]`: array of `{"type":"text","text":"..."}` and/or `{"type":"toolCall","name":"...","input":{...}}`
- `message.usage`: `{inputTokens, outputTokens, cost: {total}}` (on assistant messages)

Optional fields that enable specific detectors:
- `sessionKey`: enables P5 (sub-agent replay, needs `"subagent:"` prefix), P8 (model routing waste, needs `"cron:"` prefix), P9 (cron accumulation, needs `"cron:"` prefix)
- `message.usage.contextTokens`: enables accurate P4 (context exhaustion) threshold; defaults to 128K if absent

If your agent framework uses a different log format, a small adapter script can convert it. The `dev/convert-claude-sessions.sh` script is an example for Claude Code sessions.

## Example output

```
🩻 clawdoc — 3 findings across 12 sessions (last 7 days)
💸 $47.20 spent — $31.60 was waste (67% recoverable)
🔴 Retry loop on exec burned $18.40 in one session
🟡 Opus running 34 heartbeats ($8.20 → $0.12 on Haiku)
🟡 SOUL.md is 9,200 tokens — 14% of your context window
```

## What it detects

| # | Pattern | Severity | What it catches |
|---|---------|----------|----------------|
| 1 | Infinite retry loop | 🔴 Critical | Same tool called 5+ times consecutively, burning tokens |
| 2 | Non-retryable error retried | 🔴 High | Validation errors re-attempted endlessly |
| 3 | Tool calls as plain text | 🔴 High | Model/provider mismatch — commands not executing |
| 4 | Context window exhaustion | 🟡-🔴 | Tokens approaching limit, session grinding to halt |
| 5 | Sub-agent replay storm | 🟡 Medium | Completion delivered 70+ times to parent |
| 6 | Cost spike attribution | 🟡-🔴 | Per-turn cost waterfall showing where money went |
| 7 | Skill selection miss | 🟢 Low | Required binary not installed |
| 8 | Model routing waste | 🟡 Medium | Opus running heartbeats that Haiku could handle |
| 9 | Cron context accumulation | 🟡 Medium | Cron jobs getting more expensive every run |
| 10 | Compaction damage | 🟡 Medium | Agent forgot context after auto-compaction |
| 11 | Workspace token overhead | 🟡 Medium | Context budget consumed before conversation starts |
| 12 | Task drift | 🟡 Medium | Agent drifts to unrelated work after compaction, or spirals reading without editing |
| 13 | Unbounded walk | 🔴 High | Repeated unscoped `find /`, `grep -r /` flooding output |
| 14 | Tool misuse | 🟡 Medium | Same file read 3+ times without edit, or identical search repeated |

## Known false positives and false negatives

clawdoc prefers false negatives over false positives — it won't flag something unless it's fairly confident. This section documents the edge cases where each detector can get it wrong, so you know when to trust a finding and when to investigate further.

### False positives (flagged but not a real problem)

| Pattern | When it over-fires | Why it happens |
|---------|-------------------|----------------|
| P1 — Infinite retry | Agent intentionally polls a long-running process (e.g., CI status check every 30s) | The detector sees 5+ identical `exec` calls and can't distinguish polling from stuck retries. Workaround: vary the input slightly or add a status message between polls. |
| P2 — Non-retryable retry | Tool error text coincidentally matches validation keywords (`TypeError`, `invalid`) but the error is actually transient | The detector regex-matches error strings — a transient network error containing "invalid certificate" would match. |
| P4 — Context exhaustion | Legitimately large sessions that need the full context window (e.g., whole-codebase refactors) | Any session reaching 70%+ of the context window is flagged, even when hitting that limit is expected. |
| P6 — Cost spike | First turn after loading a large project with many workspace files | Expensive first turns are normal for projects with large `CLAUDE.md`, `AGENTS.md`, or many SOUL files — the cost reflects loading, not waste. |
| P8 — Model routing waste | Cron job intentionally using Opus/Sonnet because the task genuinely requires reasoning | The detector flags any expensive model on a `cron:` session key, regardless of task complexity. |
| P11 — Workspace overhead | Projects that legitimately need large system prompts (complex AGENTS.md, many tool definitions) | Anything over 15% of context at first turn is flagged — some projects need that configuration space. |
| P12 — Task drift (exploration) | Legitimate research phases where reading 10+ files before writing is the correct approach | The detector counts consecutive read-only tool calls and can't judge whether the reading is purposeful or aimless. |
| P13 — Unbounded walk | Agent running `find` on a known small directory without `-maxdepth` (safe in practice) | The detector doesn't evaluate directory size — `find ./small-dir -name '*.ts'` is flagged the same as `find / -name '*.ts'`. |
| P14 — Tool misuse | Agent re-reads a file after a long gap because it was compacted out of context | Reads of the same file after compaction are necessary — the content is no longer in context — but the detector counts them as redundant. |

### False negatives (real problem but not detected)

| Pattern | What it misses | Why it misses |
|---------|---------------|---------------|
| P1 — Infinite retry | Retries with slightly different input (e.g., appending a space or changing a flag) | The detector requires identical `name + input` — minor input variations create a new "run" and reset the counter. |
| P2 — Non-retryable retry | Non-retryable errors that don't match the regex (custom error formats, non-English errors) | Only matches `Missing required parameter`, `TypeError`, `ValidationError`, and `invalid.*parameter`. Errors outside this list are invisible. |
| P3 — Tool as text | Tool names written in the middle of a sentence, not at the start of a line | The regex requires `^toolname\s+` at line start — `"I'll now read the file"` doesn't match even though `read` was never executed. |
| P5 — Sub-agent replay | Replay storms in sessions without a `subagent:` session key pattern | Only runs when `sessionKey` matches `agent:*:subagent:*` — identical message replay in a main session is not checked. |
| P6 — Cost spike | Gradually expensive sessions where no single turn is expensive but total cost is high and below the $1.00 session threshold | The per-turn threshold ($0.50) and session threshold ($1.00) can both be missed by sessions that are moderately expensive across many turns. Adjust with `CLAWDOC_COST_TURN_HIGH` and `CLAWDOC_COST_SESSION` env vars. |
| P9 — Cron accumulation | Non-monotonic token growth (e.g., grows, dips, grows again) | The detector requires strictly monotonic growth — any dip in token count between turns causes it to exit early. |
| P10 — Compaction damage | Agent repeats work using *different* tool calls than before compaction (same goal, different approach) | The detector matches exact `name + input` pairs — if the agent re-does work with a different tool or different arguments, it's invisible. |
| P12 — Task drift (compaction) | Drift to new directories when the pre-compaction baseline had no file operations | If the agent had no file path operations before compaction, there's no baseline to compare against — drift detection is skipped. |
| P13 — Unbounded walk | Recursive operations via non-exec tools (e.g., Glob with `**/*` pattern, or a custom script that internally runs `find`) | Only checks `exec` tool calls — other tools performing recursive operations aren't inspected. |
| P14 — Tool misuse | Re-reading a file that was changed externally (by another process or a git operation) between reads | The detector only tracks clawdoc-visible writes (write/edit tool calls) — external changes are invisible, so the re-read looks redundant when it isn't. |

### Tuning thresholds

Most thresholds are calibrated for Sonnet-class models. If you run Opus (where normal turn costs are higher) or Haiku (where costs are lower), adjust via environment variables:

```bash
# Cost spike thresholds (raise for Opus, lower for Haiku)
export CLAWDOC_COST_TURN_CRITICAL=2.00  # default: 1.00
export CLAWDOC_COST_TURN_HIGH=1.00      # default: 0.50
export CLAWDOC_COST_SESSION=3.00        # default: 1.00
```

Other thresholds are currently hardcoded in `diagnose.sh`. See `CONTRIBUTING.md` for how to propose threshold changes.

## Daily Brief integration

Add to your morning cron prompt:
```
Run /clawdoc brief and include the result in today's daily brief.
```

Output: `Yesterday: 8 sessions, $3.40, 1 warning (cron context growth on daily-report)`

## Requirements

- `bash` 3.2+ (macOS system bash works; bash 5.x recommended)
- `jq` 1.6+
- `bc` (for floating-point arithmetic in detectors)
- Standard POSIX tools: `awk`, `sed`, `grep`, `sort`, `uniq`, `wc`
- OpenClaw (optional — only needed for slash command and skill integration)

Verify with: `bash scripts/check-deps.sh`

## How it works

clawdoc reads JSONL session files, runs 14 pattern detectors implemented in bash + jq, and outputs structured JSON findings. Pipe the findings through `prescribe.sh` for a formatted markdown report with actionable prescriptions. No data leaves your machine. No API keys. No network calls.

When installed as an OpenClaw skill, your agent reads SKILL.md and can invoke clawdoc via `/clawdoc` or natural language. But the scripts work standalone — point them at any JSONL session file.

## Testing

```bash
make demo       # generate a broken session and diagnose it — try clawdoc instantly
make test       # runs 57 tests: detection, edge cases, unit, integration
make lint       # shellcheck all scripts (requires: brew install shellcheck)
make check-deps # verify jq, bash, awk are present
```

## Works with

- **Any JSONL agent logs**: Point `diagnose.sh` at any file matching the session format above
- **OpenClaw ecosystem**: First-class integration as a skill with slash commands, natural language triggers, and session directory conventions
- **ClawMetry** (OpenClaw): ClawMetry shows what happened. clawdoc explains why and how to fix it.
- **self-improving-agent** (OpenClaw): Writes findings to `.learnings/LEARNINGS.md` with idempotent recurrence tracking
- **SecureClaw** (OpenClaw): clawdoc handles behavioral and cost issues. SecureClaw handles security.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add pattern detectors, design principles, threshold rationale, and the PR process.

## License

MIT — see [LICENSE](LICENSE).
