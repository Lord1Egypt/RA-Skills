---
name: apidot-grok-imagine-image-quality-api
description: "Use APIDot for Grok Imagine Image Quality API workflows, including high-fidelity image generation, image editing, reference-guided images, 1K, 2K, output formats, task_id, polling, webhooks, and APIDot docs routing."
homepage: https://apidot.ai/models/grok-imagine-image-quality
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Grok Imagine Image Quality API

Use APIDot as a Grok Imagine Image Quality-focused API surface for high-fidelity text-to-image generation, reference-guided image editing, 1K or 2K output planning, polling, and webhook delivery.

This skill is for routing Grok Imagine Image Quality questions to the right APIDot docs, model page, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Grok Imagine Image Quality model page: https://apidot.ai/models/grok-imagine-image-quality
- Read Grok Imagine Image Quality API docs: https://apidot.ai/docs/grok-imagine-image-quality
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## Search Terms

Use this skill for searches and requests phrased as Grok Imagine Image Quality, grok-imagine-image-quality, xAI image API, high-fidelity image generation, 2K image generation, image editing, reference-guided image, product images, readable text images, or APIDot Grok Imagine API.

## When To Use

Use this skill when the user asks to:

- Build a Grok Imagine Image Quality API integration with APIDot.
- Generate polished 1K or 2K images with stronger detail, lighting, text clarity, or finished visual quality.
- Edit or guide images with reference image URLs when supported by the current APIDot docs.
- Plan output format, aspect ratio, multiple outputs, polling, webhook callbacks, or cost-sensitive image workflows.
- Choose between Grok Imagine Image Quality and broader Grok Imagine image/video workflows.
- Find APIDot Grok Imagine Image Quality docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Treat prompts, source image URLs, generated image URLs, callback URLs, customer data, and task IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Grok Imagine Image Quality Workflow

APIDot Grok Imagine Image Quality generation follows the shared async task pattern:

1. Choose the Grok Imagine Image Quality request mode from the current APIDot docs.
2. Decide whether the job is prompt-only image generation or reference-guided editing.
3. Submit the image request through the documented APIDot async generation flow.
4. Save the returned `data.task_id` immediately.
5. Poll task status with the documented task status API for local tests.
6. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
7. Store final image URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Grok Imagine Image Quality task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Grok Imagine Image Quality model page | https://apidot.ai/models/grok-imagine-image-quality |
| Build with Grok Imagine Image Quality | https://apidot.ai/docs/grok-imagine-image-quality |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Grok Imagine Image Quality request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another image model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Grok Imagine Image Quality model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-image-generation-api` when the user needs broad image generation guidance across several model families.
- Use `apidot-grok-imagine-api` when the user needs broader Grok Imagine image and video routing.
- Use `apidot-grok-imagine-video-1-5-api` when the user specifically needs Grok Imagine video.
- Use this skill when the user is specifically building high-fidelity Grok Imagine still image workflows through APIDot.
- Ask which image task the user needs before choosing a model-specific path: prompt-only image generation, reference-guided edit, product image, ad creative, poster, UI-style graphic, or high-quality review option.
- Persist `task_id`, selected model, user ID, source image references, request status, and final image URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging API keys, private prompts, private image URLs, generated image URLs, callback URLs, or task IDs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Grok Imagine Image Quality model page: https://apidot.ai/models/grok-imagine-image-quality
- Grok Imagine Image Quality docs: https://apidot.ai/docs/grok-imagine-image-quality
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
