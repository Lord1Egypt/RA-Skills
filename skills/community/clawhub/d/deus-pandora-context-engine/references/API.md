# Context Engine API Reference

## Commands

```bash
# List all projects
node context-engine.js list

# Create a new project
node context-engine.js create "Project Name" "Description"

# Switch to a project (creates if doesn't exist)
node context-engine.js switch "Project Name"

# Get active project
node context-engine.js get-active

# Get project by ID
node context-engine.js get "project-id"

# Save context (JSON string)
node context-engine.js save '{"lastTopic": "topic", "lastFile": "file.txt"}'

# Restore context (session start)
node context-engine.js restore

# Summarize active project
node context-engine.js summarize

# Add pending task
node context-engine.js add-task "Task description"

# Remove pending task by index
node context-engine.js remove-task 0

# Set project status
node context-engine.js set-status "paused"

# Heartbeat (periodic save)
node context-engine.js heartbeat
```

## Data Storage

- **Projects:** `/home/deus/.openclaw/workspace/memory/projects/projects.json`
- **Session:** `/home/deus/.openclaw/workspace/memory/projects/session.json`

## Project Schema

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "status": "active|paused|completed|archived",
  "createdAt": "ISO8601",
  "updatedAt": "ISO8601",
  "lastSessionAt": "ISO8601",
  "sessionCount": "number",
  "context": {
    "lastTopic": "string",
    "lastFile": "string",
    "lastCommand": "string",
    "pendingTasks": ["string"],
    "notes": "string"
  },
  "metadata": {
    "tags": ["string"],
    "custom": {}
  }
}
```
