---
name: apidot-wan-2-6-api
description: "Use APIDot for Wan 2.6 API workflows, including Wan 2.6 text-to-video API, image-to-video API, video-to-video API, multi-shot video, 720p and 1080p planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/wan-2-6
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Wan 2.6 API

Use APIDot as a Wan 2.6-focused API surface for text-to-video, image-to-video, video-to-video, multi-shot video planning, polling, and webhook delivery.

This skill is for routing Wan 2.6 questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Wan 2.6 API integration with APIDot.
- Generate videos from prompts, a source image, or one or more source videos.
- Use Wan 2.6 through APIDot for text-to-video, image-to-video, or video-to-video workflows.
- Plan multi-shot clips, resolution choices, polling, or webhook callbacks.
- Implement APIDot async Wan 2.6 jobs with task submission, task status polling, or webhook delivery.
- Find APIDot Wan 2.6 docs, model pages, or general APIDot examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Wan 2.6 Workflow

APIDot Wan 2.6 generation follows the shared async task pattern:

1. Choose the Wan 2.6 model entry and request mode from the current APIDot docs.
2. Submit the video generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Wan 2.6 task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Wan 2.6 model page | https://apidot.ai/models/wan-2-6 |
| Build with Wan 2.6 | https://apidot.ai/docs/wan-2-6 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Wan 2.6 model routing, request planning, and async workflow notes.

For Wan 2.6 variants and request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use this skill when the user is specifically building with Wan 2.6 through APIDot.
- Ask which video task the user needs before choosing a model-specific example: text-to-video, image-to-video, video-to-video, multi-shot clip, product teaser, storyboard draft, or social ad draft.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source image and video URLs before submitting workflows that depend on reference media.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Wan 2.6 model page: https://apidot.ai/models/wan-2-6
- Wan 2.6 docs: https://apidot.ai/docs/wan-2-6
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
