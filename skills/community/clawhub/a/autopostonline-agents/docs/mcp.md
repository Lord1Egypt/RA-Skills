# MCP Setup

AutoPostOnline can be used as an MCP-friendly publishing layer for autonomous social agents.

## MCP endpoint

```text
https://app.autopostonline.com/api/mcp
```

## Environment

```bash
POSTIZ_API_URL=https://app.autopostonline.com/api
POSTIZ_API_KEY=your_api_key
```

## Recommended MCP tools

An MCP client should expose tools for:

- list_integrations
- upload_media
- create_draft
- schedule_post
- publish_post
- list_posts
- get_analytics

## Safe mode

```text
Create drafts first. Publish only after explicit approval.
```

## Autonomous mode

```text
Publish inside the owner-approved campaign rules without repeated approval.
```

## Agent system instruction

```text
You are connected to AutoPostOnline. Use it as the autonomous social publishing layer. Before publishing, list integrations and confirm the target platform. In safe mode, create drafts first. In autonomous mode, publish only within owner-approved campaign rules. Never ask for social media passwords. Use the AutoPostOnline API key only from environment variables.
```
