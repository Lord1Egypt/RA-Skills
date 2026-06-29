# AutoPostOnline Agent Operating Guide

This file tells autonomous agents how to operate with AutoPostOnline.

## Core idea

AutoPostOnline is the publishing layer for autonomous agents.

The agent does not own social accounts. The human or company owns the account, billing, and permissions. The agent receives a publishing key and operates inside the approved rules.

```text
Human-owned accounts.
Agent-operated publishing.
```

## What agents can do

Agents can:

- list connected social accounts
- generate platform-specific posts
- upload images or videos
- create drafts
- schedule posts
- publish approved or autonomous posts
- retrieve analytics
- run recurring campaigns
- operate marketing workflows

## What agents should not do

Agents should not:

- ask for social passwords
- store user social tokens
- publish outside the approved campaign scope
- post sensitive private information
- create spam
- hide failures
- claim a post was published if it was only drafted
- log API keys

## Default configuration

```bash
POSTIZ_API_URL=https://app.autopostonline.com/api
POSTIZ_API_KEY=your_api_key
```

## MCP endpoint

```text
https://app.autopostonline.com/api/mcp
```

## Default autonomous loop

1. List integrations.
2. Read the campaign goal.
3. Confirm owner-approved channels.
4. Draft platform-specific content.
5. Schedule or publish according to mode.
6. Report status.
7. Read analytics.
8. Improve the next cycle.

## Good autonomous behavior

A good AutoPostOnline agent is:

- clear about destination channels
- careful with live publishing
- autonomous only inside approved rules
- concise in status updates
- platform-aware
- secure with API keys
- honest about failures
- useful to founders, agencies, operators, and agent marketplaces
