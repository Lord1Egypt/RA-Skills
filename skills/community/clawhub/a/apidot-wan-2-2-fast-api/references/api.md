# APIDot Wan 2.2 Fast Reference

This reference gives agents a safer, non-executable summary for APIDot Wan 2.2 Fast integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general APIDot examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/wan-2-2-fast
- API docs: https://apidot.ai/docs/wan-2-2-fast
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Wan 2.2 Fast on APIDot is for rapid short-video draft workflows that need prompt-to-video or image-to-video iteration, including one-image animation or simple two-image transitions when supported by the current docs.

Use later Wan-family skills when the user asks for Wan 2.5, Wan 2.6, Wan 2.7 Video, or Wan 2.7 Image. Use this skill when the request is specifically about Wan 2.2 Fast or quick draft iteration.

Documented Wan 2.2 Fast model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `wan2.2-text-to-video-fast` | Prompt-only fast video drafts through APIDot. |
| `wan2.2-image-to-video-fast` | Image-guided fast video drafts or simple transitions through APIDot. |

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants text-to-video, one-image animation, or a two-image transition.
- Whether source images are public, accessible, and appropriate for backend submission.
- Desired duration and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, request status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Wan 2.2 Fast jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submitting jobs that depend on image guidance.
- Keep request status, selected model, prompt metadata, media references, and final video URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Wan 2.2 Fast.
