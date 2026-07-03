---
name: apidot-kling-2-1-api
description: "Use APIDot for Kling 2.1 API workflows, including Kling 2.1 Standard, Kling 2.1 Pro, image-to-video API, start-frame guidance, optional end-frame control, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/kling-2-1
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Kling 2.1 API

Use APIDot as a Kling 2.1-focused API surface for image-to-video workflows, start-frame guided clips, optional end-frame planning, polling, and webhook delivery.

This skill is for routing Kling 2.1 questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Kling 2.1 API integration with APIDot.
- Generate short videos from source images.
- Use Kling 2.1 Standard or Kling 2.1 Pro through APIDot.
- Plan start-frame guidance, optional end-frame control, duration choice, polling, or webhook callbacks.
- Implement APIDot async Kling 2.1 jobs with task submission, task status polling, or webhook delivery.
- Find APIDot Kling 2.1 docs, model pages, or general APIDot examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Kling 2.1 Workflow

APIDot Kling 2.1 generation follows the shared async task pattern:

1. Choose the Kling 2.1 model entry and request mode from the current APIDot docs.
2. Submit the video generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Kling 2.1 task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Kling 2.1 model page | https://apidot.ai/models/kling-2-1 |
| Build with Kling 2.1 | https://apidot.ai/docs/kling-2-1 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Kling 2.1 model routing, request planning, and async workflow notes.

For Kling 2.1 variants and request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use this skill when the user is specifically building with Kling 2.1 through APIDot.
- Ask which video task the user needs before choosing a model-specific example: image-to-video, start-frame animation, end-frame transition, product teaser, character motion, or social clip.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source image URLs before submitting workflows that depend on reference media.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Kling 2.1 model page: https://apidot.ai/models/kling-2-1
- Kling 2.1 docs: https://apidot.ai/docs/kling-2-1
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
