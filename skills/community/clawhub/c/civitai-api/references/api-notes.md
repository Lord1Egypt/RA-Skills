# Civitai Public REST API notes

## Base URLs

- REST base: `https://civitai.com/api/v1`
- Model downloads: `https://civitai.com/api/download/models/{modelVersionId}`
- Public docs: `https://developer.civitai.com/docs/api/public-rest`

## Auth

Use either:

- `Authorization: Bearer <token>` for normal API requests
- `?token=<token>` on download URLs

Prefer the header for JSON API calls. Use the query token only when constructing a direct download URL.

## Useful endpoints

- `GET /models` — search/list models
- `GET /models/{modelId}` — full model details
- `GET /model-versions/{modelVersionId}` — version details
- `GET /model-versions/by-hash/{hash}` — reverse lookup by file hash
- `GET /creators` — creator listing/search
- `GET /images` — image listing/search
- `GET /tags` — tag listing/search
- `GET /api/download/models/{modelVersionId}` — direct download endpoint

## Common filters

The docs/examples show these as common query inputs depending on endpoint:

- `query`
- `limit`
- `page`
- `sort`
- `period`
- `tag`
- `username`
- `types`
- `nsfw`
- `modelId`
- `modelVersionId`
- `postId`

## Response shape patterns

Expect paginated list endpoints to return objects with items and paging metadata. Model and version detail endpoints return a single object. Large fields often include nested stats, creator info, tags, files, images, and download URLs.

## Workflow hints

1. Start with `/models` when the user knows a name or concept but not an id.
2. Use `/models/{id}` to inspect versions, file hashes, tags, and images.
3. Use `/model-versions/{id}` when the user already has a version id.
4. Use `/model-versions/by-hash/{hash}` to identify a local checkpoint or LoRA file.
5. Use `/api/download/models/{versionId}` when the user wants a real file URL.

## Safety / hygiene

- Keep the token in `.env` as `CIVITAI_API_KEY`; do not hard-code it into the skill.
- Treat download links with embedded `?token=` as sensitive.
- Avoid echoing secrets back to chat unless the user explicitly asks.
