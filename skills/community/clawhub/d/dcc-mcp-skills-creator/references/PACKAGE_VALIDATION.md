## Quick Start

### Create a new skill

```python
# Call the loaded MCP tool:
# dcc_mcp_skills_creator__create_skill(
#     name="maya-rigging",
#     parent_dir="/path/to/skills/dir",
#     dcc="maya",
#     tool_name="create_locator",
#     affinity="main",
# )
```

### Validate an existing skill

```bash
dcc-mcp-cli lint /path/to/my-skill
```

The CLI loads the sibling `tools.yaml` table and invokes every declaration
through Core's real router with deterministic mock handlers. CI fails if a
sync declaration produces a job envelope or an async declaration produces a
direct result. Adapter/DCC code is never imported or executed by this probe.

### Get a SKILL.md template

```python
# Call the loaded MCP tool:
# dcc_mcp_skills_creator__skill_template()
```

## Skill Directory Structure

```
my-skill/
|-- SKILL.md              # Required: metadata frontmatter + instructions
|-- tools.yaml            # Required when metadata.dcc-mcp.tools points here
|-- scripts/              # Optional: tool implementation scripts
|   `-- create_locator.py
`-- references/           # Optional: recipes, examples, and long-form docs
    |-- RECIPES.md
    `-- NOTES.md
```

## Validation Rules

The validator checks:

- **SKILL.md** exists and is readable
- **YAML frontmatter** is well-formed
- **Required fields**: `name`, `description`
- **Name format**: kebab-case, <=64 chars, matches directory name
- **Field lengths**: description <=1024, compatibility <=500
- **Tool declarations**: non-empty names, no duplicates, snake_case client-safe format
- **Script files**: `source_file` references exist in `scripts/`
- **Sidecar files**: `metadata.dcc-mcp.tools/groups/prompts` references exist
- **Dependencies**: `metadata.dcc-mcp.depends` consistency
- **Spec compliance**: non-standard top-level keys are frontmatter errors; dcc-mcp-core extensions must live under `metadata.dcc-mcp.*` and point to sibling files
- **Version metadata**: `metadata.dcc-mcp.version` is accepted and projected
  to `SkillMetadata.version`; top-level `version` fails with an actionable
  migration hint
- **Skill helper adoption**: `validate_skill_dir` emits `skill-helper-adoption` warnings when scripts import avoidable dependencies covered by `dcc_mcp_core.skills_helper`, such as `requests`, `httpx`, PyYAML, or local JSON/HTTP/file/path helper modules
