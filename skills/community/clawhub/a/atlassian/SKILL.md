---
name: Atlassian Cloud APIs + CLIs
slug: atlassian
version: 1.0.0
homepage: https://clawic.com/skills/atlassian
description: Operate Atlassian Cloud APIs and CLIs across Jira, Confluence, Bitbucket, Trello, Admin, Forge, Compass, Opsgenie, and Statuspage.
changelog: Initial release with Atlassian Cloud API and CLI coverage across Jira, Confluence, Bitbucket, Trello, Admin, Forge, Compass, Opsgenie, and Statuspage.
metadata: {"clawdbot":{"emoji":"🧩","requires":{"anyBins":["curl","jq"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User needs to read, create, update, search, administer, or automate Atlassian Cloud products from terminal workflows. This skill routes to the right API or CLI, matches auth to the chosen surface, and avoids unsupported command paths.

## Architecture

Memory lives in `~/atlassian/`. If `~/atlassian/` does not exist, run `setup.md`. See `memory-template.md` for structure. This skill works without persistent memory; save defaults only when the user wants repeatable shortcuts.

```
~/atlassian/
└── memory.md           # Optional saved sites, products, auth preferences, and safety defaults
```

## Quick Reference

Load only the smallest file that matches the current Atlassian surface.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Product routing map | `product-map.md` |
| Jira Platform, Software, and JSM | `jira-suite.md` |
| Confluence, Bitbucket, and Trello | `content-dev-collab.md` |
| Cloud Admin, Compass, Statuspage, Opsgenie, GraphQL | `admin-ops.md` |
| Auth and CLI matrix | `auth-and-clis.md` |

## Scope

This skill is Cloud-first and covers publicly documented Atlassian automation surfaces current as of 2026-03-13. Prefer first-party REST, GraphQL, `acli`, and `forge` paths when they exist. If the user is on Data Center or a product without public Cloud automation docs, say that explicitly before acting.

## Core Rules

### 1. Pick the exact Atlassian surface first
- Jira splits across platform, software, and service management APIs.
- Confluence, Bitbucket, Trello, Cloud Admin, Compass, Statuspage, and Opsgenie each have different auth and URL rules.
- Do not mix Cloud and Data Center docs unless the user explicitly confirms Data Center.

### 2. Ask for only the credential family the chosen surface needs
- Jira, Confluence, GraphQL, and Forge commonly use API token plus email, OAuth 2.0, or Forge auth.
- Bitbucket uses access tokens, app passwords, or OAuth.
- Trello uses key plus token, Statuspage uses an API token, Opsgenie uses an API key, and Cloud Admin uses an admin API key.

### 3. Prefer first-party surfaces before partner CLIs
- Start with official REST, GraphQL, `acli`, or `forge`.
- Use partner CLIs only when Atlassian has no first-party CLI for that product or the user explicitly asks for that toolchain.

### 4. Treat every write as high-impact
- Resolve site, org, project, board, space, page, list, workspace, or component IDs before create, update, archive, or delete operations.
- For bulk or destructive actions, show the exact target set first and get user confirmation.

### 5. Respect product-specific data formats
- Jira rich text often requires Atlassian Document Format.
- Confluence body representations differ from Jira fields.
- Bitbucket relies on slugs, UUIDs, and `next` pagination.
- Trello auth lives in query parameters, while Statuspage nests many write payloads.

### 6. Handle rate limits and pagination every time
- Follow `next` links, cursors, `pagelen`, `limit`, `startAt`, or page tokens depending on the product.
- Back off on HTTP 429 and never hide partial failures on bulk writes.

### 7. Be explicit about CLI support gaps
- Official Atlassian CLI currently exposes `admin`, `jira`, and `rovodev`.
- Official Forge CLI is for building and deploying Forge apps, not for general product CRUD.
- Confluence, Bitbucket, Trello, Statuspage, and Opsgenie still route mainly through APIs or partner CLIs.

## Common Traps

- Using Jira Platform endpoints for boards or sprints -> use Jira Software `/rest/agile/1.0`.
- Sending plain text into Jira rich fields without checking ADF support -> malformed descriptions or comments.
- Forgetting `/wiki` in Confluence Cloud URLs -> wrong host or 404.
- Assuming `acli` covers every Atlassian product -> today it is mostly Jira, Admin, and Rovo Dev.
- Mixing Bitbucket auth with Atlassian tenant auth -> valid token, wrong endpoint family.
- Treating Opsgenie as a long-term target without checking migration plans -> official docs now point many users to Jira Service Management or Compass.
- Reusing tenant GraphQL paths for non-tenant products -> Bitbucket and Trello have different gateway hosts.

## External Endpoints

Route requests only to the endpoint family that matches the active Atlassian product.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://{site}.atlassian.net/rest/api/*` | Jira issue, project, workflow, user, and search payloads | Jira Cloud platform operations |
| `https://{site}.atlassian.net/rest/agile/1.0/*` and `https://{site}.atlassian.net/rest/servicedeskapi/*` | Board, sprint, backlog, request, customer, and queue payloads | Jira Software and Jira Service Management |
| `https://{site}.atlassian.net/wiki/api/v2/*` | Confluence page, space, comment, label, attachment metadata | Confluence Cloud |
| `https://api.atlassian.com/admin/*`, `https://api.atlassian.com/graphql`, and product GraphQL gateways | Organization, policy, graph, Compass, and app payloads | Cloud Admin, GraphQL, and Compass |
| `https://api.bitbucket.org/2.0/*` and `https://api.trello.com/1/*` | Repository, pull request, pipeline, board, list, card, and webhook data | Bitbucket Cloud and Trello |
| `https://api.statuspage.io/v1/*`, `https://api.opsgenie.com/*`, and `https://api.eu.opsgenie.com/*` | Incident, component, metric, alert, schedule, and on-call payloads | Statuspage and Opsgenie |

No other first-party Atlassian endpoints are targeted by default. If the user chooses a partner CLI, review that tool's own endpoints before using it.

## Security & Privacy

**Data that leaves your machine:**
- Only the Atlassian request payloads, identifiers, and auth material needed for the chosen product surface
- CLI and API requests sent to the declared Atlassian or explicitly chosen partner endpoints

**Data that stays local:**
- Only the defaults the user explicitly wants remembered in `~/atlassian/`
- Notes about whether the user prefers read-only, review-first, or bulk automation workflows

**This skill does NOT:**
- Ask for every Atlassian credential up front
- Read unrelated config files or third-party tokens
- Send data to undeclared endpoints
- Store raw tokens, API keys, or passwords in local memory
- Assume write permission just because read access works

## Trust

By using this skill, data is sent to Atlassian services and any explicitly chosen partner CLI.
Only install if you trust Atlassian and any partner tooling you decide to use.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `api` — General REST API patterns, pagination, and provider routing
- `http` — HTTP request construction, headers, and debugging
- `json` — JSON shaping, `jq`, and schema inspection
- `oauth` — OAuth flows, tokens, scopes, and refresh handling
- `webhook` — Webhook delivery, verification, and replay-safe handling

## Feedback

- If useful: `clawhub star atlassian`
- Stay updated: `clawhub sync`
