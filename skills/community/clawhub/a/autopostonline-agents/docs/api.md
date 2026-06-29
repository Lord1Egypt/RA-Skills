# API Reference

AutoPostOnline exposes agent-friendly API access for social publishing workflows.

## Base URL

```text
https://app.autopostonline.com/api
```

## Authentication

Preferred:

```http
Authorization: Bearer <api_key>
```

Fallback:

```http
Authorization: <api_key>
```

## Important endpoints

### List integrations

```http
GET /public/v1/integrations
```

Use before drafting, scheduling, or publishing.

### Upload media

```http
POST /public/v1/media
```

Use when a post needs images or videos.

### Create post or draft

```http
POST /public/v1/posts
```

Use for draft, scheduled, or publish workflows depending on the supported API fields.

### List posts

```http
GET /public/v1/posts
```

Use for scheduled, draft, and published post status.

## Agent rules

- Always know the connected integrations.
- Avoid publishing to the wrong destination.
- Use safe mode by default.
- Use autonomous mode only inside owner-approved campaign rules.
- Respect platform limits and tone.
- Never expose the API key.
- Report failures clearly.
