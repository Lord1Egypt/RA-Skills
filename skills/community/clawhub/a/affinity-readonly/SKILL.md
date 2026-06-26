---
name: affinity-readonly
description: Read-only Affinity CRM access for analysis and memo prep. Use when you need to fetch Affinity companies, people, notes, opportunities, interactions, or relationship data via API and summarize it. Enforce GET-only operations, never perform writes, and never expose API keys.
---

# Affinity Read-Only

Use this skill for Affinity analysis tasks from chat or Slack.

## Hard rules

- Use GET requests only.
- Never call POST, PUT, PATCH, or DELETE.
- Never change stages, notes, tags, companies, or people.
- Never print, log, or echo `AFFINITY_API_KEY`.
- If a request requires modification, stop and ask for explicit approval.

## Prerequisite

- `AFFINITY_API_KEY` must be set in local environment.

Quick check:

```bash
zsh -lc '[[ -n "$AFFINITY_API_KEY" ]] && echo "AFFINITY_API_KEY is set" || echo "AFFINITY_API_KEY is not set"'
```

## API helper

Use the bundled script:

```bash
./skills/affinity-readonly/scripts/affinity_get.sh "/companies" "page_size=25"
./skills/affinity-readonly/scripts/affinity_get.sh "/persons" "term=Driven%20Plastics"
./skills/affinity-readonly/scripts/affinity_get.sh "/notes" "person_id=12345"
```

- Arg 1: endpoint path beginning with `/`
- Arg 2 (optional): query string without leading `?`
- Base URL defaults to `https://api.affinity.co` and can be overridden with `AFFINITY_API_BASE`

## Workflow

1. Confirm task is analysis-only.
2. Fetch only required records with `affinity_get.sh`.
3. Summarize evidence with IDs/timestamps when available.
4. If data appears incomplete, request clarifying filters (date range, company, person).
5. Refuse any write/update request unless user explicitly approves and policy is changed.
