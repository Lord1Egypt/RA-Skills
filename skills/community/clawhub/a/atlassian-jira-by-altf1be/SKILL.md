---
name: atlassian-jira-by-altf1be
description: "Atlassian Jira Cloud CRUD skill — manage issues, comments, attachments, workflow transitions, and JQL search via Jira REST API v3 with email + API token auth."
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira
metadata:
  {"openclaw": {"emoji": "🎫", "requires": {"env": ["JIRA_HOST", "JIRA_EMAIL", "JIRA_API_TOKEN"]}, "optional": {"env": ["JIRA_DEFAULT_PROJECT", "JIRA_MAX_RESULTS", "JIRA_MAX_FILE_SIZE"]}, "primaryEnv": "JIRA_HOST"}}
---

# Jira Cloud by @altf1be

Manage Atlassian Jira Cloud issues, comments, attachments, and workflow transitions via the REST API.

## Setup

1. Get an API token from https://id.atlassian.com/manage-profile/security/api-tokens
2. Set environment variables (or create `.env` in `{baseDir}`):

```
JIRA_HOST=yourcompany.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=your-api-token
JIRA_DEFAULT_PROJECT=PROJ
```

3. Install dependencies: `cd {baseDir} && npm install`

## Commands

### Issues

```bash
# List issues (optionally filter by project, status, assignee)
node {baseDir}/scripts/jira.mjs list --project PROJ --status "In Progress" --assignee "currentUser()"

# Create an issue
node {baseDir}/scripts/jira.mjs create --project PROJ --type Task --summary "Fix login bug" --description "Users can't log in" --priority High

# Read issue details
node {baseDir}/scripts/jira.mjs read --key PROJ-123

# Update issue fields
node {baseDir}/scripts/jira.mjs update --key PROJ-123 --summary "New title" --priority Low

# Delete issue (requires --confirm)
node {baseDir}/scripts/jira.mjs delete --key PROJ-123 --confirm

# Search with JQL
node {baseDir}/scripts/jira.mjs search --jql "project = PROJ AND status = Open ORDER BY created DESC"
```

### Comments

```bash
# List comments on an issue
node {baseDir}/scripts/jira.mjs comment-list --key PROJ-123

# Add a comment
node {baseDir}/scripts/jira.mjs comment-add --key PROJ-123 --body "This is ready for review"

# Update a comment
node {baseDir}/scripts/jira.mjs comment-update --key PROJ-123 --comment-id 10001 --body "Updated comment"

# Delete a comment (requires --confirm)
node {baseDir}/scripts/jira.mjs comment-delete --key PROJ-123 --comment-id 10001 --confirm
```

### Attachments

```bash
# List attachments on an issue
node {baseDir}/scripts/jira.mjs attachment-list --key PROJ-123

# Upload an attachment
node {baseDir}/scripts/jira.mjs attachment-add --key PROJ-123 --file ./screenshot.png

# Delete an attachment (requires --confirm)
node {baseDir}/scripts/jira.mjs attachment-delete --attachment-id 10001 --confirm
```

### Workflow Transitions

```bash
# List available transitions for an issue
node {baseDir}/scripts/jira.mjs transitions --key PROJ-123

# Move issue to a new status (by transition ID or name)
node {baseDir}/scripts/jira.mjs transition --key PROJ-123 --transition-id 31
node {baseDir}/scripts/jira.mjs transition --key PROJ-123 --transition-name "Done"
```

## Dependencies

- `commander` — CLI framework
- `dotenv` — environment variable loading
- Node.js built-in `fetch` (requires Node >= 18)

## Security

- Email + API token auth (Basic auth via base64 encoding)
- No secrets or tokens printed to stdout
- All delete operations require explicit `--confirm` flag
- Path traversal prevention for file uploads
- Built-in rate limiting with exponential backoff retry
- Lazy config validation (only checked when a command runs)

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels 🇧🇪
X: [@altf1be](https://x.com/altf1be)
