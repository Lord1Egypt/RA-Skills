# Runtime Adapters

This capability is intentionally portable. The canonical interface is:

- `SKILL.md` for agent instructions
- `capability.json` for machine-readable metadata
- `scripts/recommend_traces.py` for deterministic recommendations
- `references/trace_schema.md` for trace data contracts

## Codex

Install the whole `agent-experience-graph` directory under:

```text
$CODEX_HOME/skills/agent-experience-graph
```

Codex can use `SKILL.md` directly. `agents/openai.yaml` adds UI metadata.

## Claude Code

Install the whole directory under a project or user skill path:

```text
.claude/skills/agent-experience-graph
~/.claude/skills/agent-experience-graph
```

Claude Code can use `SKILL.md` and the bundled files directly.

## OpenClaw

Install the whole directory under a workspace or shared skills root, such as:

```text
~/.openclaw/skills/agent-experience-graph
```

OpenClaw can use `SKILL.md` as the skill instruction pack.

## Hermes Or Other Agents

If the runtime supports `SKILL.md`, install the directory as-is. If it uses another prompt format, load `SKILL.md` as the instruction text and expose:

```text
python3 scripts/recommend_traces.py
```

as a callable helper. The only hard requirement is Python 3.9+ and a readable JSON trace library.
