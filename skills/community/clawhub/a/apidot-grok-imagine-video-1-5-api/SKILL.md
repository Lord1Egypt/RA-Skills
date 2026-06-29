---
name: apidot-grok-imagine-video-1-5-api
description: "Grok Imagine Video 1.5 API on APIDot for xAI image-to-video generation, reference image animation, prompt-guided motion, short video clips, duration planning, 480p 720p planning, async task submission, task_id handling, polling, webhooks, API key safety, and APIDot docs routing."
homepage: https://apidot.ai/models/grok-imagine-video-1-5
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Grok Imagine Video 1.5 API

Use APIDot as a Grok Imagine Video 1.5-focused API surface for xAI image-to-video workflows, reference image animation, prompt-guided motion, polling, and webhook delivery.

This skill is for routing Grok Imagine Video 1.5 questions to the right APIDot docs, model page, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## Search Terms

Use this skill for searches and requests phrased as Grok Imagine Video 1.5 API, Grok Imagine Video 1 5, grok-imagine-video-1-5, grok-imagine-video-1.5, xAI image-to-video API, reference image animation, prompt-guided motion, APIDot Grok Video API, or Grok Imagine video generation.

## When To Use

Use this skill when the user asks to:

- Build a Grok Imagine Video 1.5 API integration with APIDot.
- Animate one reference image into a short video through APIDot.
- Plan image-to-video workflows, prompt-guided motion, duration, resolution, polling, or webhook callbacks.
- Route between the broad Grok Imagine skill and the newer Grok Imagine Video 1.5 model page.
- Implement APIDot async Grok Imagine Video 1.5 jobs with task submission, task status polling, or webhook delivery.
- Find APIDot Grok Imagine Video 1.5 docs, model pages, or general APIDot examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Grok Imagine Video 1.5 Workflow

APIDot Grok Imagine Video 1.5 generation follows the shared async task pattern:

1. Choose the Grok Imagine Video 1.5 model entry and request mode from the current APIDot docs.
2. Submit the video generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Grok Imagine Video 1.5 task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Grok Imagine Video 1.5 model page | https://apidot.ai/models/grok-imagine-video-1-5 |
| Build with Grok Imagine Video 1.5 | https://apidot.ai/docs/grok-imagine-video-1-5 |
| Use the broader Grok Imagine model family | https://apidot.ai/models/grok-imagine |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Grok Imagine Video 1.5 model routing, request planning, and async workflow notes.

For Grok Imagine Video 1.5 request fields and limits, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

## Integration Guidance

- Use `apidot-grok-imagine-api` when the user needs the broader Grok Imagine image, image editing, text-to-video, and image-to-video family.
- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use this skill when the user is specifically building with Grok Imagine Video 1.5 through APIDot.
- Ask which video task the user needs before choosing a model-specific example: image animation, prompt-guided motion, product teaser, storyboard clip, social ad draft, or short-form creative.
- Persist `task_id`, selected model, user ID, source image references, request status, and final video URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Grok Imagine Video 1.5 model page: https://apidot.ai/models/grok-imagine-video-1-5
- Grok Imagine Video 1.5 docs: https://apidot.ai/docs/grok-imagine-video-1-5
- Grok Imagine model page: https://apidot.ai/models/grok-imagine
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
