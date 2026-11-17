---
name: agentscope-doc-generator
description: Generate documentation for AgentScope 2.0 agents, pipelines, and skills from code and config files. Use this when the user wants README scaffolding, agent capability docs, or project documentation from existing AgentScope code.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - python3
    primaryEnv: ""
    envVars: []
    emoji: "📝"
    homepage: https://github.com/agentscope-ai/agentscope
---

# AgentScope Doc Generator

This skill generates documentation artifacts from AgentScope 2.0 project files. It focuses on:

- README scaffolding for skills/plugins
- Agent capability summaries from config
- Pipeline documentation from workflow definitions

## What this skill does

- Inspects AgentScope project structure
- Generates README templates
- Creates agent capability tables
- Produces usage examples from configs

## How to use

Run the generator script from this skill folder:

```bash
python3 scripts/generate_docs.py --project /path/to/agentscope/project --output /tmp/docs
```

Supported sources:

- `agent.json` / `config.json`
- `skills/*/SKILL.md`
- `run.py` / pipeline definitions

## Security notes

- Generated docs are based on local project files only
- No secrets are extracted or emitted
- Review generated content before publishing

## Troubleshooting

- If no project is detected, pass `--project` explicitly
- For skill docs, ensure `SKILL.md` frontmatter is valid YAML
