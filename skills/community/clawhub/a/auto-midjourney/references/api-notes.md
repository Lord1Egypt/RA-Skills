# Midjourney Alpha API Notes

This skill is based on the browser flow observed on `https://alpha.midjourney.com/`.

## Confirmed request

- Method: `POST`
- URL: `https://alpha.midjourney.com/api/submit-jobs`
- Content type: `application/json`
- Important headers:
  - `cookie: <authenticated session cookie>`
  - `origin: https://alpha.midjourney.com`
  - `referer: https://alpha.midjourney.com/explore?tab=hot`
  - `x-csrf-protection: 1`
  - `x-mj-traceparent: <trace id>`

## Confirmed payload shape

```json
{
  "f": {
    "mode": "fast",
    "private": true
  },
  "channelId": "singleplayer_<uuid>",
  "metadata": {
    "isMobile": null,
    "imagePrompts": 0,
    "imageReferences": 0,
    "characterReferences": 0,
    "depthReferences": 0,
    "lightboxOpen": null
  },
  "t": "imagine",
  "prompt": "1 girl --ar 16:9 --raw --v 8"
}
```

## Confirmed response shape

```json
{
  "success": [
    {
      "job_id": "<uuid>",
      "prompt": "1 girl --ar 16:9 --raw --v 8.0",
      "is_queued": false,
      "softban": false,
      "event_type": "diffusion",
      "job_type": "v8_diffusion",
      "flags": {
        "mode": "fast",
        "visibility": "stealth"
      },
      "meta": {
        "height": 816,
        "width": 1456,
        "batch_size": 4,
        "parent_id": null,
        "parent_grid": null
      }
    }
  ],
  "failure": []
}
```

## Unknowns to capture next

1. Final job-status endpoint
2. Result image URLs and field names
3. Upscale / variation button-action endpoints
4. Reference-image upload endpoints

## Experimental recent-jobs endpoint

Public GitHub reverse-engineering notes indicate a recent-jobs endpoint at:

```text
https://www.midjourney.com/api/app/recent-jobs/
```

Typical query parameters seen in community tooling include:

- `userId`
- `page`
- `amount`
- `orderBy`
- optional `jobStatus`
- optional `jobType`

This skill exposes that path as an experimental helper. It may change without notice.

## Confirmed user-state endpoint

- Method: `GET`
- URL: `https://alpha.midjourney.com/api/user-mutable-state`
- Purpose: returns current web settings and user flags

Example fields observed:

```json
{
  "settings": {
    "speed": "fast",
    "visibility": "stealth"
  },
  "macros": {
    "Richard": "https://cdn.discordapp.com/attachments/..."
  },
  "abilities": 31457284
}
```

This is useful for reading defaults, but it is not a job result endpoint.

## Observed telemetry endpoints

### Proxima metrics

- Method: `POST`
- URL: `https://proxima.midjourney.com/`
- Observed header: `x-metrics-token`
- Observed purpose: event ingestion for web analytics / metrics

Example event types:

- `WEB_GENERATE`

The current skill does not need this endpoint to submit `imagine` jobs.

### Trace ingestion

- Method: `POST`
- URL: `https://alpha.midjourney.com/api/v1/traces`
- Observed purpose: lifecycle tracing for client observability

Observed trace attributes included:

- `job.job_id`
- `job.model_version`
- `job.submission_type`
- `job.speed`

This can confirm that a job existed, but it is still not a replacement for a true job-status or result endpoint.

## Capture checklist

When extending this skill, collect one HAR or request sample for each new action:

1. `imagine` submit
2. job status poll
3. final image open/download
4. upscale
5. variation

Strip live cookies before storing samples in the repo.
