---
name: apidot-hunyuan-3d-3-1-api
description: "Use APIDot for Hunyuan 3D 3.1 API workflows, including Hunyuan 3D Pro and Rapid variants, text-to-3D API, image-to-3D API, multi-view guidance, PBR output planning, geometry controls, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/hunyuan-3d-3-1
metadata:
  openclaw:
    homepage: https://apidot.ai/docs/hunyuan-3d-3-1
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Hunyuan 3D 3.1 API

Use APIDot as a Hunyuan 3D 3.1-focused API surface for text-to-3D, image-to-3D, multi-view guidance, PBR planning, geometry controls, polling, and webhook workflows.

This skill routes Hunyuan 3D 3.1 questions to current APIDot model pages, docs, reference notes, and the shared async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, shell automation, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Hunyuan 3D 3.1 model page: https://apidot.ai/models/hunyuan-3d-3-1
- Read Hunyuan 3D 3.1 API docs: https://apidot.ai/docs/hunyuan-3d-3-1
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## When To Use

Use this skill when the user asks to:

- Build a Hunyuan 3D 3.1 API integration with APIDot.
- Generate 3D assets from text prompts or a primary reference image.
- Choose between current Pro and Rapid text-to-3D or image-to-3D variants.
- Plan multi-view image guidance, PBR output, geometry mode, or face-count controls when supported.
- Implement APIDot async 3D jobs with task submission, task status polling, or webhook delivery.
- Find current APIDot Hunyuan 3D 3.1 docs, model pages, or general examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent request fields, commercial terms, model availability, reliability claims, or competitor comparisons.
- Use current APIDot docs and model pages for model variants, supported controls, limits, and current product details.

## Hunyuan 3D 3.1 Workflow

APIDot Hunyuan 3D 3.1 generation follows the shared async task pattern:

1. Choose the current Pro or Rapid text-to-3D or image-to-3D model entry from the APIDot docs.
2. Plan prompt, primary image, optional multi-view guidance, materials, and geometry controls only where supported.
3. Submit the 3D generation request through the documented APIDot async generation flow.
4. Save the returned `data.task_id` immediately.
5. Poll task status for local tests or use `callback_url` webhook delivery for production asset pipelines.
6. Store final asset URLs only after the task reaches a terminal success state.

Do not copy fields across Pro, Rapid, text, or image variants unless the current APIDot docs explicitly support them.

## Model Routing

| User Goal | Start Here |
| --- | --- |
| Browse Hunyuan 3D 3.1 | https://apidot.ai/models/hunyuan-3d-3-1 |
| Build with Hunyuan 3D 3.1 | https://apidot.ai/docs/hunyuan-3d-3-1 |
| Browse APIDot 3D models | https://apidot.ai/models/3d |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn the APIDot quickstart | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for local, non-executable variant selection, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-3d-generation-api` for broad 3D guidance across model families.
- Use this skill when the request specifically targets Hunyuan 3D 3.1 through APIDot.
- Confirm text or image input, Pro or Rapid, asset requirements, and supported controls before planning a request.
- Persist `task_id`, selected model, user ID, source media references, request status, and final asset URLs together.
- Validate source image URLs before image-to-3D submission.
- Treat webhook handlers as idempotent so duplicate deliveries do not create duplicate visible assets.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private image URLs, callback URLs, or generated asset URLs.

## Official Links

- Website: https://apidot.ai
- Hunyuan 3D 3.1 model page: https://apidot.ai/models/hunyuan-3d-3-1
- Hunyuan 3D 3.1 docs: https://apidot.ai/docs/hunyuan-3d-3-1
- APIDot 3D models: https://apidot.ai/models/3d
- APIDot docs: https://apidot.ai/docs
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Account dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
