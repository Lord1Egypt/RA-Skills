# 10 Meta-Principles of Harness Engineering

Distilled from [Harness Engineering](https://github.com/wquguru/harness-books) and [Claude Code v2.1.88 source analysis](https://github.com/openedclaude/claude-reviews-claude).

---

## M1: Determinism over Persuasion

System mechanisms (hooks, denials, circuit breakers) take precedence over prompt instructions. Prompts are probabilistic — a prompt saying "don't retry more than 3 times" will be ignored under pressure. A PostToolUseFailure hook that counts failures and blocks at 5 is deterministic.

## M2: Filesystem as the Coordination Medium

All inter-agent, inter-session, and inter-hook communication goes through disk files. No in-memory state, no custom IPC. JSON files + atomic writes (write-to-temp-then-rename) + one directory per session.

## M3: Safety Valves on Every Enforcement Loop

Any mechanism that blocks agent progress MUST have escape conditions. Minimum set: authentication failure (401/403), explicit cancel signal, idle timeout, iteration cap.

## M4: Session-Scoped Isolation

State from one session MUST NOT leak into another. Each session gets its own directory. Cross-session transfer only through explicit mechanisms (handoff documents, memory consolidation gates).

## M5: Fail-Open on Uncertainty

When harness state is ambiguous (file missing, JSON parse error), default to ALLOWING the agent to proceed. Exception: safety-critical contexts flip to fail-closed.

## M6: Proportional Intervention

Match harness intensity to task complexity. A 5-minute typo fix needs no hooks; a 2-hour multi-file refactor needs all of them.

## M7: Observe Before Intervening

Measurement patterns (tool error tracking, bracket metrics, context estimation) are prerequisites for intervention patterns (tool error blocking, Ralph loop, budget injection).

## M8: Explicit Knowledge Transfer

Write decisions to disk in structured formats that survive compaction. Don't rely on LLM summary alone. A handoff document written at decision time is ground truth.

## M9: Coordinator Synthesizes, Never Delegates Understanding

"Based on your findings, fix it" is an anti-pattern. The coordinator must digest worker results and convert them into concrete next steps with specific file paths and line numbers.

## M10: Honest Limitation Labeling

When a mechanism cannot be implemented reliably, say so with a "NOT IMPLEMENTED" or "ADVISORY ONLY" label. "Silently broken" is worse than "honestly absent."

---

## Hook Protocol: Multi-Hook Aggregation Rules

When multiple hooks respond to the same event, Claude Code aggregates their outputs:

| Output field | Aggregation rule | Example |
|---|---|---|
| `permissionDecision` | **Most restrictive wins** — any single `deny` overrides all `allow` | Hook A: allow, Hook B: deny → deny |
| `updatedInput` | **Last one wins** — hooks execute in settings.json order | Hook A: adds `--dry-run`, Hook B: adds `--timeout 30` → only `--timeout 30` survives |
| `additionalContext` | **Concatenate** — all hooks' context messages are joined | Hook A: "check deps", Hook B: "watch memory" → agent sees both |

Source: Claude Code source, `utils/hooks.ts` aggregation logic.
