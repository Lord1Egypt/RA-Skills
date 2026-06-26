# Knowledge Sync

Synchronizes knowledge extracted from project sessions to Serena memory.

## Usage

```bash
/sync knowledge <session_id>      # Extract knowledge from a specific session
/sync knowledge                   # Recommend knowledge update candidates based on current conversation
```

## Workflow

### Mode 1: When Session ID is Specified

Automatically extracts knowledge from a specific session using MCP.

#### 1. Check MCP Tools

Check availability of the following tools:
- `mcp__claude-sessions-mcp__extract_project_knowledge`
- `mcp__serena__write_memory`

- **Both available**: Proceed directly to step 3
- **Unavailable**: Proceed with step 2 UTCP registration

#### 2. Register MCP via UTCP (only when not directly registered)

**Register claude-sessions-mcp:**

```bash
/utcp claude-sessions-mcp add
```

Register with code-mode:

```
Call mcp__code-mode__register_manual tool:
- template_name: "claude_sessions"
```

**Register serena:**

```bash
/utcp serena add
```

Register with code-mode:

```
Call mcp__code-mode__register_manual tool:
- template_name: "serena"
```

#### 3. Extract Knowledge

**When MCP is directly registered:**

```
Call mcp__claude-sessions-mcp__extract_project_knowledge
- session_id: "<session UUID>"
```

**When using UTCP/code-mode:**

```
Call mcp__code-mode__call_tool_chain tool:
- tool_call_chain: "claude_sessions.claude_sessions_mcp_extract_project_knowledge"
- input: { "session_id": "<session UUID>" }
```

#### 4. Save to Serena Memory

**When MCP is directly registered:**

```
Use mcp__serena__write_memory
- Memory filename: project-knowledge-{project-name}.md
```

**When using UTCP/code-mode:**

```
Call mcp__code-mode__call_tool_chain tool:
- tool_call_chain: "serena.serena_write_memory"
- input: { "path": "project-knowledge-{project-name}.md", "content": "..." }
```

---

### Mode 2: When Session ID is Not Specified (Current Conversation Based)

Analyzes the current conversation content and recommends knowledge update candidates.

#### 1. Analyze Current Conversation

Extract the following items from the conversation:

- **Discovered infrastructure info**: Server paths, ports, config file locations
- **Resolved issues**: Error causes, solutions
- **Newly learned patterns**: Workflows, tool usage patterns
- **Important decisions**: Architecture decisions, reasons for technology choices

#### 2. Present Knowledge Update Candidates

```markdown
## Knowledge Update Candidates

### Infrastructure Info (recommended to add to CLAUDE.md or rules)
- [ ] {discovered server config path}
- [ ] {discovered port mapping}

### Issue Resolution Records (recommended to add to pages/FAILED_ATTEMPTS.md)
- [ ] {issue}: {solution}

### Project Knowledge (recommended to save to Serena memory)
- [ ] {pattern or workflow}

### Recommended Actions
1. Add to CLAUDE.md: {item}
2. Update Serena memory: {item}
3. No documentation needed: {item} (one-time task)
```

#### 3. Execute Based on User Selection

For items selected by the user:
- Add to CLAUDE.md/rules → Use Edit tool
- Save to Serena memory → Perform save step from Mode 1
- FAILED_ATTEMPTS.md → Use Edit tool

## Storage Format

```markdown
# Project Knowledge: {project-name}

Last updated: {timestamp}

## Hot Files (frequently modified files)
- path/to/file.ts - modification count: N

## Common Workflows
- Tool1 → Tool2 → Tool3 (frequency: N)

## Key Decisions
- Context: ...
  Decision: ...
  Session: ...

## Patterns
- Pattern Type: description (frequency: N)
```

## Notes

- Overwrite if existing memory exists
- Skip projects without sessions
- Report cause on error
