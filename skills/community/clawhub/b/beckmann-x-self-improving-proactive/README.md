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
answer, the agent asks for explicit consent before storing the insight in a
quarantine location. Promotion to HOT/WARM memory only happens after further
user confirmation. Graph gaps are logged as `#beckmann-graph-extension-candidate`
entries (also only after consent). If the user declines the initial escalation,
the agent answers with standard reasoning and keeps the offer open.


## Install

```
openclaw skills install beckmann-x-self-improving-proactive
```

## Requires

- `ivangdavila/self-improving@1.2.16`
- `matthiasbeckmann987-spec/beckmann-knowledge-graph@3.1.0`

(Exact versions and integrity hashes are documented in the skill’s `SKILL.md`.)


## Uninstall

Two modes are available:

### Soft uninstall (default)
1. Delete this skill’s `SKILL.md`.
2. Both base skills (`ivangdavila/self-improving` and `matthiasbeckmann987-spec/beckmann-knowledge-graph`) continue working independently.
3. Memory entries tagged `#beckmann` (including any quarantine files) remain available to the Self-Improving + Proactive Agent as standard memory — no data loss.

### Clean uninstall (optional, recommended for security-conscious users)
1. Delete this skill’s `SKILL.md`.
2. List every file and entry tagged `#beckmann` or located in `~/self-improving/quarantine/` that was created by this skill.
3. Ask the user to confirm deletion or archival of the selected entries.
4. After confirmation, remove or archive the chosen items.
5. Both base skills continue working independently.

Always present both options and let the user decide.

## License

MIT-0
