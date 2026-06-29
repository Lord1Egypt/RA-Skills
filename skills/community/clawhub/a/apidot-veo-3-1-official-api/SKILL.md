---
name: apidot-veo-3-1-official-api
description: "Use APIDot for Veo 3.1 Official API workflows, including Google Veo 3.1 Official, veo3.1-fast-official, veo3.1-lite-official, veo3.1-quality-official, text-to-video API, image-to-video API, first frame and last frame control, reference video, native audio, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/veo-3-1-official
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Veo 3.1 Official API

Use APIDot as a Veo 3.1 Official-focused API surface for Google video generation, text-to-video, image-guided video, first/last-frame control, reference workflows, native audio planning, polling, and webhook delivery.

This skill is for routing Veo 3.1 Official questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Veo 3.1 Official API integration with APIDot.
- Generate videos from prompts, source images, first/last frame images, or reference media.
- Use `veo3.1-fast-official`, `veo3.1-lite-official`, or `veo3.1-quality-official` through APIDot.
- Plan native audio behavior, reference guidance, resolution choices, polling, or webhook callbacks.
- Implement APIDot async Veo 3.1 Official jobs with task submission, task status polling, or webhook delivery.
- Find APIDot Veo 3.1 Official docs, model pages, or general APIDot examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Veo 3.1 Official Workflow

APIDot Veo 3.1 Official generation follows the shared async task pattern:

1. Choose the Veo 3.1 Official model entry and request mode from the current APIDot docs.
2. Submit the video generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Veo 3.1 Official task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Veo 3.1 Official model page | https://apidot.ai/models/veo-3-1-official |
| Build with Veo 3.1 Official | https://apidot.ai/docs/veo-3-1-official |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Veo 3.1 Official model routing, request planning, and async workflow notes.

For Veo 3.1 Official variants and request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use `apidot-veo-3-1-api` when the user asks for the broader Veo 3.1 API family.
- Use this skill when the user specifically asks for Veo 3.1 Official model entries through APIDot.
- Ask which video task the user needs before choosing a model-specific example: text-to-video, image-to-video, first/last-frame video, reference-guided video, native audio, storyboard clip, or product teaser.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source image and reference media URLs before submitting workflows that depend on external media.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Veo 3.1 Official model page: https://apidot.ai/models/veo-3-1-official
- Veo 3.1 Official docs: https://apidot.ai/docs/veo-3-1-official
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
