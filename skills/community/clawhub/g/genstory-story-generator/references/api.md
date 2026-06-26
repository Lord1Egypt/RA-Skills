# Genstory Story Task API

Base site: `https://www.genstory.app`

## 1) Create API key

- User creates the key in the Genstory user center:
  - `https://www.genstory.app/api-keys`
- Save it as:

```bash
GENSTORY_API_KEY=sk-xxxxxxxxxxxxxxxx
```

## 2) Submit story task

`POST /api/v1/story-tasks`

Headers:

```http
Authorization: Bearer <GENSTORY_API_KEY>
Content-Type: application/json
```

Example body:

```json
{
  "prompt": "Create a non-fiction story about the life cycle of butterflies for kids.",
  "title": "The Butterfly Journey",
  "character_name": "Mila",
  "scenes_count": 6,
  "generation_type": "text",
  "generation_mode": "standard",
  "layout_mode": "default",
  "page_spec": "0.7:1",
  "public_visibility": true
}
```

Success response:

```json
{
  "success": true,
  "data": {
    "task_id": "task_uuid",
    "status": "pending",
    "polling_url": "/api/v1/story-tasks/task_uuid"
  }
}
```

## 3) Poll task

`GET /api/v1/story-tasks/{task_id}`

Success response while running:

```json
{
  "success": true,
  "data": {
    "task_id": "task_uuid",
    "status": "pending",
    "error": null,
    "story": null
  }
}
```

Success response when completed:

```json
{
  "success": true,
  "data": {
    "task_id": "task_uuid",
    "status": "success",
    "error": null,
    "story": {
      "id": "story_uuid",
      "title": "The Butterfly Journey",
      "url": "https://www.genstory.app/stories/the-butterfly-journey",
      "cover_url": "https://cdn.example.com/butterfly-cover.webp",
      "locale": "en"
    }
  }
}
```

## 4) Recommended client behavior

- Poll every `3-5` seconds.
- Stop after a reasonable timeout.
- Surface `data.error` when status is `failed`.
- In final UX, prioritize `story.url` and `story.cover_url`.
