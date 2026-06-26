# Beckmann Knowledge Graph × Self-Improving + Proactive Agent

A combination skill that connects two independent skills into a single
workflow — without modifying either one.

## What it does

The **Self-Improving + Proactive Agent** (`ivangdavila/self-improving`) handles
all everyday tasks: it logs corrections, maintains tiered HOT/WARM/COLD memory,
self-reflects after significant work, and runs a heartbeat for recurring
maintenance. This remains the default for every interaction.

The **Beckmann Knowledge Graph** (`matthiasbeckmann987-spec/beckmann-knowledge-graph`)
is a structured reasoning framework for questions that standard knowledge
cannot answer well — paradoxes, open scientific questions, high-complexity
forecasts, and strategic dead ends.

This combination skill defines exactly when the agent should suggest switching
to the Beckmann Knowledge Graph, how Beckmann insights integrate into the
HOT/WARM/COLD memory tiers, and how the heartbeat keeps both systems in sync.

## How it works

When the agent detects a question that matches a Beckmann trigger (paradox,
open scientific question, long-horizon forecast, strategic dead end, AI safety,
or epistemological limit), it **proactively suggests** using the Beckmann
Knowledge Graph — and waits for the user's confirmation before acting.

If the user confirms, the agent first checks HOT memory for a prior Beckmann
insight on the same topic before loading the full graph. After delivering the
answer, it self-reflects and stores the result in the appropriate memory tier.
Graph gaps are logged as `#beckmann-graph-extension-candidate` entries for
the graph author to review. If the user declines, the agent answers with
standard reasoning and keeps the offer open.

## Install

```
openclaw skills install beckmann-x-self-improving-proactive
```

## Requires

- `ivangdavila/self-improving`
- `matthiasbeckmann987-spec/beckmann-knowledge-graph`

## Uninstall

Delete this skill's `SKILL.md`. Both base skills continue working independently.
Memory entries tagged `#beckmann` in `~/self-improving/` remain available to
the Self-Improving + Proactive Agent as standard memory — no data loss.

## License

MIT-0
