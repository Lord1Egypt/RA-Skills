# AWP Platform Adapter: ClawHub (OpenClaw)

ClawHub is the public skill registry for agent frameworks. This adapter
describes how AWP workflows and skills integrate with ClawHub for
discovery, publishing, and installation.

There are two integration paths:

1. **Publish the AWP build skill** to ClawHub so any user can install it
   and generate AWP workflows from natural language.
2. **Publish individual AWP workflows** as ClawHub skills so others can
   install and run pre-built workflows.

---

## 1. AWP Build Skill on ClawHub

The `skill/SKILL.md` in this repository already has ClawHub-compatible
YAML frontmatter and can be published directly.

### Publishing

```bash
# From the agent-workflow-protocol repo root
clawhub publish skill/
```

This publishes the AWP build skill including all templates, references,
adapters, and extensions. Users install it with:

```bash
clawhub install awp-workflow-builder
```

Once installed, any ClawHub-compatible agent (Clawdbot, Claude, etc.)
can use the skill to generate AWP workflows from natural language.

---

## 2. AWP Workflows as ClawHub Skills

An individual AWP workflow can be published as a ClawHub skill. This
lets other users discover, install, and run your workflow.

### Packaging a Workflow for ClawHub

An AWP workflow becomes a ClawHub skill by adding ClawHub-compatible
YAML frontmatter to its existing files. The workflow directory already
contains a SKILL.md-compatible structure.

#### Option A: Add a SKILL.md wrapper

Create a `SKILL.md` at the workflow root that describes the workflow
and wraps the AWP configuration:

```markdown
---
name: my-research-pipeline
description: >
  Three-agent research pipeline that plans, researches, and writes
  articles on any topic. AWP L1 Composable compliant.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - LLM_API_KEY
        - LLM_MODEL
      bins: []
    primaryEnv: LLM_API_KEY
    emoji: "\U0001F50D"
    homepage: https://github.com/user/my-research-pipeline
    tags:
      - awp
      - research
      - multi-agent
      - pipeline
---

# Research Pipeline

A three-agent AWP workflow for automated research and article writing.

## Agents

| Agent | Role | Description |
|-------|------|-------------|
| planner | Strategist | Breaks down the research topic into subtasks |
| researcher | Investigator | Gathers information for each subtask |
| writer | Author | Synthesizes findings into a polished article |

## Usage

### With AWP Runtime

\`\`\`python
from awp.runtime import WorkflowRunner

runner = WorkflowRunner(".")
result = runner.run("Research quantum computing trends in 2026")
print(result["writer"]["article"])
\`\`\`

### With AWP CLI

\`\`\`bash
awp run . --task "Research quantum computing trends in 2026"
\`\`\`

## Compliance

AWP L1 Composable -- DAG orchestration with state sharing.

## Files

See `workflow.awp.yaml` for the full manifest and `agents/` for
individual agent configurations.
```

#### Option B: Use workflow.awp.yaml as the skill

If the workflow already has a `SKILL.md` (e.g., project-level skills),
rename it or create a wrapper. ClawHub requires a `SKILL.md` at the
package root.

### Directory Structure for ClawHub

```
my-research-pipeline/           <-- published as ClawHub skill
├── SKILL.md                    <-- ClawHub frontmatter + description
├── workflow.awp.yaml           <-- AWP manifest
├── agents/
│   ├── planner/
│   │   ├── agent.awp.yaml
│   │   ├── agent.py
│   │   └── workflow/...
│   ├── researcher/...
│   └── writer/...
├── mcp/                        <-- custom tools (optional)
├── skills/                     <-- project skills (optional)
└── .clawhubignore              <-- exclude runtime data
```

### .clawhubignore

Exclude runtime artifacts from publishing:

```
workspace/
runs/
data/state/
logs/
__pycache__/
*.pyc
.env
```

### Publishing

```bash
cd my-research-pipeline
clawhub publish .
```

### Installing

```bash
clawhub install my-research-pipeline
```

