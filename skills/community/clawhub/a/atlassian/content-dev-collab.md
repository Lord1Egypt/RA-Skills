# Confluence, Bitbucket, and Trello

## Confluence Cloud REST API v2

Base URL:
`https://{site}.atlassian.net/wiki/api/v2`

Use for:
- pages, blog posts, spaces, labels, comments
- attachments and content metadata
- content tree navigation and search-adjacent reads

Quick example:
```bash
curl -s "https://<site>.atlassian.net/wiki/api/v2/pages?limit=25" \
  -u "<email>:<api_token>" \
  -H "Accept: application/json"
```

Confluence gotchas:
- Cloud URLs need `/wiki/`.
- Body representations and editor formats are not interchangeable by guesswork.
- Space keys, page IDs, and parent IDs matter more than titles.

## Bitbucket Cloud REST API

Base URL:
`https://api.bitbucket.org/2.0`

Use for:
- repositories, branches, and commits
- pull requests, comments, and approvals
- pipelines, downloads, webhooks, and workspace automation

Quick example:
```bash
curl -s "https://api.bitbucket.org/2.0/repositories/<workspace>/<repo>/pullrequests" \
  -H "Authorization: Bearer <bitbucket_token>"
```

Bitbucket gotchas:
- Access tokens, app passwords, and OAuth are all valid but not interchangeable.
- Many resources use slugs while others expose UUIDs with braces.
- Pagination follows `next` and `pagelen`, not Jira-style `startAt`.

## Trello REST API

Base URL:
`https://api.trello.com/1`

Use for:
- boards, lists, cards, checklists, labels
- members, actions, search, batch, and webhooks

Quick example:
```bash
curl -s "https://api.trello.com/1/boards/<board_id>/cards?key=<trello_key>&token=<trello_token>"
```

Trello gotchas:
- Trello auth typically lives in query params.
- IDs are safer than names for boards, lists, labels, and cards.
- Webhook callback URLs must be public HTTPS URLs.
- Rate limits are tight enough that batch and backoff matter.

## Official Docs

- Confluence: https://developer.atlassian.com/cloud/confluence/rest/v2/intro/
- Bitbucket: https://developer.atlassian.com/cloud/bitbucket/rest/intro/
- Trello: https://developer.atlassian.com/cloud/trello/rest/
