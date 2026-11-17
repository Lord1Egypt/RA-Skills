# DecomTangle — atomic tool-call decomposer

An OpenClaw-style agent skill that enforces one discipline: **decompose every
multi-step procedure into atomic tool calls** — one observable action per
call, observe the result between steps.

## The problem it solves

Agents — especially on local/open-weight models — try to do whole procedures
in ONE giant tool call: a full multi-step bash script as a single `command`
argument, with loops, `&&` chains, and quotes nested three deep. These
mega-calls:

- break tool-call parsers (Ollama, LiteLLM/ollama_chat) → opaque HTTP 500s;
- kill agent turns with **no terminal event** — the bot just goes silent;
- execute blind: five decisions collapsed into zero, failures unlocatable;
- leave side-effecting steps in unknowable states.

This is a tool-call **shape** problem, not a model-capability problem. In the
incident that motivated this skill, the same model that stalled on the
mega-script completed the same procedure when each step was its own call.

## The five rules

1. **One tool call = one atomic action.** Never embed a script, loop, or
   multi-step procedure in a single call's args.
2. **Step → observe → step.** Read each result before choosing the next action.
3. **N steps = N calls.** Prefer native tool endpoints over generic scripting.
4. **Side effects are "attempted," not "confirmed,"** until verified in the
   live system.
5. **Complexity tripwire.** Needing nested-quoted multi-line scripting in one
   call means: decompose further.

## What's in the package

| File | What it is |
| --- | --- |
| `SKILL.md` | Operating model: the five rules + working defaults |
| `references/decomposition-heuristics.md` | How to find atomic boundaries; anti-pattern catalog |
| `references/atomic-call-checklist.md` | Six-point pre-flight check per call |
| `examples/bad-mega-script-stall.md` | The real 2026-07-04 silent-stall incident, annotated |
| `examples/good-multicalendar-atomic.md` | The same procedure done right, call by call |
| `SKILL_CARD.md` | NVIDIA skill-card trust format |

## Install

```
clawhub install decomtangle
```

Doctrine-only: declares no tools, no permissions, no env vars. Safe to install
alongside any tool surface. Composes with domain skills (e.g.
`airbnb-gateway`) — they define WHAT to do; DecomTangle governs HOW each step
is emitted.

## Status

v0.1.0 — extracted from a diagnosed production incident and its verified
resolution. See `CHANGELOG.md`.

> ⭐ If this skill saves you a silent stall, please star it on ClawHub — stars
> help other operators find it.

## License

MIT
