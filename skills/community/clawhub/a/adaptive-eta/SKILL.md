---
name: adaptive-eta
description: Give the user an honest time estimate before long-running work, re-estimate when it runs over, and ask before blowing far past it. Use for multi-step tasks expected to take more than ~2 minutes or 4+ tool calls — research, batch file processing, builds, migrations, multi-file edits, data analysis. Skip for quick answers and single-step edits. 长任务时间预估：预计超过约 2 分钟或需 4 次以上工具调用的多步任务，先报预估时间，超时主动更新，严重超时先征得同意。
---

# Adaptive ETA

Never leave the user waiting in silence. Promise a time, track it with a real clock, correct it honestly, and learn from the gap.

You cannot feel time passing between tool calls — the script is your clock. Trust its numbers over your sense of progress.

## When to activate

| Expected duration | What to do |
|---|---|
| < 30s, or a direct answer | Nothing. Just do it. |
| 30s – 2 min | One line up front ("About a minute."). No timer. |
| > 2 min, or ≥ 4 tool calls | Full protocol below. |

When unsure, lean toward the lighter tier. An ETA on a trivial task is noise.

## Script

`scripts/timer.py` sits next to this file. Call it by **absolute path** (resolve this skill's directory once), e.g. `python3 <skill-dir>/scripts/timer.py check`. State is stored in `~/.adaptive-eta/` (override with `ADAPTIVE_ETA_HOME`); add `--task <id>` only if you run parallel timers.

| Command | When |
|---|---|
| `start --eta <sec> --label "<what>"` | Right after estimating, before the first real step |
| `check` | At each step boundary (see below) |
| `revise --eta <remaining sec> --reason "<why>"` | After telling the user a new estimate. Keeps the original ETA for the 3× rule |
| `stop` (or `stop --outcome aborted`) | When the work ends, before the final report |
| `calibrate` | Optional; shows how accurate past estimates were |

## Protocol

**1. Estimate.** Break the task into 3–5 steps, estimate each, sum, add ~20% buffer. Run `start`. If it prints a `CALIBRATION` line, your past estimates were off — use its suggested figure and run the `revise` it shows.

**2. Announce.** One or two lines, in the user's language: total time and the steps. Round honestly; a range is fine.
> About 5 minutes: read the 12 files (~1 min), draft the changes (~3 min), run tests (~1 min).

**3. Check at step boundaries — not around every tool call.** Run `check` when you finish a planned step, and before starting anything that may block for more than a minute (long builds, big downloads). Act on the status:

| STATUS | Action |
|---|---|
| `ON_TRACK` | Continue. Say nothing. |
| `THRESHOLD_REACHED` | ≥80% of the window used. If nearly done, finish. Otherwise re-estimate, tell the user, `revise`. |
| `EXPIRED` | Tell the user what is slower than expected and the new remaining time, then `revise`. |
| `OVERRUN` | Over 3× the original estimate. Stop and ask: continue, cut scope, or stop? Wait for an answer. |
| `NOT_RUNNING` / `STALE` | No live timer. `start` again if work continues. |

An update names the cause, not just a number:
> Slower than planned — the test suite takes ~4 min per run. About 6 more minutes.

**4. Deliver.** Run `stop`, then add its `REPORT` line in one short line at the end of the result:
> Estimated 5m · actual 7m20s · 1 revision

## Rules

- Report real progress only. Never claim a step is done to stay on schedule.
- At most one update per step unless the status gets worse. Do not narrate the timer.
- If you cannot speak during a single long command, say so before it starts ("the build blocks for ~3 min").
- If the user changes the scope, re-estimate and `revise` — that is not an overrun.
- Always `stop`, including when the task fails or the user cancels (`--outcome aborted`). That keeps calibration honest.
