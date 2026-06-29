# APIDot Seedance 2 Reference

This reference gives agents a safer, non-executable summary for APIDot Seedance 2 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or runnable GitHub examples.

This reference contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials. The optional submit helper lives separately at `scripts/submit_seedance_2.sh` and should only be used with a reviewed JSON payload from a trusted server-side environment.

## Source Of Truth

- Model page: https://apidot.ai/models/seedance-2
- API docs: https://apidot.ai/docs/seedance-2
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Runnable examples: https://github.com/APIDotAI/seedance-2-api
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Seedance 2 on APIDot is for video generation workflows that need prompt-driven clips, image-to-video, native audio behavior, multimodal references, and stronger continuity across short-form scenes when supported by the selected model mode.

Documented Seedance 2 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `seedance-2` | Final-quality Seedance 2 jobs and higher-resolution output when supported. |
| `seedance-2-fast` | Faster iteration before moving a validated workflow to the standard model entry. |

Do not assume every request mode is supported by every model entry. Check the APIDot Seedance 2 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants text-to-video, image-to-video, reference-image video, reference-video guidance, or reference-audio guidance.
- Whether native audio generation is part of the desired output.
- Whether the workflow uses first or last frame images, or multimodal reference fields.
- Desired aspect ratio, duration, and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, status, and final video URLs.

For copyable request shapes, open the APIDot docs or the Seedance 2 GitHub examples instead of recreating examples inside this skill.

## Script Boundary

The optional submit script is intentionally narrow:

- It accepts a reviewed JSON payload file path or reviewed JSON from standard input.
- It requires `APIDOT_API_KEY` in the server-side environment.
- It submits to the APIDot generation submit endpoint.
- It does not build payloads, poll task status, register webhooks, write local files, store credentials, or download generated videos.

Use the script only after confirming the payload matches the current APIDot Seedance 2 docs.

## Async Flow

APIDot Seedance 2 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate all source media URLs before submitting jobs that depend on images, videos, or audio references.
- Keep request status, selected model, prompt metadata, media references, and final result URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Seedance 2.
