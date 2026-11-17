---
name: apidot-flux-schnell-api
description: "Use APIDot for Flux Schnell API workflows, including FLUX.1 Schnell, Black Forest Labs image generation, fast low-cost text-to-image drafts, prompt exploration, batch creative iteration, task_id, polling, webhooks, and APIDot docs routing."
homepage: https://apidot.ai/models/flux-schnell
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Flux Schnell API

Use APIDot as a Flux Schnell-focused API surface for FLUX.1 Schnell text-to-image generation, fast low-cost drafts, prompt exploration, batch creative iteration, polling, and webhook delivery.

This skill is for routing Flux Schnell questions to the right APIDot docs, model page, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Flux Schnell model page: https://apidot.ai/models/flux-schnell
- Read Flux Schnell API docs: https://apidot.ai/docs/flux-schnell
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## Search Terms

Use this skill for searches and requests phrased as Flux Schnell, FLUX.1 Schnell, flux-schnell, Black Forest Labs Flux, fast image generation, low-cost text-to-image, prompt exploration, batch creative iteration, draft image generation, or APIDot Flux API.

## When To Use

Use this skill when the user asks to:

- Build a Flux Schnell API integration with APIDot.
- Generate fast, low-cost image drafts from text prompts.
- Explore prompt variations before moving to higher-fidelity image models.
- Plan output size, output format, polling, webhook callbacks, or image result persistence.
- Choose between Flux Schnell, Flux Dev, FLUX.2, and Flux Kontext APIDot workflows.
- Find APIDot Flux Schnell docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Treat prompts, generated image URLs, callback URLs, customer data, and task IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Flux Schnell Workflow

APIDot Flux Schnell generation follows the shared async task pattern:

1. Choose the Flux Schnell request mode from the current APIDot docs.
2. Use Flux Schnell for fast prompt-only draft generation and prompt exploration.
3. Submit the image request through the documented APIDot async generation flow.
4. Save the returned `data.task_id` immediately.
5. Poll task status with the documented task status API for local tests.
6. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
7. Store final image URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Flux Schnell task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Flux Schnell model page | https://apidot.ai/models/flux-schnell |
| Build with Flux Schnell | https://apidot.ai/docs/flux-schnell |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Flux Schnell request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another image model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Flux Schnell model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-image-generation-api` when the user needs broad image generation guidance across several model families.
- Use `apidot-flux-dev-api` when the user specifically needs FLUX.1 Dev quality or single-reference workflows.
- Use `apidot-flux-2-api` when the user specifically needs newer FLUX.2 workflows.
- Use this skill when the user is specifically building fast Flux Schnell draft-generation workflows through APIDot.
- Ask whether the workflow needs quick drafts, prompt exploration, batch creative options, product visual ideation, or a later upgrade path to a higher-fidelity Flux model.
- Persist `task_id`, selected model, user ID, prompt metadata, request status, and final image URLs together.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging API keys, private prompts, generated image URLs, callback URLs, or task IDs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Flux Schnell model page: https://apidot.ai/models/flux-schnell
- Flux Schnell docs: https://apidot.ai/docs/flux-schnell
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
