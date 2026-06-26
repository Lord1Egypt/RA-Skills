---
name: gh-skillforge
description: "Generate valid, ClawHub-ready SKILL.md files from product metadata. Give it a name, description, and instructions — get back a properly formatted SKILL.md with YAML frontmatter, slug normalization, and optional env/bins declarations."
metadata: {"openclaw":{"emoji":"🔨","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic","pyyaml"]}]}}
---

# SkillForge

Generate a SKILL.md ready to publish on ClawHub.

## Start the server

```bash
uvicorn skillforge.app:app --port 8003
```

## Generate a SKILL.md

```bash
curl -s -X POST http://localhost:8003/v1/forge-skill \
  -H "Content-Type: application/json" \
  -d '{"name": "My Cool Tool", "description": "Does cool things.", "instructions": "Step 1: Be cool."}' | jq
```

Returns `skill_md` (the complete SKILL.md content) and `slug` (ClawHub-compatible name like `my-cool-tool`).

## With optional env vars and bins

```bash
curl -s -X POST http://localhost:8003/v1/forge-skill \
  -H "Content-Type: application/json" \
  -d '{"name": "API Client", "description": "Calls APIs.", "instructions": "Use curl.", "env_vars": ["API_KEY"], "bins": ["curl"]}' | jq '.skill_md' -r
```

## Slug rules

Names are auto-converted to ClawHub slugs: lowercase, spaces to dashes, special chars removed. `"My Tool v2!"` becomes `my-tool-v2`.
