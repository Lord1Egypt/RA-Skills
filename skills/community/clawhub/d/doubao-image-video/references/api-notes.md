# API Notes

## Endpoints

- Image generation: `POST https://ark.cn-beijing.volces.com/api/v3/images/generations`
- Video generation: `POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`
- Video task query: `GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}`

## Environment variables

- `DOUBAO_API_KEY`: required
- `DOUBAO_IMAGE_ENDPOINT_ID`: optional default image endpoint id
- `DOUBAO_VIDEO_ENDPOINT_ID`: optional default video endpoint id
- `DOUBAO_DEFAULT_IMAGE_MODEL`: optional, default `doubao-seedream-4-5`
- `DOUBAO_DEFAULT_VIDEO_MODEL`: optional, default `doubao-seedance-1.0-lite-t2v`

## Image command

Supported flags:

- `--prompt` required
- `--endpoint-id` optional
- `--model` optional
- `--size` optional
- `--image-url` optional
- `--ref-image-url` repeatable
- `--req-key` optional
- `--watermark` optional

## Video command

Supported flags:

- `--prompt` required
- `--endpoint-id` optional
- `--model` optional
- `--video-duration` optional
- `--fps` optional
- `--resolution` optional
- `--first-frame-image-url` optional
- `--ref-image-url` repeatable
- `--req-key` optional

Behavior:

- Appends `--dur`, `--fps`, `--rs`, and `--ratio` to the prompt if missing.
- Uses ratio `16:9` for `720p`, otherwise `adaptive`.
- Returns JSON with the upstream response body.

## Wait and download

The `wait` subcommand supports:

- `--task-id`: required
- `--timeout`: max wait time in seconds, default `600`
- `--interval`: polling interval in seconds, default `5`
- `--download-to`: optional local output path; if the task succeeds and returns `content.video_url`, the file is downloaded automatically

## Important caveats

- Upstream documentation and implementation disagree on some defaults; this skill preserves the implementation-oriented behavior where practical.
- The script never prints secrets. It only emits structured JSON or concise errors.
