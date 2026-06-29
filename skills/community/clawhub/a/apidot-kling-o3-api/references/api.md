# APIDot Kling O3 Reference

This reference gives agents a safer, non-executable summary for APIDot Kling O3 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general APIDot examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/kling-o3
- API docs: https://apidot.ai/docs/kling-o3
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Kling O3 on APIDot is for flexible short-form video workflows that need prompt-driven clips, image guidance, reference-guided generation, multi-shot structure, Native Audio, and higher-control variant selection when supported by the selected model mode.

Documented Kling O3 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `kling-o3/standard` | General Kling O3 video iteration and broad request-mode coverage. |
| `kling-o3/pro` | Higher-fidelity Kling O3 jobs when the user needs stronger visual output. |
| `kling-o3/4K` | High-resolution Kling O3 work when current APIDot docs support that mode. |

Do not assume every request mode is supported by every model entry. Check the APIDot Kling O3 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants text-to-video, image-to-video, or reference-guided video.
- Whether the clip needs one scene, multi-shot structure, or a specific camera/motion plan.
- Whether Native Audio is part of the desired output.
- Desired resolution, duration, aspect ratio, and model variant, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Kling O3 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image and reference media URLs before submitting jobs that depend on external media.
- Keep request status, selected model, prompt metadata, media references, and final result URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Kling O3.
