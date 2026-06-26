# Reference — Cron Job Auditor

## Where cron jobs usually live

- Default path (typical install): `~/.openclaw/cron/jobs.json`
- Schema may include a top-level `version` and a `jobs` array. Confirm against current OpenClaw docs if fields differ.

Always resolve paths from the user’s **OpenClaw home** or **workspace** if they use a non-default layout.

## Payload kinds (conceptual)

| `payload.kind` | Typical LLM use | Notes |
|----------------|-----------------|--------|
| `agentTurn` | **Yes** — full agent run | Highest token cost per execution. |
| Other / shell / hook | **Maybe** — depends on OpenClaw version | Read the job definition; do not assume. |

If unsure, label confidence **low** and say what would need manual inspection.

## Glossary

- **Agent turn**: A scheduled run that invokes the model (tools, reasoning, messaging).
- **Message-only path**: Delivering text via `openclaw message send` (or equivalent) **without** an agent turn for the delivery step.
- **OS timer**: systemd user `.timer`, macOS `launchd`, or another scheduler **outside** OpenClaw Gateway cron.
- **Script candidate**: A job that *might* be replaced by a timer + script, subject to human verification.

## Heuristic confidence

- **High**: Payload clearly requires only deterministic steps you could script (fetch URL, run CLI, format fixed template) **and** the user confirms no reasoning is needed.
- **Medium**: Likely automatable but prompt mentions summarization, filtering “what matters,” or tool choice — may still need an LLM sometimes.
- **Low**: Explicit research, multi-step judgment, or evolving instructions — keep as agent cron or redesign scope.

## Verification checklist (after user migrates manually)

1. Old Gateway cron job **disabled** or **removed** (avoid duplicate sends).
2. New timer fires at the intended time (check `systemctl --user list-timers` or equivalent).
3. Test run: script exits 0; notification received once.
4. No unexpected duplicate messages (compare with previous behaviour).

## Anti-patterns

- Promising token savings without seeing actual prompts or runtime.
- Editing `jobs.json` or system config **on behalf of the user** without explicit instruction (out of scope for this skill).
- Treating every `agentTurn` as replaceable — most are not 1:1 with a dumb script.
