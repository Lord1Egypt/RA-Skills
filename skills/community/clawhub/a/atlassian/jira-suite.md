# Jira Suite — Platform, Software, and Service Management

## Jira Platform REST v3

Base URL:
`https://{site}.atlassian.net/rest/api/3`

Use for:
- issues, comments, worklogs, transitions
- projects, fields, workflows, filters, dashboards
- users, groups, permissions, audit, webhooks

Quick example:
```bash
curl -s "https://<site>.atlassian.net/rest/api/3/search?jql=project=TEAM&maxResults=50" \
  -u "<email>:<api_token>" \
  -H "Accept: application/json"
```

## Jira Software REST

Base URL:
`https://{site}.atlassian.net/rest/agile/1.0`

Use for:
- boards and board filters
- sprints and sprint issues
- backlog and agile ranking flows

Quick example:
```bash
curl -s "https://<site>.atlassian.net/rest/agile/1.0/board/<board_id>/sprint" \
  -u "<email>:<api_token>" \
  -H "Accept: application/json"
```

## Jira Service Management REST

Base URL:
`https://{site}.atlassian.net/rest/servicedeskapi`

Use for:
- customer requests and request types
- service desks, queues, and knowledgebase links
- customers and support organizations

Quick example:
```bash
curl -s "https://<site>.atlassian.net/rest/servicedeskapi/request" \
  -u "<email>:<api_token>" \
  -H "Accept: application/json"
```

## Jira-Specific Gotchas

- Rich text often needs Atlassian Document Format, not plain text.
- Transition actions use transition IDs or status mappings, not free-form status text.
- Agile entities like boards and sprints are not in Platform REST v3.
- JSM permissions can differ sharply from plain Jira project permissions.
- Pagination uses `startAt` and `maxResults`; do not assume full result sets.
- Search and mutation permissions are project- and role-dependent even with valid auth.

## Official Docs

- Platform: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
- Software: https://developer.atlassian.com/cloud/jira/software/rest/intro/
- Service Management: https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/
