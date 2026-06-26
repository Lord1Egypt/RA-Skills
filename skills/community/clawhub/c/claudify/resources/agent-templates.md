# Agent Templates

Claude Code agent templates and usage examples.

## Basic Structure

```markdown
---
name: agent-name
description: Brief description. Use when [trigger conditions].
tools: [Tool1, Tool2, Tool3]
---

# Agent Name

## Purpose

What this agent does

## Instructions

1. Step one
2. Step two
3. Step three

## Output

What to return to the parent agent
```

## Frontmatter Fields

| Field         | Required | Description                                                    |
| ------------- | -------- | -------------------------------------------------------------- |
| `name`        | ✅       | Agent identifier (kebab-case)                                  |
| `description` | ✅       | Description + trigger conditions + examples (escaped newlines) |
| `tools`       | ❌       | Allowed tools list (all if omitted)                            |
| `model`       | ❌       | Model to use (sonnet, opus, haiku)                             |

### CRITICAL: Description Field Format

The `description` field **MUST be a single line** with escaped newlines (`\n`). Multi-line descriptions break YAML parsing.

**✅ Correct (single line with `\n`):**

```yaml
description: Brief description. Use when [trigger].\n\nExamples:\n\n<example>\nContext: ...\nuser: "..."\nassistant: "..."\n</example>
```

**❌ Wrong (multi-line with `Examples:`):**

```yaml
description: Brief description.

Examples:

<example>
...
</example>
```

**✅ Correct (multi-line with `|`):**

```yaml
description: |
  Brief description
  Examples:

  <example>
  ...
  </example>
```

### Description with Examples Template

```yaml
description: [Brief description]. [Trigger keywords: "keyword1", "keyword2"]\n\nExamples:\n\n<example>\nContext: [When this triggers]\nuser: "[User message]"\nassistant: "[Agent response]"\n<Task tool call to agent-name agent>\n</example>
```

## Template Examples

### 1. Code Review Agent

```markdown
---
name: code-reviewer
description: Code review after git commits. Checks conventions against CONTRIBUTING.md if exists, otherwise offers to create one
tools: [Glob, Grep, Read, WebFetch, TodoWrite, Edit, Write, NotebookEdit]
---

# Code Reviewer

## Purpose

Review committed code for quality and convention compliance.

## Instructions

1. Check for CONTRIBUTING.md
2. If exists:
   - Check changed files (`git diff HEAD~1 --name-only`)
   - Compare with CONTRIBUTING.md rules
   - Report violations
3. If not exists:
   - Analyze project structure
   - Suggest CONTRIBUTING.md creation

## Output

- Convention violation list
- Improvement suggestions
- (If needed) CONTRIBUTING.md draft
```

### 2. CI/CD Monitor Agent

```markdown
---
name: cicd-manager
description: Check CI/CD pipeline status after git push
tools: [Bash, Read, WebFetch, TodoWrite]
---

# CI/CD Manager

## Purpose

Check and report pipeline execution status after push.

## Instructions

1. Check current branch and remote
2. Query pipeline status via API
3. If running, poll until complete (30s interval, max 10min)
4. Analyze results:
   - Success: Summary report
   - Failure: Log analysis and cause estimation
   - Not running: Check CI config

## Output

- Pipeline status (success/failed/pending)
- Cause analysis on failure
- Suggested next actions
```

### 3. Cleanup Agent

```markdown
---
name: system-cleanup
description: System cleanup and maintenance. Clean caches, temp files, and unused resources
tools: [Bash, Glob, Grep, Read, TodoWrite, Edit, Write]
---

# System Cleanup

## Purpose

Safely clean unnecessary files from the system.

## Instructions

1. Check current disk usage (`df -h`)
2. Scan cleanup targets:
   - Package caches (npm, pip, brew)
   - Build artifacts
   - Temp files
3. Calculate size for each item
4. Request user confirmation for cleanup items
5. Execute cleanup only for approved items

## Output

- Before/after size comparison
- Deleted item list
- Recovered space
```

