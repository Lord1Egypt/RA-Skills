# HTTP Contract

## Health

`GET /healthz`

```json
{
  "status": "ok",
  "backend": "codex-exec",
  "model": "gpt-image-2",
  "output_dir": "/absolute/path"
}
```

## Capabilities

`GET /v1/capabilities`

Return the model, supported output formats, quality options, max images, ratio options, size options, and size constraints.

Important values:

- `model`: `gpt-image-2`
- `max_images`: `4`
- `qualities`: `auto`, `high`, `medium`, `low`
- `references.mode`: `original_image`
- `size_constraints.max_edge`: `3840`
- `size_constraints.multiple_of`: `16`

## Generate

`POST /v1/images/generate`

```json
{
  "prompt": "red product poster",
  "count": 4,
  "size": "1024x1024",
  "quality": "high",
  "aspect": "1:1",
  "output_format": "png",
  "references": [
    {
      "label": "visible layer",
      "image": "data:image/png;base64,..."
    }
  ]
}
```

Response:

```json
{
  "status": "completed",
  "backend": "codex-exec",
  "model": "gpt-image-2",
  "requested_size": "1024x1024",
  "quality": "high",
  "data": [
    {
      "id": "codex-...",
      "label": "生成图",
      "mime_type": "image/png",
      "path": "/absolute/output.png",
      "resolved_size": "1024x1024",
      "url": "http://127.0.0.1:17341/v1/images/codex-.../file"
    }
  ]
}
```

## Image File

`GET /v1/images/:id/file`

Return the generated image bytes with the correct image content type.

## Cancellation

The server must abort work when:

- the caller aborts the request,
- the socket closes before completion,
- the configured timeout is reached,
- one worker fails during a multi-image request.

On macOS and Linux, start `codex exec` with `detached: true` and kill the negative process id so child processes do not remain alive.
