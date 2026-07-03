# APIDot MiniMax Music 2.6 Reference

This reference gives agents a safer, non-executable summary for APIDot MiniMax Music 2.6 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/minimax-music-2-6
- API docs: https://apidot.ai/docs/minimax-music-2-6
- Music models: https://apidot.ai/models/music
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

MiniMax Music 2.6 on APIDot is for music and audio workflows such as song generation, instrumentals, lyrics-related flows, backing tracks, and final audio delivery when supported by the selected request mode.

Do not assume every music request mode is supported by every MiniMax Music 2.6 entry. Check the APIDot MiniMax Music 2.6 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants a full song, instrumental, backing track, lyrics workflow, or audio export guidance.
- Whether the prompt, style, vocal, language, duration, or source audio controls are relevant in the current APIDot docs.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, prompt metadata, request status, and final audio URLs.
- How the product should handle longer-running jobs, failed jobs, retries, and duplicate webhook delivery.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot MiniMax Music 2.6 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Keep request status, selected model, prompt metadata, audio references, and final audio URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, callback URLs, API keys, or generated audio URLs.
- Do not copy fields from another music model family unless the APIDot docs show the same field for MiniMax Music 2.6.
