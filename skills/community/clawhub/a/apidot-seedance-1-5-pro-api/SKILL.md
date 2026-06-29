---
name: apidot-seedance-1-5-pro-api
description: "Use APIDot for Seedance 1.5 Pro API workflows, including ByteDance Seedance 1.5 Pro, text-to-video API, image-to-video API, synchronized audio planning, first frame and last frame control, fixed camera video, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/seedance-1-5-pro
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Seedance 1.5 Pro API

Use APIDot as a Seedance 1.5 Pro-focused API surface for cinematic short video, text-to-video, image-to-video, synchronized-audio planning, first/last-frame control, polling, and webhook delivery.

This skill is for routing Seedance 1.5 Pro questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Seedance 1.5 Pro API integration with APIDot.
- Generate cinematic short videos from prompts, source images, or frame guidance.
- Use Seedance 1.5 Pro through APIDot for text-to-video or image-to-video workflows.
- Plan synchronized audio, fixed-camera behavior, first/last-frame control, polling, or webhook callbacks.
- Implement APIDot async Seedance 1.5 Pro jobs with task submission, task status polling, or webhook delivery.
- Find APIDot Seedance 1.5 Pro docs, model pages, or general APIDot examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Seedance 1.5 Pro Workflow

APIDot Seedance 1.5 Pro generation follows the shared async task pattern:

1. Choose the Seedance 1.5 Pro request mode from the current APIDot docs.
2. Submit the video generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Seedance 1.5 Pro task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Seedance 1.5 Pro model page | https://apidot.ai/models/seedance-1-5-pro |
| Build with Seedance 1.5 Pro | https://apidot.ai/docs/seedance-1-5-pro |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Seedance 1.5 Pro model routing, request planning, and async workflow notes.

For Seedance 1.5 Pro request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use `apidot-seedance-2-api` when the user asks specifically for Seedance 2.
- Use this skill when the user is specifically building with Seedance 1.5 Pro through APIDot.
- Ask which video task the user needs before choosing a model-specific example: text-to-video, image-to-video, synchronized audio, first/last-frame control, fixed-camera clip, storyboard draft, or social ad draft.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source image URLs before submitting workflows that depend on frame guidance.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Seedance 1.5 Pro model page: https://apidot.ai/models/seedance-1-5-pro
- Seedance 1.5 Pro docs: https://apidot.ai/docs/seedance-1-5-pro
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
