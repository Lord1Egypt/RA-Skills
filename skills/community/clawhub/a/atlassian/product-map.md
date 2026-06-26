# Product Map — Atlassian Cloud

| Surface | Main API | Auth | Best CLI path | Notes |
|---------|----------|------|---------------|-------|
| Jira Platform | `https://{site}.atlassian.net/rest/api/3` | API token + email, OAuth 2.0, Forge | `acli jira` | Issues, projects, fields, workflows, users |
| Jira Software | `https://{site}.atlassian.net/rest/agile/1.0` | Same as Jira Platform | `acli jira` for many Jira workflows | Boards, sprints, backlog, epics |
| Jira Service Management | `https://{site}.atlassian.net/rest/servicedeskapi` | API token + email or OAuth 2.0 | No dedicated first-party product CLI | Requests, customers, queues, organizations |
| Confluence Cloud | `https://{site}.atlassian.net/wiki/api/v2` | API token + email, OAuth 2.0, Forge | API first | Pages, spaces, comments, labels, attachments |
| Bitbucket Cloud | `https://api.bitbucket.org/2.0` | Access tokens, app passwords, OAuth 2.0 | API first | Repositories, pull requests, pipelines, workspaces |
| Trello | `https://api.trello.com/1` | Key + token | API first | Boards, lists, cards, checklists, webhooks |
| Cloud Admin | `https://api.atlassian.com/admin` | Admin API key | `acli admin` | Orgs, users, groups, policies, API access |
| Compass | `https://api.atlassian.com/compass/cloud/{cloudId}` and GraphQL | API token, OAuth 2.0, Forge | `forge` for app workflows | Components, scorecards, events, metrics |
| Statuspage | `https://api.statuspage.io/v1` | API token | API first | Pages, incidents, components, metrics, subscribers |
| Opsgenie | `https://api.opsgenie.com` or `https://api.eu.opsgenie.com` | API key | API first | Alerts, schedules, on-call, integrations |
| Atlassian GraphQL | `https://api.atlassian.com/graphql` or product gateway | OAuth, API token, Forge | None | Cross-product graph and product-specific GraphQL |

## Routing Rules

- Use Jira Platform for issues, projects, custom fields, workflows, filters, dashboards, and permissions.
- Use Jira Software for boards, sprints, backlog, and agile-only reporting entities.
- Use Jira Service Management for request types, customers, portals, queues, and support organizations.
- Use Confluence API v2 for page and space automation in Cloud.
- Use Bitbucket and Trello APIs directly because their auth and hosts differ from Atlassian tenant APIs.
- Use Cloud Admin for org-wide user, group, policy, and API access tasks.
- Use Compass REST or GraphQL when the task is about components, scorecards, events, or catalogs.
- Use Statuspage and Opsgenie APIs directly for incident comms and on-call automation.

## Official Docs

- Jira Platform: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
- Jira Software: https://developer.atlassian.com/cloud/jira/software/rest/intro/
- Jira Service Management: https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/
- Confluence: https://developer.atlassian.com/cloud/confluence/rest/v2/intro/
- Bitbucket: https://developer.atlassian.com/cloud/bitbucket/rest/intro/
- Trello: https://developer.atlassian.com/cloud/trello/rest/
- Cloud Admin: https://developer.atlassian.com/cloud/admin/rest-apis/
