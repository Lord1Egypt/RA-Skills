---
name: apidot-kling-avatar-2-0-api
description: "Use APIDot for Kling Avatar 2.0 API workflows, including talking avatar video, image-and-audio-to-video, Standard and Pro variants, avatar performance direction, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/kling-avatar-2-0
metadata:
  openclaw:
    homepage: https://apidot.ai/docs/kling-avatar-2-0
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Kling Avatar 2.0 API

Use APIDot as a Kling Avatar 2.0-focused API surface for expressive talking-avatar video from one reference image and one speech audio track.

This skill routes Kling Avatar 2.0 questions to current APIDot model pages, docs, reference notes, and the shared async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, shell automation, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Kling Avatar 2.0 model page: https://apidot.ai/models/kling-avatar-2-0
- Read Kling Avatar 2.0 API docs: https://apidot.ai/docs/kling-avatar-2-0
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## When To Use

Use this skill when the user asks to:

- Build a Kling Avatar 2.0 API integration with APIDot.
- Generate a talking-avatar video from one reference image and one speech audio track.
- Choose between the current Standard and Pro model variants.
- Plan emotion, gesture, camera feel, or speaking-style direction for an avatar performance.
- Implement APIDot async avatar jobs with task submission, task status polling, or webhook delivery.
- Find current APIDot Kling Avatar 2.0 docs, model pages, or general examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent request fields, commercial terms, model availability, reliability claims, or competitor comparisons.
- Use current APIDot docs and model pages for supported media, limits, model variants, and current product details.

## Kling Avatar 2.0 Workflow

APIDot Kling Avatar 2.0 generation follows the shared async task pattern:

1. Choose the current Standard or Pro model entry from the APIDot docs.
2. Prepare one supported reference image and one supported speech audio source.
3. Submit the avatar request through the documented APIDot async generation flow.
4. Save the returned `data.task_id` immediately.
5. Poll task status for local tests or use `callback_url` webhook delivery for production.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields or media limits. Open the current APIDot docs when exact request details are needed.

## Model Routing

| User Goal | Start Here |
| --- | --- |
| Browse Kling Avatar 2.0 | https://apidot.ai/models/kling-avatar-2-0 |
| Build with Kling Avatar 2.0 | https://apidot.ai/docs/kling-avatar-2-0 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn the APIDot quickstart | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for local, non-executable model-routing, media-planning, and async workflow notes.

## Integration Guidance

- Use `apidot-video-generation-api` for broad video guidance across model families.
- Use this skill when the request specifically targets Kling Avatar 2.0 through APIDot.
- Confirm the reference image, speech audio, model variant, and performance direction before planning a request.
- Use a separate workflow for text-to-speech, multiple characters, multiple audio tracks, or longer-form avatar programs.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate image and audio URLs before submission.
- Treat webhook handlers as idempotent and retry transient failures with backoff.
- Avoid logging API keys, private media URLs, private prompts, callback URLs, or generated video URLs.

## Official Links

- Website: https://apidot.ai
- Kling Avatar 2.0 model page: https://apidot.ai/models/kling-avatar-2-0
- Kling Avatar 2.0 docs: https://apidot.ai/docs/kling-avatar-2-0
- APIDot docs: https://apidot.ai/docs
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Account dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
