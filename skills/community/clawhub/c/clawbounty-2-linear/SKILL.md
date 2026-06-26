---
name: linear
description: "Manage Linear issues, projects, and cycles via GraphQL. Use when triaging backlogs, creating tasks from conversation, checking sprint progress, or running team reviews. Requires LINEAR_API_KEY."
metadata:
  openclaw:
    emoji: 🔷
    requires:
      env:
        - LINEAR_API_KEY
    install:
      - id: api-key
        kind: manual
        label: "Get your Linear API key"
        steps:
          - "Go to Linear → Settings → API → Personal API keys"
          - "Create a new key with read + write scope"
          - "Set LINEAR_API_KEY=<your-key> in your OpenClaw workspace config"
---

## Purpose

Control Linear from OpenClaw. Create issues, triage backlogs, update priorities, and run sprint reviews — all from your AI assistant, without switching tabs.

Works via Linear's GraphQL API using `curl`. No CLI or SDK required.

## When to Use

- Checking sprint progress mid-cycle
- Creating issues from meeting notes or conversation
- Triaging and reprioritizing a backlog
- Looking up an issue's status before a standup
- Bulk-updating labels, assignees, or priorities
- Generating a status report across projects or teams

## When NOT to Use

- Complex Figma/design reviews (use browser tooling)
- GitHub PR integration (use the `github` skill instead)
- Syncing Linear with Jira or other trackers (script with Linear's API directly)

## Setup

1. Open Linear → Settings → API → Personal API keys
2. Create a key (read + write scope)
3. Add to your OpenClaw config:

```
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxxxxx
```

Verify the key works:
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { name } }"}' | jq .
```

You should see your name returned.

## Commands

### List your open issues

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ viewer { assignedIssues(filter: { state: { type: { nin: [\"completed\", \"cancelled\"] } } }) { nodes { id title priority state { name } team { name } } } } }"
  }' | jq '.data.viewer.assignedIssues.nodes'
```

### Get issues for a team

```bash
TEAM_KEY="ENG"  # your team's key

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"{ team(key: \\\"$TEAM_KEY\\\") { issues(filter: { state: { type: { eq: \\\"started\\\" } } }) { nodes { id identifier title assignee { name } priority } } } }\"
  }" | jq '.data.team.issues.nodes'
```

### Create an issue

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation IssueCreate($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier title } } }",
    "variables": {
      "input": {
        "teamId": "TEAM_ID_HERE",
        "title": "Issue title from OpenClaw",
        "description": "Created via OpenClaw linear skill.",
        "priority": 2
      }
    }
  }' | jq '.data.issueCreate'
```

Priority levels: `0` = No priority, `1` = Urgent, `2` = High, `3` = Medium, `4` = Low.

### Update an issue

```bash
ISSUE_ID="ISSUE_ID_HERE"

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"mutation { issueUpdate(id: \\\"$ISSUE_ID\\\", input: { priority: 1, stateId: \\\"STATE_ID\\\" }) { success issue { id title priority state { name } } } }\"
  }" | jq '.data.issueUpdate'
```

### Search issues by keyword

```bash
QUERY="authentication bug"

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"{ issueSearch(query: \\\"$QUERY\\\") { nodes { id identifier title state { name } assignee { name } priority } } }\"
  }" | jq '.data.issueSearch.nodes'
```

### Get current cycle (sprint) for a team

```bash
TEAM_KEY="ENG"

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"{ team(key: \\\"$TEAM_KEY\\\") { activeCycle { id name startsAt endsAt issues { nodes { id title state { name } estimate } } } } }\"
  }" | jq '.data.team.activeCycle'
```

### Add a comment to an issue

```bash
ISSUE_ID="ISSUE_ID_HERE"
COMMENT="LGTM — deploying to staging now."

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"mutation { commentCreate(input: { issueId: \\\"$ISSUE_ID\\\", body: \\\"$COMMENT\\\" }) { success comment { id body } } }\"
  }" | jq '.data.commentCreate'
```

## Examples

**Morning standup prep:**
"What are my open Linear issues with priority Urgent or High?"
→ Run the "list your open issues" query, filter by priority ≤ 2.

**After a meeting:**
"Create a Linear issue in the ENG team: 'Fix auth token refresh race condition', High priority"
→ Look up ENG team ID, then run the create mutation with the title and priority=2.

**Sprint review:**
"Show me all completed issues in the current ENG cycle"
→ Get activeCycle, filter `state.type == "completed"`. Summarize with titles and estimates.

**Triage:**
"Move all issues assigned to @alice in ENG to 'In Progress'"
→ Fetch issues, get state ID for "In Progress", run issueUpdate for each.

## Notes

- **Rate limits**: Linear API allows 1,500 requests/hour. Cache results for bulk reads.
- **IDs vs keys**: Teams can be queried by `key` (e.g. `"ENG"`). Issues, states, and cycles require UUIDs. Get UUIDs from list queries.
- **GraphQL introspection**: Run `{ __schema { types { name } } }` to explore the full API schema.
- **Webhooks**: For real-time issue updates, configure a webhook in Linear → Settings → API → Webhooks. Pair with the `webhook-listener` skill.
- **Pagination**: Large teams should use `first: N, after: cursor` pagination. Default page size is 50.
