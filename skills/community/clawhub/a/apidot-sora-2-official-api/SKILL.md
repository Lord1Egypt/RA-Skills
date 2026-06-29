---
name: apidot-sora-2-official-api
description: "Use APIDot for Sora 2 Official API workflows, including OpenAI Sora API, sora-2-official, sora-2-pro-official, text-to-video API, image-to-video API, prompt-to-video generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs."
homepage: https://apidot.ai/models/sora-2-official
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Sora 2 Official API

Use APIDot as a Sora 2 Official-focused API surface for prompt-to-video, image-guided video, polling, and webhook workflows.

This skill is for routing Sora 2 Official questions to the right APIDot docs, examples, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Sora 2 Official API integration with APIDot.
- Generate videos from prompts or one guiding image through APIDot.
- Use OpenAI Sora API, Sora 2 Official, sora-2-official, or sora-2-pro-official through APIDot.
- Choose between Sora 2 Standard and Pro request modes.
- Implement APIDot async Sora jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Sora 2 Official docs, model pages, or runnable examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Sora 2 Official Workflow

APIDot Sora 2 Official generation usually follows an async task pattern:

1. Choose the Sora 2 Official model entry and request mode from the current APIDot docs.
2. Submit the video generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or the matching APIDot GitHub example.

## Model Routing

Start from the user's Sora task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Sora 2 Official model page | https://apidot.ai/models/sora-2-official |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with Sora 2 Official | https://apidot.ai/docs/sora-2-official |
| Use runnable Sora 2 Official examples | https://github.com/APIDotAI/sora-2-official-api |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Sora 2 Official variants and request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Sora 2 Official model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use this skill when the user is specifically building with Sora 2 Official through APIDot.
- Ask which Sora task the user needs before choosing a model-specific example: prompt-to-video, image-guided video, Standard, or Pro.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source image URLs before submitting workflows that depend on image guidance.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private image URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Sora 2 Official model page: https://apidot.ai/models/sora-2-official
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Sora 2 Official docs: https://apidot.ai/docs/sora-2-official
- Sora 2 Official examples: https://github.com/APIDotAI/sora-2-official-api
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
