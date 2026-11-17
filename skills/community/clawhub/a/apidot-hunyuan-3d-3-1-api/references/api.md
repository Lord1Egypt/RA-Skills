# APIDot Hunyuan 3D 3.1 Reference

Use this non-executable reference to choose the current APIDot Hunyuan 3D 3.1 variant and documentation path before implementation.

It contains no shell commands, runnable request examples, bundled clients, or stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/hunyuan-3d-3-1
- API docs: https://apidot.ai/docs/hunyuan-3d-3-1
- 3D models: https://apidot.ai/models/3d
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- General examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model IDs, supported fields, limits, availability, and commercial terms.

## Model Family

Hunyuan 3D 3.1 on APIDot provides Pro and Rapid variants for text-to-3D and image-to-3D. Pro is intended for stronger control and supports additional options in selected image workflows; Rapid is intended for faster drafts.

Do not assume every control works across all four variants. Check the live docs before preparing inputs.

## Request Planning

Before planning a request, identify:

- Whether the source is a text prompt or a primary image.
- Whether Pro or Rapid fits the quality, speed, and control requirements.
- Whether multi-view image guidance is needed and supported by the selected variant.
- Whether PBR or geometry-oriented output is required and compatible with the selected mode.
- Whether polling is sufficient for testing or webhook delivery is needed for production.
- Where the backend will persist `task_id`, selected model, source references, status, and final asset URLs.

Open the live APIDot docs for exact variant rules and copyable request shapes.

## Async Flow

1. Select the current Hunyuan 3D 3.1 variant in the live docs.
2. Validate prompt or image inputs and variant-specific controls.
3. Submit through the documented APIDot generation flow.
4. Store `data.task_id` before retries, page transitions, or status checks.
5. Poll status for local tests and use `callback_url` for production asset pipelines.
6. Treat webhook delivery as idempotent.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submission.
- Keep request status, model variant, input references, control metadata, and final asset URLs together.
- Retry transient failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, image URLs, callback URLs, API keys, or generated asset URLs.
