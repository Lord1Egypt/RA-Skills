# Beckmann Knowledge Graph × Self-Improving Agent

A combination skill that connects two independent skills into a single
workflow — without modifying either one.

## What it does

The **Self-Improving Agent** (`pskoett/self-improving-agent`) handles all
everyday tasks: it logs errors, captures learnings, and improves over time.
This remains the default for every interaction.

The **Beckmann Knowledge Graph** (`matthiasbeckmann987-spec/beckmann-knowledge-graph`)
is a structured reasoning framework for questions that standard knowledge
cannot answer well — paradoxes, open scientific questions, high-complexity
forecasts, and strategic dead ends.

This combination skill defines exactly when the agent should suggest switching
to the Beckmann Knowledge Graph, and how the results flow back into the
Self-Improving Agent's learning memory.

## How it works

When the agent detects a question that matches a Beckmann trigger (paradox,
open scientific question, long-horizon forecast, strategic dead end, AI safety,
or epistemological limit), it **proactively suggests** using the Beckmann
Knowledge Graph — and waits for the user's confirmation before acting.

If the user confirms, the agent applies the full 6-step Beckmann protocol and
logs the insight back into the Self-Improving Agent's learning log with a
`#beckmann` tag. If the user declines, the agent answers with standard
reasoning and keeps the offer open.

## Install

```
openclaw skills install beckmann-x-self-improving-agent
```

## Requires

- `pskoett/self-improving-agent`
- `matthiasbeckmann987-spec/beckmann-knowledge-graph`

## Uninstall

Delete this skill's `SKILL.md`. Both base skills continue working independently.
No data in `.learnings/` is affected.

## License

MIT-0
