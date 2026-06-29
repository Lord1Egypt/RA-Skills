---
name: apidot-3d-generation-api
description: "Use APIDot for 3D generation API workflows, including text-to-3D API, image-to-3D API, multi-image-to-3D, Meshy 6 API, Tripo H3.1 API, Tripo P1 API, task_id handling, polling, task status, and webhook integration based on APIDot docs."
homepage: https://apidot.ai/models/3d
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot 3D Generation API

Use APIDot as a 3D-focused API surface for text-to-3D, image-to-3D, multi-image-to-3D, polling, and webhook workflows.

This skill is for routing 3D generation questions to the right APIDot docs, examples, and async integration pattern. It is documentation-only: it includes no executable files, setup-time automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a 3D generation API integration with APIDot.
- Generate 3D assets from text prompts, single reference images, or multiple reference images.
- Use Meshy 6, Tripo H3.1, Tripo P1, or related 3D model APIs through APIDot.
- Choose between text-to-3D, image-to-3D, and multi-image-to-3D workflows.
- Implement APIDot async 3D jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot 3D docs, model pages, or runnable 3D examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, pricing, model availability, reliability claims, refund behavior, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## 3D Workflow

APIDot 3D generation usually follows an async task pattern:

1. Choose the 3D model and generation mode from the current APIDot docs.
2. Submit the 3D generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or asset pipelines that may outlive the current page.
6. Store final 3D asset URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or the matching APIDot GitHub example.

## Model Routing

Start from the user's 3D task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot 3D models | https://apidot.ai/models/3d |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with Meshy 6 3D | https://apidot.ai/docs/meshy-6-3d |
| Build with Tripo H3.1 3D | https://apidot.ai/docs/tripo-h31-3d |
| Build with Tripo P1 3D | https://apidot.ai/docs/tripo-p1-3d |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Meshy, Tripo, or other 3D model families, prefer the live APIDot model page and docs page for that exact model. Do not copy request fields from another model family unless the APIDot docs show the same field.

## Integration Guidance

- Use the broad `apidot-ai-api` skill when the user needs APIDot across image, video, chat, music, and 3D.
- Use this skill when the user is specifically building 3D generation, 3D asset polling, or 3D webhook workflows.
- Ask which 3D task the user needs before choosing a model-specific example: text-to-3D, image-to-3D, multi-image-to-3D, or generated asset pipeline.
- Persist `task_id`, selected model, user ID, source media references, request status, and final 3D asset URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible assets.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private source image URLs, generated asset URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- 3D models: https://apidot.ai/models/3d
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Meshy 6 3D docs: https://apidot.ai/docs/meshy-6-3d
- Tripo H3.1 3D docs: https://apidot.ai/docs/tripo-h31-3d
- Tripo P1 3D docs: https://apidot.ai/docs/tripo-p1-3d
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
