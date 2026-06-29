---
name: apidot-seedream-5-0-lite-api
description: "Use APIDot for Seedream 5.0 Lite API workflows, including Seedream 5.0 Lite, image generation API, image editing API, multi-reference image generation, reference-guided editing, structured layout image workflows, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/seedream-5-0-lite
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Seedream 5.0 Lite API

Use APIDot as a Seedream 5.0 Lite-focused API surface for image generation, image editing, reference-guided workflows, structured layout image planning, polling, and webhook delivery.

This skill is for routing Seedream 5.0 Lite questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Seedream 5.0 Lite API integration with APIDot.
- Generate or edit images from prompts and reference images.
- Use Seedream 5.0 Lite through APIDot for image generation, image editing, or reference-guided workflows.
- Plan structured layout image tasks, output count, polling, or webhook callbacks.
- Implement APIDot async Seedream 5.0 Lite jobs with task submission, task status polling, or webhook delivery.
- Find APIDot Seedream 5.0 Lite docs, model pages, or general APIDot examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Seedream 5.0 Lite Workflow

APIDot Seedream 5.0 Lite generation follows the shared async task pattern:

1. Choose the Seedream 5.0 Lite request mode from the current APIDot docs.
2. Submit the image generation or editing request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final image URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Seedream 5.0 Lite task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Seedream 5.0 Lite model page | https://apidot.ai/models/seedream-5-0-lite |
| Build with Seedream 5.0 Lite | https://apidot.ai/docs/seedream-5-0-lite |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Seedream 5.0 Lite model routing, request planning, and async workflow notes.

For Seedream 5.0 Lite request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another image model family unless the APIDot docs show the same field.

## Integration Guidance

- Use `apidot-image-generation-api` when the user needs broad image generation guidance across several model families.
- Use `apidot-seedream-4-5-api` when the user asks specifically for Seedream 4.5.
- Use this skill when the user is specifically building with Seedream 5.0 Lite through APIDot.
- Ask which image task the user needs before choosing a model-specific example: prompt-based image generation, image editing, reference-guided edit, structured layout, product visual, or marketing creative.
- Persist `task_id`, selected model, user ID, source media references, request status, and final image URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private image URLs, generated image URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Seedream 5.0 Lite model page: https://apidot.ai/models/seedream-5-0-lite
- Seedream 5.0 Lite docs: https://apidot.ai/docs/seedream-5-0-lite
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