### 4. Report Generator Agent

````markdown
---
name: report-generator
description: Generate reports from data or work history. Use for weekly reports, summaries, or analysis
tools: [Bash, Glob, Grep, Read, WebFetch, TodoWrite, Edit, Write]
---

# Report Generator

## Purpose

Collect and organize work history into reports.

## Instructions

1. Collect git commits for the period
   ```bash
   git log --since="last monday" --until="now" --oneline
   ```
````

2. Collect completed items from task tracker
3. Categorize:
   - New features
   - Bug fixes
   - Refactoring
   - Documentation
4. Write according to report template

## Output

- Report markdown
- Key achievements summary (3-5 lines)
```

### 5. Explore Agent (Fast Search)

```markdown
---
name: explore
description: Fast codebase exploration. Use for file pattern search, keyword search, structure understanding
tools: [Glob, Grep, Read, Bash]
model: haiku
---

# Explore

## Purpose
Quickly explore codebase to gather information.

## Instructions

1. Identify request type:
   - Find files → Use Glob
   - Search code → Use Grep
   - Understand structure → Use ls + tree
2. Execute search (parallel if possible)
3. Summarize results

## Output
- Found file/code locations
- Related context summary
- Additional exploration suggestions (if needed)
```

### 6. Refactor Agent

```markdown
---
name: refactor
description: Code refactoring and structure improvement. File size limits, component/utility separation
tools: [Bash, Glob, Grep, Read, Edit, Write, TodoWrite]
---

# Refactor

## Purpose

Split large files and improve structure.

## Instructions

1. Analyze target file
   - Total line count
   - Script/template/style ratio
2. Apply separation criteria:
   - Components: Consider split if >200 lines
   - Utility functions: Separate to `.ts` file
   - Types: Separate to `types.ts`
3. Present separation plan
4. Execute after approval

## Output

- Separated file list
- Changed import paths
- Items requiring verification
```

## Agent Invocation

### Using Task Tool

```
Task tool with:
- subagent_type: "agent-name"
- prompt: "Task description"
- description: "3-5 word summary"
```

### Example

```
subagent_type: "code-reviewer"
prompt: "Review the changes from the recent commit"
description: "Review recent commit"
```

### 7. Interactive Supervisor Agent (User-Decision Pattern)

Pattern for agents that collect decision items, then the **caller** presents them via AskUserQuestion for sequential resolution. The agent itself does NOT call AskUserQuestion.

```markdown
---
name: my-supervisor
description: |
  Supervisor that collects items and reports back for user decisions.
  Reports include a "Requires User Decision" section.
  The caller presents these via AskUserQuestion.

  <example>
  user: "run supervisor"
  assistant: "Launching supervisor..."
  (agent completes)
  assistant: "There are 3 items requiring user decision."
  (AskUserQuestion with the 3 items)
  </example>
skills:
  - relevant-skill
---

# My Supervisor

## Workflow
1. Phase 1: Collect data
2. Phase 2: Analyze
3. Phase 3: Report

## Final Report Format

Include a **Requires User Decision** section in the final report:

### Requires User Decision
- [ ] Item 1 — reason judgment is needed
- [ ] Item 2 — reason judgment is needed
```

**Caller Responsibility** (parent session MUST):

1. Parse "Requires User Decision" section from the agent's result
2. Present items via AskUserQuestion (multiSelect for batch selection)
3. Process selected items sequentially, asking direction per item
4. Optionally offer reassignment to sub-agents for complex items:
   ```
   AskUserQuestion: "Handle directly" / "Delegate to sub-agent" / "Skip"
   ```

**Real example**: `.claude/agents/ralph-supervisor.md`

## Best Practices

1. **Clear triggers**: Specify when to use in description
2. **Tool restrictions**: List only needed tools
3. **Step-by-step instructions**: Structure with numbers
4. **Output specification**: Define what to return
5. **Model selection**: haiku for simple tasks, opus for complex analysis
