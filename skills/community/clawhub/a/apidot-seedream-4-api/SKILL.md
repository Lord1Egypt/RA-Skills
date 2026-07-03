---
name: apidot-seedream-4-api
description: "Use APIDot for Seedream 4 API workflows, including 4K image generation, image editing, image-to-image planning, reference image generation, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/seedream-4
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Seedream 4 API

Use APIDot as a Seedream 4-focused API surface for image generation, image editing, image-to-image workflows, polling, and webhook delivery.

This skill is for routing Seedream 4 questions to the right APIDot docs, model pages, reference notes, and async integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Seedream 4 API integration with APIDot.
- Generate images, edit images, or plan image-to-image workflows through APIDot.
- Use Seedream 4 for 4K image generation, product visuals, marketing creative, or reference-guided image output.
- Implement APIDot async image jobs with task submission, task status polling, or webhook callbacks.
- Compare routing between Seedream 4 and newer Seedream model skills.
- Find APIDot Seedream 4 docs, model pages, or integration notes.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Seedream 4 Workflow

APIDot Seedream 4 jobs follow the shared async image generation pattern:

1. Choose the Seedream 4 request mode from the current APIDot docs.
2. Submit the generation or edit request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final image URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Seedream task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Seedream 4 model page | https://apidot.ai/models/seedream-4 |
| Build with Seedream 4 | https://apidot.ai/docs/seedream-4 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Seedream 4 model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-image-generation-api` when the user needs broad image generation guidance across several model families.
- Use `apidot-seedream-4-5-api` or `apidot-seedream-5-0-lite-api` when the user specifically names those newer Seedream variants.
- Use this skill when the user is specifically building with Seedream 4 through APIDot.
- Ask which image task the user needs before choosing a request mode: prompt-based image generation, image editing, image-to-image, product visual, marketing creative, or reference-guided generation.
- Persist `task_id`, selected model, user ID, source media references, request status, and final image URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private image URLs, generated image URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Seedream 4 model page: https://apidot.ai/models/seedream-4
- Seedream 4 docs: https://apidot.ai/docs/seedream-4
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
