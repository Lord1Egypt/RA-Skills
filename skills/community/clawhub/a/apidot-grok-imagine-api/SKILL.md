---
name: apidot-grok-imagine-api
description: "Use APIDot for Grok Imagine API workflows, including xAI Grok Imagine image generation, image editing, text-to-video, image-to-video, Grok Imagine Video 1.5, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/grok-imagine
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Grok Imagine API

Use APIDot as a Grok Imagine-focused API surface for xAI image generation, image editing, text-to-video, image-to-video, polling, and webhook delivery.

This skill is for routing Grok Imagine questions to the right APIDot docs, model pages, reference notes, and async integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Grok Imagine API integration with APIDot.
- Generate images or videos with Grok Imagine through APIDot.
- Use prompt-only generation or single-reference image guidance when supported by the current APIDot docs.
- Route between Grok Imagine image workflows and Grok Imagine video workflows.
- Implement APIDot async media jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Grok Imagine docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Grok Imagine Workflow

APIDot Grok Imagine generation follows the shared async task pattern:

1. Choose the Grok Imagine request mode from the current APIDot docs.
2. Submit the generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final image or video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Grok Imagine task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Grok Imagine model page | https://apidot.ai/models/grok-imagine |
| Build with Grok Imagine | https://apidot.ai/docs/grok-imagine |
| Build with Grok Imagine Video 1.5 | https://apidot.ai/docs/grok-imagine-video-1-5 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Grok Imagine request modes, prefer the live APIDot model page and docs pages. Do not copy request fields from another image or video model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Grok Imagine model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-image-generation-api` when the user needs broad image generation guidance across several model families.
- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use this skill when the user is specifically building with Grok Imagine through APIDot.
- Ask which media task the user needs before choosing a model-specific example: image generation, image editing, text-to-video, image-to-video, product concept, campaign creative, or social clip.
- Persist `task_id`, selected model, user ID, source media references, request status, and final media URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated media URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Grok Imagine model page: https://apidot.ai/models/grok-imagine
- Grok Imagine docs: https://apidot.ai/docs/grok-imagine
- Grok Imagine Video 1.5 docs: https://apidot.ai/docs/grok-imagine-video-1-5
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
