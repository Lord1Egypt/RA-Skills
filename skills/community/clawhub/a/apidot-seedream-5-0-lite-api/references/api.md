# APIDot Seedream 5.0 Lite Reference

This reference gives agents a safer, non-executable summary for APIDot Seedream 5.0 Lite integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general APIDot examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/seedream-5-0-lite
- API docs: https://apidot.ai/docs/seedream-5-0-lite
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Seedream 5.0 Lite on APIDot is for image generation and editing workflows that need prompt-driven output, reference-guided edits, structured layouts, and multi-reference planning when supported by the current docs.

The documented APIDot model entry is:

| Model Entry | Best Fit |
| --- | --- |
| `seedream-5.0-lite` | Seedream 5.0 Lite image generation and editing jobs through APIDot. |

Do not assume Seedream 4.5 fields apply to Seedream 5.0 Lite. Check the APIDot Seedream 5.0 Lite docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants prompt-based image generation or reference-guided image editing.
- Whether the workflow depends on one or more source image URLs.
- Desired size, output count, or layout constraints, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, status, and final image URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Seedream 5.0 Lite jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submitting jobs that depend on reference-guided editing.
- Keep request status, selected model, prompt metadata, media references, and final result URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private image URLs, callback URLs, API keys, or generated image URLs.
- Do not copy fields from another image model family unless the APIDot docs show the same field for Seedream 5.0 Lite.
