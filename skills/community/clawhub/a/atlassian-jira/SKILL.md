---
name: jira
version: 1.0.0
description: Manage Jira Cloud issues — search, create, update, comment, transition. Use when user mentions Jira, issues, tickets, sprints, bugs, tasks, or issue keys like PROJ-123.
author: Viksi.ai
license: MIT
metadata:
  openclaw:
    emoji: "🎫"
    requires:
      env: ["ATLASSIAN_URL", "ATLASSIAN_EMAIL", "ATLASSIAN_API_TOKEN"]
      tools: ["curl", "python3"]
---

# Jira Cloud

Manage Jira Cloud issues via a bash CLI wrapper. No `jq` required — uses `python3` for JSON parsing, which is available in the stock OpenClaw container.

Script location: `{baseDir}/jira-cli.sh`

## Setup

Set these environment variables on your OpenClaw gateway:

- `ATLASSIAN_URL` — your Jira instance (e.g. `https://yourcompany.atlassian.net`)
- `ATLASSIAN_EMAIL` — the Atlassian account email
- `ATLASSIAN_API_TOKEN` — API token from [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

Make the script executable: `chmod +x {baseDir}/jira-cli.sh`

## Commands

### Search issues

```bash
{baseDir}/jira-cli.sh search "assignee=currentUser() AND status!=Done"
{baseDir}/jira-cli.sh search "project=PROJ AND issuetype=Bug" 50
```

Second argument is max results (default: 20).

Returns: `{ total, issues: [{ key, summary, status, priority, assignee, type, created, updated }] }`

Common JQL patterns:
- My open issues: `assignee=currentUser() AND status!=Done`
- All bugs in project: `project=PROJ AND issuetype=Bug`
- Created this week: `project=PROJ AND created >= startOfWeek()`
- High priority open: `project=PROJ AND priority=High AND status!=Done`
- By status: `project=PROJ AND status="In Progress"`
- Updated recently: `project=PROJ AND updated >= -7d`

### Get issue details

```bash
{baseDir}/jira-cli.sh get PROJ-123
```

Returns: `{ key, summary, status, priority, type, assignee, reporter, project, description, labels, created, updated, url }`

### Create issue

```bash
{baseDir}/jira-cli.sh create --project PROJ --type Bug --summary "Login fails with unicode email" --description "Steps to reproduce..." --priority High
```

Required: `--project`, `--summary`
Optional: `--type` (default: Task), `--description`, `--priority`

Returns: `{ key, id, url }`

### Add comment

```bash
{baseDir}/jira-cli.sh comment PROJ-123 "Tested on staging — confirmed fixed"
```

Returns: `{ id, created, author }`

### List available transitions

Always check this before transitioning — transition IDs vary per project workflow.

```bash
{baseDir}/jira-cli.sh transitions PROJ-123
```

Returns: `{ transitions: [{ id, name, to }] }`

### Transition issue (change status)

```bash
{baseDir}/jira-cli.sh transition PROJ-123 31
```

Second argument is the transition ID from the `transitions` command.

### Assign issue

First look up the user's account ID:

```bash
{baseDir}/jira-cli.sh users "jane"
```

Then assign:

```bash
{baseDir}/jira-cli.sh assign PROJ-123 "5b10a2844c20165700ede21g"
```

### Update issue fields

```bash
{baseDir}/jira-cli.sh update PROJ-123 --summary "Updated title" --priority High --labels "regression,blocker"
```

Labels are comma-separated.

### List projects

```bash
{baseDir}/jira-cli.sh projects
```

Returns: `[{ key, name, type }]`

## Rules

- All output is JSON to stdout, errors to stderr.
- Before transitioning, ALWAYS run `transitions` first to get valid IDs.
- Before assigning, ALWAYS run `users` first to get the account ID.
- If a command fails, the error JSON includes the HTTP status code.