After installation, the workflow is available in the ClawHub skills
directory and can be executed with any AWP-compatible runtime.

---

## 3. AWP Extensions as ClawHub Skills

AWP extensions (e.g., `financial.md`, `devops.md`) can also be published
as standalone ClawHub skills. This enables a marketplace of domain-specific
AWP customizations.

### Extension Skill Structure

```
awp-ext-financial/
├── SKILL.md                    <-- ClawHub frontmatter
└── financial.md                <-- AWP extension file
```

Example `SKILL.md` for an extension:

```markdown
---
name: awp-ext-financial
description: >
  AWP extension for financial workflows. Adds risk assessment agents,
  audit trail requirements, and compliance controls.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    tags:
      - awp
      - awp-extension
      - financial
      - compliance
---

# AWP Financial Extension

Domain extension for the AWP Workflow Builder skill.

## Installation

1. Install the AWP build skill: `clawhub install awp-workflow-builder`
2. Install this extension: `clawhub install awp-ext-financial`

## Usage

Tell your AI assistant:

> "Build a portfolio analysis workflow using the AWP financial extension."

The AI loads both the base AWP skill and this extension, then generates
a workflow with built-in risk assessment, audit logging, and compliance
controls.

See `financial.md` for the complete extension specification.
```

---

## 4. ClawHub Metadata in AWP Manifests

AWP workflows that target ClawHub publication can include ClawHub
metadata directly in `workflow.awp.yaml` under a `clawhub` section:

```yaml
awp: "1.0.0"

workflow:
  name: my-research-pipeline
  version: "1.0.0"
  description: "Three-agent research pipeline"
  tags: ["awp", "research"]

  # ClawHub publication metadata (optional, ignored by AWP runtimes)
  clawhub:
    slug: my-research-pipeline
    emoji: "\U0001F50D"
    primary_env: LLM_API_KEY
    requires:
      env: [LLM_API_KEY, LLM_MODEL]

# ... rest of AWP manifest
```

AWP runtimes SHOULD ignore the `clawhub` section. It is used only for
generating the ClawHub `SKILL.md` frontmatter during `awp pack --clawhub`.

---

## 5. CLI Integration

### Proposed AWP CLI commands for ClawHub

```bash
# Generate SKILL.md from workflow.awp.yaml for ClawHub publishing
awp clawhub init <workflow-dir>

# Pack workflow as ClawHub-ready directory (adds SKILL.md + .clawhubignore)
awp clawhub pack <workflow-dir> [-o <output-dir>]

# Publish directly to ClawHub (requires clawhub CLI)
awp clawhub publish <workflow-dir>
```

These commands are convenience wrappers:
- `awp clawhub init` generates `SKILL.md` from `workflow.awp.yaml` metadata
- `awp clawhub pack` creates a directory ready for `clawhub publish`
- `awp clawhub publish` calls `clawhub publish` after packing

---

## 6. Discovery Tags Convention

AWP skills on ClawHub use these tag conventions for discoverability:

| Tag | Meaning |
|-----|---------|
| `awp` | This is an AWP-related skill |
| `awp-workflow` | A complete AWP workflow |
| `awp-extension` | An AWP domain extension |
| `awp-builder` | The AWP build skill itself |
| `awp-l0` through `awp-l5` | Compliance level |
| `multi-agent` | Multi-agent workflow |

### Searching for AWP skills on ClawHub

```bash
clawhub search awp
clawhub explore --sort trending --limit 20
```

---

## 7. Compatibility Notes

| ClawHub Requirement | AWP Compatibility |
|---------------------|-------------------|
| SKILL.md with frontmatter | Add as wrapper around workflow |
| Slug: `^[a-z0-9][a-z0-9-]*$` | AWP `workflow.name` uses same pattern |
| Text files only | AWP workflows are YAML/MD/JSON/Python -- all text |
| 50MB limit | AWP workflows are typically <1MB |
| MIT-0 license | AWP is MIT -- compatible |
| SemVer versioning | AWP uses SemVer for `workflow.version` |
