# APIDot Generate Music Reference

This reference gives agents a safer, non-executable summary for APIDot Generate Music integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/generate-music
- API docs: https://apidot.ai/docs/generate-music
- Music detail docs: https://apidot.ai/docs/music-detail
- Music models: https://apidot.ai/models/music
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, pricing, and commercial terms.

## Model Family

Generate Music on APIDot is for prompt-driven music workflows such as full songs, instrumentals, vocal music, background music, and audio result delivery when supported by the selected request mode.

Do not assume every music option is supported by every request mode. Check the APIDot Generate Music docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants a full song, instrumental, vocal track, background loop, or music detail lookup.
- Whether prompt, style, lyric, vocal, language, version, duration, or callback_url controls are relevant in the current APIDot docs.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, prompt metadata, request status, and final audio URLs.
- How the product should handle longer-running jobs, failed jobs, retries, and duplicate webhook delivery.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Generate Music jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status or music detail polling for local tests and debugging.
5. Use callback_url or webhook delivery for production jobs that may outlive the current browser session.
6. Treat callback_url handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Keep request status, selected model, prompt metadata, audio references, and final audio URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, callback_url values, webhook payloads, API keys, or generated audio URLs.
- Do not copy fields from another music model family unless the APIDot docs show the same field for Generate Music.
