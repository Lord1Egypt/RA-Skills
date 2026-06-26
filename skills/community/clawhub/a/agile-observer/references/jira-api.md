# Jira Cloud API Quick Reference

## Authentication
- **Method:** Basic Auth with email + API token, or OAuth 2.0 Bearer token.
- **Base URL:** `https://{instance}.atlassian.net/rest/api/3`
- Credentials: look for `jira-credentials.json` in workspace secrets.

## Key Endpoints

### Projects
```
GET /rest/api/3/project/search?maxResults=50
```

### Board & Sprints (Agile API)
```
GET /rest/agile/1.0/board?projectKeyOrId={key}
GET /rest/agile/1.0/board/{boardId}/sprint?state=active,future
GET /rest/agile/1.0/sprint/{sprintId}/issue?fields=summary,status,assignee,created,resolutiondate,customfield_10016
```
- `customfield_10016` is commonly Story Points (verify per instance).

### Issue Search (JQL)
```
POST /rest/api/3/search
{
  "jql": "project = PROJ AND sprint in openSprints()",
  "fields": ["summary", "status", "assignee", "created", "resolutiondate", "labels", "priority"],
  "maxResults": 100
}
```

### Issue Changelog (for cycle time)
```
GET /rest/api/3/issue/{issueKey}/changelog?maxResults=100
```
- Filter for `field == "status"` entries.
- Each entry has `created` (timestamp), `fromString`, `toString`.

## Status Category Mapping
Jira statuses belong to categories:
- **To Do** → statusCategory.key = `new`
- **In Progress** → statusCategory.key = `indeterminate`
- **Done** → statusCategory.key = `done`

Use `statusCategory` for reliable metric computation across custom workflows.

## Rate Limits
- Jira Cloud: ~100 requests/minute for Basic Auth.
- Pagination: use `startAt` + `maxResults` (max 100 per page).
- Bulk fetch: prefer JQL search over individual issue GETs.
