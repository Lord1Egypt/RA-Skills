# Model notes

Prices change; read the current price on each model page before running paid jobs. Every request field is documented in the API reference at https://apiko.app/docs.

## Nano Banana 2.1 and Nano Banana Pro (image edit and generation)

- Model page: [Nano Banana 2.1](https://apiko.app/models/nano-banana-2.1), [Nano Banana Pro](https://apiko.app/models/nano-banana-pro)
- Endpoints: `POST /v1/images/generations` (text to image), `POST /v1/images/edits` with `images` (array of reference image URLs).
- `resolution`: `1k` (default), `2k`, `4k`. Each tier has its own price per image.
- Timing seen in production: a 2K edit takes about a minute; 4K is close to 2K at the median but one in ten 4K jobs takes over four minutes.
- Results may be JPEG or PNG; check the `Content-Type`.

## GPT Image 2.5 Sunburst, GPT Image 2.5 Flare, GPT Image 2

- Model page: [GPT Image 2.5 Sunburst](https://apiko.app/models/gpt-image-2.5-sunburst), [GPT Image 2.5 Flare](https://apiko.app/models/gpt-image-2.5-flare), [GPT Image 2](https://apiko.app/models/gpt-image-2)
- Endpoints: `POST /v1/images/generations`, `POST /v1/images/edits` (JSON body with `images`).
- `size`: an aspect ratio such as `1:1`, `16:9`, `3:2`, or one of the exact sizes listed in the model's API reference (e.g. `1024x1024`). Other pixel sizes are rejected before any charge.
- Prompt limit: 32,000 characters.

## Wan 3.0 (text, image and reference to video)

- Model pages: [Wan 3.0 text-to-video](https://apiko.app/models/wan3.0-text-to-video), [image-to-video](https://apiko.app/models/wan3.0-image-to-video), [reference-to-video](https://apiko.app/models/wan3.0-reference-video); Prime versions add `-prime-` to the id.
- Endpoint: `POST /v1/videos`; read the task with `GET /v1/videos/{id}` (`video_url`) or `GET /v1/tasks/{id}`.
- `duration`: 2–30 seconds. `resolution`: `480p`, `720p` (default), `1080p`. `aspect_ratio`: `adaptive`, `16:9`, `9:16`, `1:1`.
- Reference-to-video fields: `reference_image_urls` (up to 10), `reference_videos` (up to 5 clips, 1–15 s each, 15 s total), `reference_audios` (wav or mp3, not billed). In the prompt, call them "Image 1", "Video 1", "Audio 1" in the order sent.
- **Billing**: output seconds × the per-second price of the resolution. For reference-to-video, the length of the reference clips is added: 5 s of output with a 3 s reference clip bills 8 s. Submission temporarily holds 15 s per distinct reference clip and refunds the difference when the task finishes. Reference length plus `duration` must stay within 30 s.
- Timing: 480p short clips about 1.5–2 minutes; 1080p with references has taken from 4.5 to over 12 minutes. Poll with a deadline of 20 minutes or pass `callback_url`.

## Seedance 2.5, 2.0, 2.0 Fast, 2.0 Mini

- Model pages: [Seedance 2.5](https://apiko.app/models/seedance-2.5), [Seedance 2.0](https://apiko.app/models/seedance-2.0), [Seedance 2.0 Fast](https://apiko.app/models/seedance-2.0-fast), [Seedance 2.0 Mini](https://apiko.app/models/seedance-2.0-mini)
- Endpoint: `POST /v1/videos`. Billed per second of output by resolution. Check the model's API reference for its exact fields before sending.

## Seedream 5.0 Pro

- Model page: [Seedream 5.0 Pro](https://apiko.app/models/doubao-seedream-5-0-pro)
- Endpoint: `POST /v1/images/generations`. Priced per image.

## Uploading local reference images

`POST /v1/uploads/images` with the raw bytes of a JPEG, PNG or WebP (up to 10 MB) and its `Content-Type`. It is free, returns a public `url`, and the file is kept for 72 hours. Anyone with the URL can open it.
