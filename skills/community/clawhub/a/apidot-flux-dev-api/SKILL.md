---
name: apidot-flux-dev-api
description: "Use APIDot for Flux Dev API workflows, including FLUX.1 Dev, Black Forest Labs image generation, text-to-image, single-reference image-to-image, prompt adherence, realistic detail, task_id, polling, webhooks, and APIDot docs routing."
homepage: https://apidot.ai/models/flux-dev
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Flux Dev API

Use APIDot as a Flux Dev-focused API surface for FLUX.1 Dev text-to-image generation, single-reference image-to-image workflows, prompt adherence, realistic detail, polling, and webhook delivery.

This skill is for routing Flux Dev questions to the right APIDot docs, model page, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Flux Dev model page: https://apidot.ai/models/flux-dev
- Read Flux Dev API docs: https://apidot.ai/docs/flux-dev
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## Search Terms

Use this skill for searches and requests phrased as Flux Dev, FLUX.1 Dev, flux-dev, Black Forest Labs Flux, open-weight image generation, text-to-image, image-to-image, product visuals, prompt adherence, realistic image generation, or APIDot Flux API.

## When To Use

Use this skill when the user asks to:

- Build a Flux Dev API integration with APIDot.
- Generate high-quality images from text prompts with FLUX.1 Dev.
- Use one reference image for image-to-image guidance when supported by the current APIDot docs.
- Plan output size, output count, file format, polling, webhook callbacks, or image result persistence.
- Choose between Flux Dev, Flux Schnell, FLUX.2, and Flux Kontext APIDot workflows.
- Find APIDot Flux Dev docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Treat prompts, source image URLs, generated image URLs, callback URLs, customer data, and task IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Flux Dev Workflow

APIDot Flux Dev generation follows the shared async task pattern:

1. Choose the Flux Dev request mode from the current APIDot docs.
2. Decide whether the job is prompt-only text-to-image or single-reference image-to-image.
3. Submit the image request through the documented APIDot async generation flow.
4. Save the returned `data.task_id` immediately.
5. Poll task status with the documented task status API for local tests.
6. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
7. Store final image URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Flux Dev task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Flux Dev model page | https://apidot.ai/models/flux-dev |
| Build with Flux Dev | https://apidot.ai/docs/flux-dev |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Flux Dev request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another image model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Flux Dev model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-image-generation-api` when the user needs broad image generation guidance across several model families.
- Use `apidot-flux-2-api` when the user specifically needs FLUX.2 workflows.
- Use `apidot-flux-kontext-api` when the user specifically needs context-aware Flux Kontext editing.
- Use this skill when the user is specifically building FLUX.1 Dev text-to-image or single-reference image-to-image workflows through APIDot.
- Ask which image task the user needs before choosing a model-specific path: prompt-only generation, single-reference image-to-image, product visual, campaign image, design exploration, or realistic detail draft.
- Persist `task_id`, selected model, user ID, source image references, request status, and final image URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging API keys, private prompts, private image URLs, generated image URLs, callback URLs, or task IDs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Flux Dev model page: https://apidot.ai/models/flux-dev
- Flux Dev docs: https://apidot.ai/docs/flux-dev
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
