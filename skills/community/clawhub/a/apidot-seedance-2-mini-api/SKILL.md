---
name: apidot-seedance-2-mini-api
description: "Use APIDot for Seedance 2.0 Mini API workflows, including low-cost short video generation, text-to-video, first and last frame image-to-video, reference image/video/audio workflows, 480p, 720p, task_id, polling, webhooks, and APIDot docs routing."
homepage: https://apidot.ai/models/seedance-2-mini
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Seedance 2.0 Mini API

Use APIDot as a Seedance 2.0 Mini-focused API surface for lower-cost short video generation, prompt testing, first/last-frame clips, multimodal reference workflows, polling, and webhook delivery.

This skill is for routing Seedance 2.0 Mini questions to the right APIDot docs, model pages, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Seedance 2.0 Mini model page: https://apidot.ai/models/seedance-2-mini
- Read Seedance 2.0 Mini API docs: https://apidot.ai/docs/seedance-2-mini
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## Search Terms

Use this skill for searches and requests phrased as Seedance 2 Mini, Seedance 2.0 Mini, seedance-2-mini, low-cost video generation, text-to-video, first frame video, last frame video, reference-to-video, reference audio video, short video drafts, or APIDot Seedance API.

## When To Use

Use this skill when the user asks to:

- Build a Seedance 2.0 Mini API integration with APIDot.
- Generate lower-cost short video drafts from prompts.
- Use first and last frame images to guide a transition.
- Use image, video, or audio references for reference-guided short clips.
- Choose between Seedance 2.0 Mini and heavier Seedance 2 workflows.
- Implement APIDot async video jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Seedance 2.0 Mini docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Treat prompts, source media URLs, reference media URLs, generated video URLs, callback URLs, customer data, and task IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Seedance 2.0 Mini Workflow

APIDot Seedance 2.0 Mini generation follows the shared async task pattern:

1. Choose the Seedance 2.0 Mini request mode from the current APIDot docs.
2. Decide whether the job is prompt-only, first/last-frame guided, or reference-guided.
3. Submit the video request through the documented APIDot async generation flow.
4. Save the returned `data.task_id` immediately.
5. Poll task status with the documented task status API for local tests.
6. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
7. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Seedance 2.0 Mini task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Seedance 2.0 Mini model page | https://apidot.ai/models/seedance-2-mini |
| Build with Seedance 2.0 Mini | https://apidot.ai/docs/seedance-2-mini |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Seedance 2.0 Mini request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Seedance 2.0 Mini model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use `apidot-seedance-2-api` when the user specifically needs the heavier Seedance 2 workflow or the controlled script pilot.
- Use this skill when the user is specifically building lower-cost, high-frequency Seedance 2.0 Mini video drafts through APIDot.
- Ask which video task the user needs before choosing a model-specific path: text-to-video, first/last-frame guided video, reference-image video, reference-video motion, reference-audio guidance, storyboard draft, or social preview.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source image, video, and audio URLs before submitting workflows that depend on external media.
- Keep frame mode and reference mode separate when the live docs describe them as separate request modes.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, callback URLs, or task IDs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Seedance 2.0 Mini model page: https://apidot.ai/models/seedance-2-mini
- Seedance 2.0 Mini docs: https://apidot.ai/docs/seedance-2-mini
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
