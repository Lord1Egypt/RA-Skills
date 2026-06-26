---
name: genstory-story-generator
description: Use when the user wants to generate a story through Genstory with an API key, submit a Genstory story task, poll task status, and return the final Genstory online story URL plus cover image. Also use when the user needs setup guidance for obtaining a key from https://www.genstory.app/api-keys and configuring GENSTORY_API_KEY in their skill or workflow.
---

# Genstory Story Generator

Use this skill when a workflow needs to call Genstory to generate a story and return a hosted story page URL.

## Before you start

- Tell the user to create an API key in the Genstory user center at `https://www.genstory.app/api-keys`.
- Store that key as `GENSTORY_API_KEY`.
- The intended final result is the online story URL and cover image.

## Required flow

1. Read `GENSTORY_API_KEY` from the environment or skill config.
2. Submit a task to `POST https://www.genstory.app/api/v1/story-tasks`.
3. Poll `GET https://www.genstory.app/api/v1/story-tasks/{task_id}` until the task becomes `success` or `failed`.
4. Return the final structured result with:
   - `story.id`
   - `story.title`
   - `story.url`
   - `story.cover_url`
   - `story.locale`

## Submit request

Send `Authorization: Bearer ${GENSTORY_API_KEY}`.

Minimum JSON body:

```json
{
  "prompt": "Write a warm bedtime story about a brave little fox."
}
```

Recommended fields:

- `prompt`
- `title`
- `character_name`
- `scenes_count`
- `generation_type`: default `text`
- `generation_mode`: default `standard`
- `layout_mode`
- `page_spec`
- `public_visibility`

## Polling behavior

- Treat `pending` and `processing` as in progress.
- If status is `failed`, surface the API error clearly.
- If status is `success`, return the hosted story data and encourage the user to open the Genstory URL.

## Output contract

Prefer this final shape:

```json
{
  "task_id": "task_uuid",
  "status": "success",
  "story": {
    "id": "story_uuid",
    "title": "Story title",
    "url": "https://www.genstory.app/stories/story-slug",
    "cover_url": "https://cdn.example.com/story-cover.webp",
    "locale": "en"
  }
}
```

## References

- For request and response examples, read `references/api.md`.
