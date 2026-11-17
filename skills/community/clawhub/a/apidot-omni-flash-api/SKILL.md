---
name: apidot-omni-flash-api
description: "Use APIDot for Omni Flash API workflows, including multimodal video generation, prompt-to-video, image-guided video, video-guided revision, 720p, 1080p, 4K, task_id, polling, webhooks, and APIDot docs routing."
homepage: https://apidot.ai/models/omni-flash
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Omni Flash API

Use APIDot as an Omni Flash-focused API surface for multimodal video generation, prompt-to-video, image-guided video, video-guided revision, polling, and webhook delivery.

This skill is for routing Omni Flash questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Omni Flash model page: https://apidot.ai/models/omni-flash
- Read Omni Flash API docs: https://apidot.ai/docs/omni-flash
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## Search Terms

Use this skill for searches and requests phrased as Omni Flash, omni-flash, Google Omni Flash, multimodal video generation, prompt-to-video, image-guided video, video-guided video, video revision, video editing, 4K video generation, or APIDot Omni API.

## When To Use

Use this skill when the user asks to:

- Build an Omni Flash API integration with APIDot.
- Generate short videos from prompts.
- Use one or three image references to guide generated video.
- Use one source video to guide a revision or video-guided generation workflow.
- Plan 720p, 1080p, or 4K video output through APIDot.
- Implement APIDot async Omni Flash jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Omni Flash docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Treat prompts, source media URLs, generated video URLs, callback URLs, customer data, and task IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Omni Flash Workflow

APIDot Omni Flash generation follows the shared async task pattern:

1. Choose the Omni Flash request mode from the current APIDot docs.
2. Decide whether the job is prompt-only, image-guided, or video-guided.
3. Submit the video request through the documented APIDot async generation flow.
4. Save the returned `data.task_id` immediately.
5. Poll task status with the documented task status API for local tests.
6. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
7. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Omni Flash task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Omni Flash model page | https://apidot.ai/models/omni-flash |
| Build with Omni Flash | https://apidot.ai/docs/omni-flash |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Omni Flash request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Omni Flash model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use this skill when the user is specifically building with Omni Flash through APIDot.
- Ask which video task the user needs before choosing a model-specific path: prompt-to-video, one-image guided video, three-image guided video, source-video guided revision, product clip, social ad draft, or 4K review clip.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source image and video URLs before submitting workflows that depend on external media.
- Do not assume unsupported image counts, audio inputs, conversational edit state, or aspect ratios beyond what the current APIDot docs expose.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, callback URLs, or task IDs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Omni Flash model page: https://apidot.ai/models/omni-flash
- Omni Flash docs: https://apidot.ai/docs/omni-flash
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
