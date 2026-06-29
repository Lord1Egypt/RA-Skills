---
name: apidot-wan-2-2-fast-api
description: "Wan 2.2 Fast API on APIDot for Alibaba Wan 2.2 Fast, wan2.2 text-to-video fast, wan2.2 image-to-video fast, prompt-to-video drafts, one or two image animation, low-cost motion iteration, 480p 720p planning, task_id handling, polling, webhooks, API key safety, and APIDot docs routing."
homepage: https://apidot.ai/models/wan-2-2-fast
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Wan 2.2 Fast API

Use APIDot as a Wan 2.2 Fast-focused API surface for rapid short-video drafts, prompt-to-video, one-or-two-image animation, polling, and webhook delivery.

This skill is for routing Wan 2.2 Fast questions to the right APIDot docs, model page, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## Search Terms

Use this skill for searches and requests phrased as Wan 2.2 Fast API, Wan 2 2 Fast, wan-2-2-fast, wan2.2 fast, wan2.2-text-to-video-fast, wan2.2-image-to-video-fast, Alibaba Wan fast video, prompt-to-video draft, image-to-video draft, or APIDot Wan API.

## When To Use

Use this skill when the user asks to:

- Build a Wan 2.2 Fast API integration with APIDot.
- Generate rapid short-video drafts from prompts, one source image, or two source images.
- Use Wan 2.2 Fast through APIDot for text-to-video or image-to-video iteration.
- Plan lower-friction video drafts, resolution choices, polling, webhook callbacks, or task result handling.
- Implement APIDot async Wan 2.2 Fast jobs with task submission, task status polling, or webhook delivery.
- Find APIDot Wan 2.2 Fast docs, model pages, or general APIDot examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Wan 2.2 Fast Workflow

APIDot Wan 2.2 Fast generation follows the shared async task pattern:

1. Choose the Wan 2.2 Fast model entry and request mode from the current APIDot docs.
2. Submit the video generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Wan 2.2 Fast task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Wan 2.2 Fast model page | https://apidot.ai/models/wan-2-2-fast |
| Build with Wan 2.2 Fast | https://apidot.ai/docs/wan-2-2-fast |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Wan 2.2 Fast model routing, request planning, and async workflow notes.

For Wan 2.2 Fast request modes, prefer the live APIDot model page and docs page. Do not copy request fields from Wan 2.5, Wan 2.6, Wan 2.7 Video, or another video model family unless the APIDot docs show the same field.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use `apidot-wan-2-5-api`, `apidot-wan-2-6-api`, or `apidot-wan-2-7-video-api` when the user asks for those later Wan video model families.
- Use this skill when the user is specifically building with Wan 2.2 Fast through APIDot.
- Ask which video task the user needs before choosing a model-specific example: text-to-video draft, one-image animation, two-image transition, product teaser, storyboard draft, or social ad draft.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source image URLs before submitting workflows that depend on image guidance.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Wan 2.2 Fast model page: https://apidot.ai/models/wan-2-2-fast
- Wan 2.2 Fast docs: https://apidot.ai/docs/wan-2-2-fast
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
