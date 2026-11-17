---
name: apidot-happy-horse-1-1-api
description: "Use APIDot for Happy Horse 1.1 API workflows, including Alibaba Happy Horse 1.1, audio-synced short video, text-to-video API, image-to-video API, reference-to-video API, 720p or 1080p planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/happy-horse-1-1
metadata:
  openclaw:
    homepage: https://apidot.ai/docs/happy-horse-1-1
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Happy Horse 1.1 API

Use APIDot as a Happy Horse 1.1-focused API surface for audio-synced short video, text-to-video, image-to-video, reference-to-video, polling, and webhook workflows.

This skill routes Happy Horse 1.1 questions to current APIDot model pages, docs, reference notes, and the shared async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, shell automation, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Happy Horse 1.1 model page: https://apidot.ai/models/happy-horse-1-1
- Read Happy Horse 1.1 API docs: https://apidot.ai/docs/happy-horse-1-1
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## When To Use

Use this skill when the user asks to:

- Build a Happy Horse 1.1 API integration with APIDot.
- Generate short videos from prompts, one source image, or reference images.
- Plan audio-synced video, 720p or 1080p output, duration, polling, or webhook delivery.
- Use Alibaba Happy Horse 1.1, text-to-video, image-to-video, or reference-to-video through APIDot.
- Implement APIDot async Happy Horse 1.1 jobs with task submission, task status polling, or callbacks.
- Find current APIDot Happy Horse 1.1 docs, model pages, or general examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent request fields, commercial terms, model availability, reliability claims, or competitor comparisons.
- Use current APIDot docs and model pages for supported inputs, limits, and current product details.

## Happy Horse 1.1 Workflow

APIDot Happy Horse 1.1 generation follows the shared async task pattern:

1. Choose text-to-video, image-to-video, or reference-to-video from the current APIDot docs.
2. Submit the generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable requests, point them to the current APIDot docs or general APIDot examples.

## Model Routing

| User Goal | Start Here |
| --- | --- |
| Browse Happy Horse 1.1 | https://apidot.ai/models/happy-horse-1-1 |
| Build with Happy Horse 1.1 | https://apidot.ai/docs/happy-horse-1-1 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn the APIDot quickstart | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for local, non-executable request-planning and async workflow notes.

## Integration Guidance

- Use `apidot-video-generation-api` for broad video guidance across model families.
- Use this skill when the request specifically targets Happy Horse 1.1 through APIDot.
- Confirm whether the user needs prompt-only, one-image, or reference-image guidance before planning inputs.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source media URLs before submitting workflows that depend on images.
- Treat webhook handlers as idempotent so duplicate deliveries do not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, callback URLs, or generated video URLs.

## Official Links

- Website: https://apidot.ai
- Happy Horse 1.1 model page: https://apidot.ai/models/happy-horse-1-1
- Happy Horse 1.1 docs: https://apidot.ai/docs/happy-horse-1-1
- APIDot docs: https://apidot.ai/docs
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Account dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
