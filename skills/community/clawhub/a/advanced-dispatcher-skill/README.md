# Advanced Dispatcher

A strict mid-session routing skill for OpenClaw.

## Purpose

- route work to the best spawned model without changing the fixed main session
- keep routing predictable, cheap, and testable
- prevent accidental Claude usage
- make future updates low-friction

## Routing table

| Task class | Primary model | Cache retention |
|---|---|---|
| Code & architecture | `openai-codex/gpt-5.4` | `long` |
| Math & algorithms | `opencode-go/glm-5` | `short` |
| Web dev & brainstorming | `opencode-go/minimax-m2.5` | `short` |
| Research & long context | `opencode-go/kimi-k2.5` | `short` |
| Quick scripts & formatting | `openai-codex/gpt-5.3-codex-spark` | `long` |

## Tradeoff routing

### Default

Generate proposals in parallel with:
- `opencode-go/glm-5`
- `openai-codex/gpt-5.3-codex`

Judge with:
- `openai-codex/gpt-5.4`

### With `--force-claude`

Use Claude only for proposal generation:
- `anthropic/claude-sonnet-4-6`
- `anthropic/claude-opus-4-6`

Judge remains:
- `openai-codex/gpt-5.4`

## Trigger language

Tradeoff mode should trigger on requests like:
- "evaluate tradeoffs"
- "compare approaches/options/designs/architectures"
- "choose between these solutions"
- "which architecture is better?"

Do not trigger tradeoff mode just because the prompt contains a vague standalone "compare".

## Flag policy

- supported: `--force-claude`
- rejected: `--use-claude`, `--force-opus`, `--no-opus`
- Claude must never appear in a route unless `--force-claude` is present

## Files

- `SKILL.md` — operating instructions, including the judge/simplify contracts (self-contained)
- `dispatcher.py` — deterministic route planner
- `test_dispatcher.py` — unit tests and smoke coverage

## Maintenance

Update routing in these places only:
- `ModelCatalog`
- `_STANDARD_DOMAIN_MODELS`
- `_TRADEOFF_PATTERNS`

Keep tests aligned with every routing change.

## Test commands

```bash
python3 -m unittest /root/.openclaw/workspace/skills/advanced-dispatcher/test_dispatcher.py -v
python3 /root/.openclaw/workspace/skills/advanced-dispatcher/test_dispatcher.py
```
