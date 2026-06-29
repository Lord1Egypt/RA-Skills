# APIDot GPT Image 2 Reference

This reference gives agents a safer, non-executable summary for APIDot GPT Image 2 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or GitHub examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/gpt-image-2
- API docs: https://apidot.ai/docs/gpt-image-2
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Model examples: https://github.com/APIDotAI/gpt-image-2-api
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

GPT Image 2 on APIDot is for image generation and editing workflows that need strong prompt following, visual composition control, image references, and explicit handling of text or product details when supported by the selected model mode.

Documented GPT Image 2 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `gpt-image-2` | Prompt-only text-to-image generation without reference images. |
| `gpt-image-2-edit` | Image editing or reference-guided generation with one or more source images. |

Do not assume every request mode is supported by every model entry. Check the APIDot GPT Image 2 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants prompt-only generation, image editing, image-to-image, product visuals, UI mockups, ad creative, or reference-guided generation.
- Whether source image URLs are involved. If they are, verify that the selected GPT Image 2 model entry supports reference images.
- Desired aspect ratio, quality, and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, source media references, request status, and final image URLs.

For copyable request shapes, open the APIDot docs or the GPT Image 2 GitHub examples instead of recreating examples inside this skill.

## Async Flow

APIDot GPT Image 2 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate all source image URLs before submitting jobs that depend on references.
- Keep request status, selected model, prompt metadata, media references, and final image URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private image URLs, callback URLs, API keys, or generated image URLs.
- Do not copy fields from another image model family unless the APIDot docs show the same field for GPT Image 2.
