---
name: "Deep Research for OpenClaw"
description: "Install and wire a structured OpenClaw deep-research sub-agent with hybrid search, artifact-based runs, claim verification, report linting, and validated finalization."
version: "0.1.1"
metadata:
  openclaw:
    homepage: "https://github.com/MilleniumGenAI/deep-research-openclaw-agent"
    requires:
      bins:
        - openclaw
        - python
      config:
        - openclaw.json
        - deep-researcher agent configured in OpenClaw
        - Tavily API key configured if Tavily-backed scouting is desired
---

# Deep Research for OpenClaw

## What this skill is
This is an integration skill for installing and wiring the `deep-researcher` OpenClaw sub-agent from the public repository:

- [deep-research-openclaw-agent](https://github.com/MilleniumGenAI/deep-research-openclaw-agent)

The repository contains:
- the `workspace-researcher` prompt pack;
- the local research helper scripts;
- the Main -> Deep Research orchestration contract;
- the report lint, validation, and finalization pipeline.

This skill is intended for OpenClaw users who want a reproducible deep-research workflow without assembling the runtime and contracts from scratch.

## What it can do
- structured deep research through `plan -> scout -> harvest -> verify -> synthesize`;
- hybrid discovery with `web_search`, Tavily, and `web_fetch`;
- explicit source registry, claim ledger, and coverage tracking;
- report linting, validation, and final M2M JSON finalization;
- honest `SUCCESS | PARTIAL | FAILURE` delivery with explicit gaps and conflicts.

## Requirements
- OpenClaw `2026.3.x` or later
- Python available on the host
- a configured `deep-researcher` agent in OpenClaw
- Tavily API access if you want the Tavily-backed path

## Install
1. Clone the repository:
   - `git clone https://github.com/MilleniumGenAI/deep-research-openclaw-agent.git`
2. Copy `openclaw/workspace-researcher/` into your OpenClaw base directory, or point your agent config at that path directly.
3. Align the main-agent handoff with:
   - `openclaw/main-deep-research-skill.md`
4. Register or update the `deep-researcher` agent in `openclaw.json`.
5. If you want Tavily-backed scouting, ensure `TAVILY_API_KEY` is available in env or `.env`.

## Validate
Run these checks before using the agent in real work:

```bash
python -m py_compile openclaw/workspace-researcher/scripts/*.py
python openclaw/workspace-researcher/scripts/init_research_run.py --workspace openclaw/workspace-researcher --topic "Smoke test" --language en --task-date 2026-03-10
```

Then run a first smoke task through OpenClaw once the agent is wired:

```bash
openclaw agent --agent deep-researcher --json --message "Perform deep research using your local SOUL.md contract. GOAL: confirm the runtime can initialize a fresh run and return PARTIAL if no external research is performed. SCOPE: in scope is only local init and artifact creation; out of scope is web research. SUCCESS CRITERIA: create fresh tmp artifacts and explain blocked evidence collection honestly. TASK DATE: 2026-03-10. DELIVERABLES: finalized M2M JSON. LANGUAGE: en. CONSTRAINTS: do not fabricate sources; return PARTIAL if evidence is insufficient."
```

## Core references
- Root README: [README.md](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/README.md)
- Sub-agent contract: [openclaw/workspace-researcher/SOUL.md](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/workspace-researcher/SOUL.md)
- Main handoff contract: [openclaw/main-deep-research-skill.md](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/main-deep-research-skill.md)
- Runtime scripts: [openclaw/workspace-researcher/scripts/](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/tree/main/openclaw/workspace-researcher/scripts)
- Agent config template: [openclaw/agent-config.template.json](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/agent-config.template.json)
- Known limits: [docs/known-limits.md](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/docs/known-limits.md)

## Notes
- This is an OpenClaw-only v1 package.
- ClawHub publishes skills under platform-wide MIT-0 terms.
- The runtime source of truth is `openclaw/workspace-researcher/SOUL.md`.
- Findings should be built only from traceable external sources, not from local artifacts.
