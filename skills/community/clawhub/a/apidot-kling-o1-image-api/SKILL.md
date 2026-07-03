---
name: apidot-kling-o1-image-api
description: "Use APIDot for Kling O1 Image API workflows, including cost-effective image editing, reference-guided image changes, text-to-image planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/kling-o1-image
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Kling O1 Image API

Use APIDot as a Kling O1 Image-focused API surface for image editing, reference-guided changes, prompt planning, polling, and webhook delivery.

This skill is for routing Kling O1 Image questions to the right APIDot docs, model pages, reference notes, and async integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Kling O1 Image API integration with APIDot.
- Edit images or create prompt-guided image variations through APIDot.
- Use a lower-cost Kling image workflow before moving to heavier image models.
- Plan reference image handling, output selection, task tracking, or callback delivery.
- Implement APIDot async image jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Kling O1 Image docs, model pages, or integration notes.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Kling O1 Image Workflow

APIDot Kling O1 Image jobs follow the shared async image generation pattern:

1. Choose the Kling O1 Image request mode from the current APIDot docs.
2. Submit the generation or edit request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final image URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Kling O1 Image task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Kling O1 Image model page | https://apidot.ai/models/kling-o1-image |
| Build with Kling O1 Image | https://apidot.ai/docs/kling-o1-image |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Kling O1 Image model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-image-generation-api` when the user needs broad image generation guidance across several model families.
- Use `apidot-kling-o3-image-api` when the user specifically needs Kling O3 Image workflows.
- Use this skill when the user is specifically building with Kling O1 Image through APIDot.
- Ask whether the user needs image editing, prompt-only generation, image variation, product visual cleanup, or reference-guided output before choosing a request mode.
- Persist `task_id`, selected model, user ID, source media references, request status, and final image URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private image URLs, generated image URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Kling O1 Image model page: https://apidot.ai/models/kling-o1-image
- Kling O1 Image docs: https://apidot.ai/docs/kling-o1-image
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
