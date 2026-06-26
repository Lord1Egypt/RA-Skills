# Figma REST API Reference

Base URL: `https://api.figma.com/v1`
Auth header: `X-Figma-Token: <token>`

## Endpoints

### File Operations

| Action | Method | Path | Skill command |
|--------|--------|------|---------------|
| Get file | GET | `/files/{key}` | `figma_client.mjs get-file {key}` |
| Get file nodes | GET | `/files/{key}/nodes?ids={ids}` | `figma_client.mjs get-file-nodes {key} {ids}` |
| Get file metadata | GET | `/files/{key}/meta` | `figma_client.mjs get-metadata {key}` |
| Get file versions | GET | `/files/{key}/versions` | `figma_client.mjs get-versions {key}` |
| Get file styles | GET | `/files/{key}/styles` | `figma_client.mjs get-styles {key}` |
| Get file components | GET | `/files/{key}/components` | `figma_client.mjs get-components {key}` |
| Get image fills | GET | `/files/{key}/images` | `figma_client.mjs get-image-fills {key}` |

### Image Export

| Action | Method | Path | Skill command |
|--------|--------|------|---------------|
| Render images | GET | `/images/{key}?ids={ids}&format={fmt}&scale={s}` | `figma_client.mjs render-images {key} {id} --format png --scale 2` |

### User

| Action | Method | Path | Skill command |
|--------|--------|------|---------------|
| Me | GET | `/me` | `figma_client.mjs me` |

## File Key

From a Figma share URL:
```
https://www.figma.com/design/ABC123xyz/My-Project
                            ^^^^^^^^
                            file key
```

## Rate Limiting

- Free tier: ~60 requests/minute
- Professional: higher limits
- The skill scripts include retry logic with exponential backoff

## Plugin API (for write operations)

The local WebSocket connector + plugin uses Figma's Plugin API internally.
See: https://www.figma.com/plugin-docs/api/api-overview/
