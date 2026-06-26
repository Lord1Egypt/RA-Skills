# Session Analyze

Analyzes Claude Code sessions to provide statistics, tool usage patterns, and optimization insights.

## Quick Start

```
/session analyze              # analyze current session
/session analyze <session_id> # analyze specific session
/session analyze --sync       # sync to Serena memory
```

## Instructions

### 1. Determine Target Session

If session ID is not provided:
- Extract current session ID from conversation context
- If unavailable, show recent session list and request selection

If session ID is provided:
- Use that session ID directly

### 2. Confirm Project Name

Derive project folder name from current working directory:
- Format: `-Users-username-path-to-project` (path with hyphens)

### 3. Call analyze_session API

Use the claude-sessions-mcp MCP tool:

```
mcp__claude-sessions-mcp__analyze_session({
  project_name: "<project-folder-name>",
  session_id: "<session-id>"
})
```

### 4. Output Results

Format analysis results in readable tables:

**Session Overview**
| Metric | Value |
|--------|-------|
| Duration | X minutes |
| Total Messages | N |
| User Messages | N |
| Assistant Messages | N |

**Tool Usage**
| Tool | Count | Errors |
|------|-------|--------|
| Bash | N | N |
| Read | N | N |
| ... | ... | ... |

**Files Changed**
- List of modified files

**Detected Patterns**
- Patterns such as high error rate, many snapshots

**Milestones**
- Key checkpoints in the session

### 5. Provide Insights

Suggestions based on analysis results:
- Optimization opportunities (e.g., reduce snapshots)
- Patterns to watch (e.g., high error rate tools)
- Session efficiency metrics

## Example Output

```
## Session Analysis: b06f2f1c

**Overview**
| Metric | Value |
|--------|-------|
| Duration | 10 min |
| Messages | 107 |
| Snapshots | 7 |

**Top Tools**
1. Bash: 13 calls (0 errors)
2. Read: 3 calls (0 errors)
3. Edit: 3 calls (0 errors)

**Files Changed**: 2 files
- ~/.claude/skills/git-repo/scripts/git-fix-worktree.sh
- ~/.claude/skills/git-repo/SKILL.md

**Insights**
- Session was efficient with no tool errors
- 7 snapshots could be compressed to save space
```

## Sync to Serena Memory (--sync)

When the `--sync` flag is provided:

### 1. Extract Project Knowledge

```
mcp__claude-sessions-mcp__extract_project_knowledge({
  project_name: "<project-folder-name>"
})
```

### 2. Format as Markdown

```markdown
# Project Knowledge: {project-name}

Last updated: {timestamp}

## Hot Files
- path/to/file.ts - modification count: N

## Common Workflows
- Tool1 → Tool2 → Tool3 (frequency: N)

## Key Decisions
- Context: ... | Decision: ...
```

### 3. Save to Serena Memory

```
mcp__serena__write_memory({
  memory_file_name: "project-knowledge-{safe-project-name}.md",
  content: "<formatted-markdown>"
})
```

## Requirements

- claude-sessions-mcp MCP server required
- Session must exist in ~/.claude/projects/
- When using --sync: Serena MCP server must be active with the project
