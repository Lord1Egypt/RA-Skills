# ChallanX API Reference

## Public endpoint

`https://challanx.in/openclaw/api`

## Typical curl patterns

### Info

```bash
curl -sS 'https://challanx.in/openclaw/api'
```

### Download video

```bash
curl -L -X POST 'https://challanx.in/openclaw/api' \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' \
  -o output.mp4
```

### Download audio

```bash
curl -L -X POST 'https://challanx.in/openclaw/api' \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","downloadMode":"audio","audioFormat":"mp3"}' \
  -o output.mp3
```

### Download image/media

```bash
curl -L -X POST 'https://challanx.in/openclaw/api' \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://www.instagram.com/p/EXAMPLE/"}' \
  -o media.bin
```

Prefer naming the output based on the actual returned content type.

## Custom JSON statuses

- `success`
- `download_ready`
- `picker_required`
- `failed`

## Response guidance

- downloadable media should come back as a file response
- info/picker/error should come back as JSON
- keep response docs short and practical
