# APIDot Hailuo 02 Reference

This reference gives agents a safer, non-executable summary for APIDot Hailuo 02 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general APIDot examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/hailuo-02
- API docs: https://apidot.ai/docs/hailuo-02
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Hailuo 02 on APIDot is for short-form video generation workflows that need prompt-driven clips, optional first-frame guidance, optional first-and-last-frame guidance, and physics-aware motion planning when supported by the selected model mode.

Documented Hailuo 02 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `hailuo-02` | Standard Hailuo 02 video jobs through APIDot. |
| `hailuo-02-pro` | Pro Hailuo 02 video jobs when the current docs support the requested workflow. |

Do not assume Hailuo 2.3 fields apply to Hailuo 02. Check the APIDot Hailuo 02 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants prompt-only text-to-video, first-frame guidance, or first-and-last-frame guidance.
- Whether the workflow depends on one or two source image URLs.
- Desired duration and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Hailuo 02 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submitting jobs that depend on frame guidance.
- Keep request status, selected model, prompt metadata, media references, and final result URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Hailuo 02.
