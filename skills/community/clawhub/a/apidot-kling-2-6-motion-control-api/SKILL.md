---
name: apidot-kling-2-6-motion-control-api
description: "Use APIDot for Kling 2.6 Motion Control API workflows, including motion transfer, reference video to character animation, image-to-video API, reference-to-video API, dance transfer, action transfer, controllable animation, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/kling-2-6-motion-control
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Kling 2.6 Motion Control API

Use APIDot as a Kling 2.6 Motion Control-focused API surface for transferring motion from a reference video onto a character image, controllable character animation, dance transfer, action transfer, polling, and webhook delivery.

This skill is for routing Kling 2.6 Motion Control questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Kling 2.6 Motion Control API integration with APIDot.
- Transfer motion from a reference video to a character image.
- Create dance transfer, action transfer, storyboard preview, ad creative, or controllable character animation workflows.
- Use Kling 2.6 Motion Control through APIDot for reference-to-video or image-to-video style workflows.
- Implement APIDot async motion-control jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Kling 2.6 Motion Control docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Kling 2.6 Motion Control Workflow

APIDot Kling 2.6 Motion Control generation follows the shared async task pattern:

1. Choose the Kling 2.6 Motion Control request mode from the current APIDot docs.
2. Prepare the character image and reference video according to the documented media requirements.
3. Submit the motion-control request through the documented APIDot async generation flow.
4. Save the returned `data.task_id` immediately.
5. Poll task status with the documented task status API for local tests.
6. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
7. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Kling 2.6 Motion Control task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Kling 2.6 Motion Control model page | https://apidot.ai/models/kling-2-6-motion-control |
| Build with Kling 2.6 Motion Control | https://apidot.ai/docs/kling-2-6-motion-control |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Kling 2.6 Motion Control request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another Kling or video model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Kling 2.6 Motion Control model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use `apidot-kling-2-6-api` when the user needs general Kling 2.6 text-to-video or image-to-video guidance.
- Use `apidot-kling-3-0-motion-control-api` when the user asks specifically for Kling 3.0 Motion Control.
- Use this skill when the user is specifically building a Kling 2.6 motion transfer or controllable character animation workflow through APIDot.
- Ask which motion task the user needs before choosing a model-specific example: dance transfer, action transfer, product demo, storyboard preview, character animation, or ad creative.
- Persist `task_id`, selected model, user ID, character image reference, motion video reference, request status, and final video URLs together.
- Validate source image and reference video URLs before submitting workflows that depend on external media.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Kling 2.6 Motion Control model page: https://apidot.ai/models/kling-2-6-motion-control
- Kling 2.6 Motion Control docs: https://apidot.ai/docs/kling-2-6-motion-control
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
