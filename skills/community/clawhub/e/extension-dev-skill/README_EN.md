English | **[中文](README.md)**

# extension-dev-skill

A skill for JLCEDA & EasyEDA Pro extension development. Use this skill to let an AI Agent automatically develop plugins, and pair it with extension-dev-mcp-tools for AI-driven building and debugging.

## Setup

### 1. Locate or Create the Skills Directory

Follow your AI Agent's documentation to find or create the directory for skills.
For example:
- Project-level: `.agents/skills`
- Global-level: `~/.agents/skills`

### 2. Clone the Skill Repository

Open a terminal, navigate to the skills directory, and clone:

```bash
git clone https://github.com/easyeda/extension-dev-skill
```

### 3. Verify

Confirm the skill is loaded in your AI Agent.  
For example in OpenCode: run `/skills` and check that `extension-dev-skill` is listed.

## MCP Debugging Tools (Optional)

Recommended: [extension-dev-mcp-tools](https://github.com/easyeda/extension-dev-mcp-tools)

Automatically imports AI Agent-built extensions into the browser for testing.

## Directory Structure

```
jlceda-plugin-builder/
  SKILL.md                 # Core skill definition (rules, workflow, runtime constraints)
  AGENTS.md                # Supplementary agent guide (search standards, recursive queries, code conventions)
  README.md                # Project description (Chinese)
  README_EN.md             # Project description (English, this file)
  resources/
    api-reference.md        # Complete API module list, enum definitions, MCP tool docs
    experience.md           # Common pitfalls and lessons learned
```

## Demo Video

Based on OpenCode:  

https://github.com/user-attachments/assets/742954b8-9527-43ad-ae08-3f08ec083fa2
