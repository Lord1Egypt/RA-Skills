---
name: apidot-meshy-6-3d-api
description: "Use APIDot for Meshy 6 3D API workflows, including Meshy 6 API, text-to-3D API, image-to-3D API, multi-image-to-3D API, 3D asset generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs."
homepage: https://apidot.ai/models/meshy-6-3d
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Meshy 6 3D API

Use APIDot as a Meshy 6-focused API surface for text-to-3D, image-to-3D, multi-image-to-3D, 3D asset polling, and webhook workflows.

This skill is for routing Meshy 6 3D questions to the right APIDot docs, examples, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Meshy 6 3D API integration with APIDot.
- Generate 3D assets from text prompts, one reference image, or multiple reference images.
- Use Meshy 6, text-to-3D, image-to-3D, or multi-image-to-3D through APIDot.
- Choose between Meshy 6 request modes.
- Implement APIDot async 3D jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Meshy 6 3D docs, model pages, or runnable examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Meshy 6 Workflow

APIDot Meshy 6 3D generation usually follows an async task pattern:

1. Choose the Meshy 6 request mode from the current APIDot docs.
2. Submit the 3D generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production asset pipelines or user workflows that may outlive the current page.
6. Store final 3D asset URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or the matching APIDot examples repository.

## Model Routing

Start from the user's Meshy 6 task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Meshy 6 model page | https://apidot.ai/models/meshy-6-3d |
| Browse APIDot 3D models | https://apidot.ai/models/3d |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with Meshy 6 3D | https://apidot.ai/docs/meshy-6-3d |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Meshy 6 request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another 3D model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Meshy 6 model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-3d-generation-api` when the user needs broad 3D generation guidance across several model families.
- Use this skill when the user is specifically building with Meshy 6 through APIDot.
- Ask which 3D task the user needs before choosing a model-specific example: text-to-3D, image-to-3D, multi-image-to-3D, or generated asset pipeline.
- Persist `task_id`, selected model, user ID, source media references, request status, and final 3D asset URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible assets.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private source image URLs, generated asset URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Meshy 6 model page: https://apidot.ai/models/meshy-6-3d
- 3D models: https://apidot.ai/models/3d
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Meshy 6 3D docs: https://apidot.ai/docs/meshy-6-3d
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
