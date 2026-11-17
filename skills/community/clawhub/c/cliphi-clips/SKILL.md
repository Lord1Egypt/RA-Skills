---
name: cliphi-clips
description: >
  Turns the user's long videos into ready-to-post vertical clips with
  captions and branding, using the Cliphi API. Use this skill when the user
  wants to clip a video, make Shorts / TikToks / Reels from a YouTube video,
  podcast, livestream or Twitch VOD, find viral moments in a video, or
  repurpose long video into short clips.
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - CLIPHI_API_KEY
---

# Cliphi: video in, ready-to-post clips out

Cliphi processes a public video URL, finds the strongest moments, and
renders vertical clips with captions and the user's saved branding.
Submitting a job bills a small per-minute processing charge. Previews are
free. Rendering is the discretionary spend; every render reports its exact
cost, and you are billed only when the clip completes.

Base URL: `https://www.cliphi.com/api/v1`
Auth: `Authorization: Bearer $CLIPHI_API_KEY` (keys look like `chp_live_...`;
the user creates one at https://www.cliphi.com/studio/settings/api-keys).
Full API reference: https://www.cliphi.com/cliphi-actions.json

## The three rules (never break these)

1. **Previews first.** Always show the free `preview_page_url` links and get
   an explicit pick from the user before rendering anything.
2. **Renders cost credits.** Never render unprompted, never render "all of
   them" without an explicit confirmation, and state the cost once from the
   render response's `estimated_credits`.
3. **Relay `message` verbatim.** Success and error responses carry a
   `message` written to be shown to a human. HTTP error bodies are
   `{"detail": {"error_code", "message", "billed"}}` (at least these keys;
   422s add an `errors` list). In an HTTP error body, `billed` says whether
   money moved, and it is always false on request errors.

## Workflow checklist

### 1. Submit

```bash
curl -X POST https://www.cliphi.com/api/v1/jobs \
  -H "Authorization: Bearer $CLIPHI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

Optional fields: `instructions` (plain-language detection guidance in the
user's own words, e.g. `"only the product demo moments"`, max 500 chars),
`quality` (`"720p"`|`"1080p"`), `start_time`/`end_time` (seconds),
`language` (ISO 639-1), `force_new` (starts a fresh billed job even when one
is in flight, only with explicit user approval).

The response returns in ~2s with `job_id`, `status_url` (a relative path,
prepend the base URL), `studio_url` and a `message` to relay. Tell the user
processing takes a few minutes and that Cliphi also emails them when clips
are ready, unless they have turned notifications off. Offer `studio_url` as
the live progress page. If `already_running` is true, this video already has
a job in flight and nothing new was charged. Resubmitting a video whose job
already FINISHED starts and bills a new job. Confirm that with the user
first.

### 2. Poll (in the background, do not block the conversation)

```bash
curl https://www.cliphi.com/api/v1/jobs/$JOB_ID \
  -H "Authorization: Bearer $CLIPHI_API_KEY"
```

- Wait `poll_after_seconds` between polls.
- Branch on the `status` FIELD (`processing` | `completed` | `failed`):
  a failed job arrives inside a successful HTTP response.
- `?wait=40` long-polls server-side (values under 3 behave as 0).
- While processing, `phase_label` + `eta_seconds` narrate progress; relay
  `message` when the user asks.

### 3. Present the moments

When `status` is `completed`, show `moments[]` as a numbered list: `title`,
`viral_score`, and the `preview_page_url` labelled "Watch preview" (free,
it already shows the finished look with captions and branding; on a rare
signing failure the field can be null, skip the link, keep the moment).
Moments already rendered in the wanted aspect ratio have it in
`rendered_aspect_ratios`. Link the existing clip from `clips[]` instead of
re-rendering; it is already paid for. A different aspect ratio is a new
billed render.

Ask which ones to render. Never decide for the user.

### 4. Render the picks (billed)

```bash
curl -X POST https://www.cliphi.com/api/v1/jobs/$JOB_ID/moments/$MOMENT_ID/render \
  -H "Authorization: Bearer $CLIPHI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"aspect_ratio": "9:16"}'
```

- Aspect ratios: `9:16` (default), `4:5`, `1:1`, `16:9`. Note: `16:9` only
  renders when the user's saved 16:9 style has captions, overlays, or a
  crop on; otherwise the API refuses with `nothing_to_render` because the
  result would equal the free preview.
- State the cost once from `estimated_credits` in the response.
- `status: "already_rendered"` means an existing clip came back free.
- `force: true` re-renders (billed again), only with explicit approval.
- Then poll the job (`wait=40`) until that moment's `render_status` is
  `rendered` (deliver the clip URL from `clips[]`; `billed_credits` on the
  clip is the receipt) or `failed` (relay `render_error` and stop;
  `render_error_code` says why: `insufficient_credits`, `source_expired`,
  `render_interrupted` (safe to POST render again), `render_failed`).
  A failed render makes no billing claim. Do not tell the user nothing was
  charged; point them at `studio_url` or support if they ask.

### 5. Hand over

Deliver the clip URLs and `studio_url`. The studio is where the user edits
further and publishes. Never publish anywhere yourself.

## No key yet? Show the demo

```bash
curl https://www.cliphi.com/api/v1/demo
```

Keyless and free: a real finished job in the exact job shape, with live
preview pages. Show it, then point the user at
https://www.cliphi.com/studio/settings/api-keys.

## Error handling

Relay `detail.message` verbatim, it states the fix. Stable `error_code`
values include `missing_api_key`, `invalid_api_key`, `insufficient_credits`
(message includes balance, required amount and the top-up link),
`video_too_long`, `throttled`, `maintenance`, `job_not_found`,
`moment_not_ready`, `nothing_to_render`, `access_denied`, `source_expired`,
`clip_too_long`, `render_in_progress`. `detail.billed` is false on every
request error, nothing was charged.

## Boundaries

- Only ever call `https://www.cliphi.com` endpoints. This skill installs
  nothing, runs no scripts, and needs no dependencies.
- The API spends the user's Cliphi credits; a revoked key stops it
  instantly.
- Only clip content the user owns or has the rights to use.
- Keep a human in the loop before anything gets posted publicly.
