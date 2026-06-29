---
name: apidot-wan-2-7-image-api
description: "Wan 2.7 Image API on APIDot for wan 2 7 image, wan2.7 image, wan27 image, Wan 2.7 Image Pro, text-to-image, image editing, image-to-image, multi-reference generation, readable visual text, task_id, polling, webhooks, and APIDot docs routing."
homepage: https://apidot.ai/models/wan-2-7-image
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Wan 2.7 Image API

Use APIDot as a Wan 2.7 Image-focused API surface for text-to-image generation, image editing, image-to-image workflows, multi-reference generation, prompt adherence, readable visual text, polling, and webhook delivery.

This skill is for routing Wan 2.7 Image questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## Search Terms

Use this skill for searches and requests phrased as Wan 2.7 Image API, Wan 2 7 Image, wan2.7 image, wan27 image, wan-2-7-image, Wan 2.7 Image Pro, Wan image generation, Wan image editing, multi-reference image generation, or APIDot Wan API.

## When To Use

Use this skill when the user asks to:

- Build a Wan 2.7 Image API integration with APIDot.
- Generate images from prompts, product briefs, campaign concepts, or design directions.
- Edit or transform source images with image-to-image or multi-reference workflows.
- Use Wan 2.7 Image or Wan 2.7 Image Pro through APIDot.
- Implement APIDot async image jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Wan 2.7 Image docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Wan 2.7 Image Workflow

APIDot Wan 2.7 Image generation usually follows an async task pattern:

1. Choose the Wan 2.7 Image model entry and request mode from the current APIDot docs.
2. Submit the generation or edit request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final image URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Wan 2.7 Image task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Wan 2.7 Image model page | https://apidot.ai/models/wan-2-7-image |
| Build with Wan 2.7 Image | https://apidot.ai/docs/wan-2-7-image |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Wan 2.7 Image request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another image model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Wan 2.7 Image model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-image-generation-api` when the user needs broad image generation guidance across several model families.
- Use `apidot-wan-2-7-video-api` when the user is specifically building Wan 2.7 video workflows.
- Use this skill when the user is specifically building with Wan 2.7 Image through APIDot.
- Ask which image task the user needs before choosing a model-specific example: text-to-image, image editing, image-to-image, multi-reference generation, product visual, ad creative, or readable visual text.
- Persist `task_id`, selected model, user ID, source media references, request status, and final image URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private image URLs, generated image URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Wan 2.7 Image model page: https://apidot.ai/models/wan-2-7-image
- Wan 2.7 Image docs: https://apidot.ai/docs/wan-2-7-image
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
