---
name: context-engine
description: Smart Context Engine - Maintains conversation state and project continuity across OpenClaw sessions. Tracks active projects, saves/restores context, and provides project management. Use when: (1) starting a new session and wanting to restore previous context, (2) working on a specific project and wanting to track progress, (3) switching between projects, (4) asking "what are we working on" or "where did we leave off", (5) wanting to save current context manually.

metadata:
  claname: context-engine
  category: memory
  tags:
    - memory
    - context
    - projects
    - workflow
  version: 1.0.0
  author: Community
  license: MIT

requires:
  env: []
  bins: []
  config: []

files:
  - scripts/*
  - "*.md"
---

# Context Engine

Smart Context Engine maintains conversation state and project continuity across OpenClaw sessions.

## Quick Start

The context engine automatically:
- Restores your last active project on session start
- Saves context periodically (heartbeat) and on session end
- Tracks pending tasks and notes per project

### Commands

- **"remember" / "save context"** - Manually save current context
- **"switch to [project]"** - Switch to a project (creates if doesn't exist)
- **"show projects" / "what are we working on"** - List all projects
- **"summarize" / "where did we leave off"** - Get project summary

## Storage

Projects are stored in: `/home/deus/.openclaw/workspace/memory/projects/`

- `projects.json` - All project data
- `session.json` - Current session state

## Actions

### save_context

Saves the current context including:
- Last topic discussed
- Last file worked on
- Last command executed
- Pending tasks
- Notes

**Trigger:** Explicit mention ("remember", "save context"), session_end, heartbeat

### restore_context

Restores the previous session's context:
- Loads last active project
- Shows "Welcome back to [project]"
- Lists pending tasks if any

**Trigger:** session_start, explicit request

### switch_project

Switches between projects:
- Saves current project context
- Loads or creates new project
- Sets as active

**Trigger:** Explicit mention ("switch to X")

### list_projects

Lists all projects with status indicators:
- Shows active project highlighted
- Displays status (active/paused/completed/archived)
- Shows last session date

**Trigger:** Explicit mention ("show projects", "what are we working on")

### summarize

Generates a summary of the active project:
- Current status
- Pending tasks
- Last topic
- Session history

**Trigger:** Explicit mention ("summarize", "where did we leave off")

## Triggers

| Trigger | Condition | Priority |
|---------|-----------|----------|
| session_start | New session begins | 1 |
| explicit_mention | User says "remember", "save context", "project", "switch to", "show projects", "summarize" | 2 |
| heartbeat | Every ~30 min when enabled | 3 |

## Integration

Works with the MEMORY.md system - updates long-term memory with project summaries.
