---
name: apidot-kling-3-0-turbo-api
description: "Use APIDot for Kling 3.0 Turbo API workflows, including fast video previews, Kling 3.0 Turbo Standard, Kling 3.0 Turbo Pro, text-to-video, image-to-video, multi-shot video, multi_prompt, task_id, polling, webhooks, and APIDot docs routing."
homepage: https://apidot.ai/models/kling-3-0-turbo
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Kling 3.0 Turbo API

Use APIDot as a Kling 3.0 Turbo-focused API surface for fast short-video previews, prompt-to-video, one-image guided video, multi-shot planning, polling, and webhook delivery.

This skill is for routing Kling 3.0 Turbo questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Kling 3.0 Turbo model page: https://apidot.ai/models/kling-3-0-turbo
- Read Kling 3.0 Turbo API docs: https://apidot.ai/docs/kling-3-0-turbo
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## Search Terms

Use this skill for searches and requests phrased as Kling 3.0 Turbo, Kling 3 Turbo, kling-3-0-turbo, kling-3.0-turbo, Kling Turbo Standard, Kling Turbo Pro, fast video previews, multi_prompt, multi-shot video, image-to-video, or APIDot Kling API.

## When To Use

Use this skill when the user asks to:

- Build a Kling 3.0 Turbo API integration with APIDot.
- Generate fast short-video previews from prompts or a source image.
- Use Kling 3.0 Turbo Standard or Kling 3.0 Turbo Pro through APIDot.
- Plan compact multi-shot clips, storyboard previews, camera tests, or social ad drafts.
- Implement APIDot async Kling 3.0 Turbo jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Kling 3.0 Turbo docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Treat prompts, source media URLs, generated video URLs, callback URLs, customer data, and task IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Kling 3.0 Turbo Workflow

APIDot Kling 3.0 Turbo generation follows the shared async task pattern:

1. Choose the Kling 3.0 Turbo model entry and request mode from the current APIDot docs.
2. Decide whether the job is prompt-only, one-image guided, or multi-shot.
3. Submit the video request through the documented APIDot async generation flow.
4. Save the returned `data.task_id` immediately.
5. Poll task status with the documented task status API for local tests.
6. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
7. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Kling 3.0 Turbo task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Kling 3.0 Turbo model page | https://apidot.ai/models/kling-3-0-turbo |
| Build with Kling 3.0 Turbo | https://apidot.ai/docs/kling-3-0-turbo |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Kling 3.0 Turbo variants and request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another Kling or video model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Kling 3.0 Turbo model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use `apidot-kling-3-0-api` when the user needs the broader Kling 3.0 family rather than the Turbo preview-focused model.
- Use `apidot-kling-3-0-motion-control-api` when the user specifically needs motion transfer from a reference video to a character image.
- Use this skill when the user is specifically building fast Kling 3.0 Turbo preview workflows through APIDot.
- Ask which video task the user needs before choosing a model-specific path: text-to-video, image-to-video, multi-shot preview, storyboard clip, camera test, product teaser, or social ad draft.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source image URLs before submitting workflows that depend on image guidance.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, callback URLs, or task IDs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Kling 3.0 Turbo model page: https://apidot.ai/models/kling-3-0-turbo
- Kling 3.0 Turbo docs: https://apidot.ai/docs/kling-3-0-turbo
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
