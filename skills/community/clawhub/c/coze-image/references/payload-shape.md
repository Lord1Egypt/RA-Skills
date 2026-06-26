# Coze Image Skill Payload

## Success

```json
{
  "image": "data:image/png;base64,AAAA...",
  "mime_type": "image/png",
  "filename": "generated-image.png",
  "source_url": "https://..."
}
```

## Failure

```json
{
  "error": "Image URL not found in SSE response. Upstream assistant replied: ...",
  "image": null,
  "mime_type": null,
  "filename": null,
  "source_url": null
}
```
