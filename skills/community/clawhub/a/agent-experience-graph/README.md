# Agent Experience Graph

Agent Experience Graph is a portable agent capability for recommending tools, skills, and workflow lessons from prior agent execution traces.

It is intentionally runtime-neutral:

- `SKILL.md` contains the instructions an agent can load directly.
- `capability.json` describes the capability for launchers, registries, and importers.
- `scripts/recommend_traces.py` ranks similar traces and recommends reusable skills/tools.
- `references/trace_schema.md` defines the trace data contract.

## Try It

```bash
python3 scripts/recommend_traces.py \
  --traces assets/example_traces.json \
  --query '{"task":"Build markdown API docs ingestion","subtasks":[{"description":"parse markdown into sections"},{"description":"evaluate endpoint metadata extraction"}]}'
```

## Install

- Codex: copy this directory to `$CODEX_HOME/skills/agent-experience-graph`
- Claude Code: copy this directory to `.claude/skills/agent-experience-graph` or `~/.claude/skills/agent-experience-graph`
- OpenClaw: install from ClawHub with `clawhub install agent-experience-graph`
- Generic agents: load `SKILL.md` as instructions and expose `scripts/recommend_traces.py` as a helper

## Record A Trace

Create a sanitized JSON trace with `id`, `task`, `outcome`, optional `subtasks`, `skills`, `tools`, and `lessons`, then append it:

```bash
python3 scripts/recommend_traces.py \
  --traces traces.json \
  --append-trace new_trace.json
```

Do not include secrets, credentials, private user data, proprietary snippets, or raw customer content in shared traces.

## License

MIT-0.
