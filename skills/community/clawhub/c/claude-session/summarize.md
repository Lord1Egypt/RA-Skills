# Session Summarize

Retrieves and summarizes the conversation content from other Claude Code sessions.

## Quick Start

```
/session summarize                 # Select project/session then summarize
/session summarize <session_id>    # Summarize a specific session
```

## Instructions

### 0. Pre-check: Verify claude-sessions-mcp tool registration

Call `mcp__code-mode__list_tools` to check whether `claude-sessions-mcp` related tools are available:

```
mcp__code-mode__list_tools
```

If `mcp__claude-sessions-mcp__list_projects` is **not** in the results, register via the utcp skill first:

```
/utcp register
```

After registration, verify again with `list_tools` before proceeding to the next step.

### 1. Select Project

If the project name is unknown, query via MCP:

```
mcp__claude-sessions-mcp__list_projects
```

Show the project list to the user and ask them to select one.

### 2. Select Session

```
mcp__claude-sessions-mcp__list_sessions
project_name: [selected project name]
```

Show the session list with title, date, message count, etc.

### 3. Remove Profanity (Optional)

It is recommended to remove profanity from session files before summarizing:

```bash
scripts/clean-profanity.py ~/.claude/projects/<project_name>/<session_id>.jsonl
```

See [profanity-cleaner.md](./profanity-cleaner.md) for details.

### 4. Extract Conversation Content (Using Script)

```bash
scripts/summarize-session.py <project_name> <session_id> [limit]
```

**Output format:**
```
user [01-18 14:30]: First request content...
assistant: Response content...
user [01-18 14:35]: Next request...
assistant: Next response...
```

- `user`: Includes timestamp `[MM-DD HH:MM]`
- `assistant`: No timestamp
- Messages exceeding 100 characters are truncated

### 5. Extract Todo Items (Optional)

For sessions that used TodoWrite, extract the completed/incomplete task list directly:

```bash
scripts/extract-todos.py <project_name> <session_id>
```

Use `--all` flag to also view intermediate snapshots:

```bash
scripts/extract-todos.py <project_name> <session_id> --all
```

→ Use this result directly as the "completed task list" in step 6 summary generation

### 6. Generate Summary

Synthesize conversation content and Todo items to produce:
- Summary of key tasks performed
- List of completed tasks (using extract-todos results)
- List of incomplete/in-progress tasks
- Important decisions or context

## Output

1. **Session Overview**: Project name, session ID, date
2. **Conversation Summary**: Key tasks, completed/incomplete items
3. **Next Steps Suggestion**: Recommendations such as pipeline delivery via import, analysis, etc.

## Notes

- Default limit: 50 messages
- For large session files, only the most recent 50 messages are read
- Be cautious with sensitive information (API keys, tokens)
- Currently active sessions have files that are continuously updated
