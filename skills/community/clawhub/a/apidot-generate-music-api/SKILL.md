---
name: apidot-generate-music-api
description: "Use APIDot for Generate Music API workflows, including prompt-to-song generation, instrumental generation, vocal music planning, async task submission, task_id handling, music detail polling, callback_url planning, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/generate-music
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Generate Music API

Use APIDot as a Generate Music-focused API surface for prompt-to-song generation, instrumental music, vocal music, polling, callback_url planning, and webhook delivery.

This skill is for routing Generate Music questions to the right APIDot docs, model pages, reference notes, and async music integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no scripts, executable files, install-time automation, review automation helpers, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Generate Music model page: https://apidot.ai/models/generate-music
- Read Generate Music API docs: https://apidot.ai/docs/generate-music
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Browse APIDot music models: https://apidot.ai/models/music

## When To Use

Use this skill when the user asks to:

- Build a Generate Music API integration with APIDot.
- Generate songs, instrumentals, vocal tracks, background music, or prompt-driven audio through APIDot.
- Plan music task submission, task status polling, music detail lookup, callback_url handling, webhook delivery, or final audio URL handling.
- Choose Generate Music instead of the broader APIDot music category or MiniMax Music 2.6 model.
- Find APIDot Generate Music docs, model pages, or integration notes.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Generate Music Workflow

APIDot Generate Music jobs follow the shared async media generation pattern:

1. Choose the Generate Music request mode from the current APIDot docs.
2. Submit the music request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status or music detail with the documented APIDot APIs for local tests.
5. Use callback_url or webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final audio URLs and metadata only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's music task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Generate Music model page | https://apidot.ai/models/generate-music |
| Build with Generate Music | https://apidot.ai/docs/generate-music |
| Read music detail docs | https://apidot.ai/docs/music-detail |
| Browse APIDot music models | https://apidot.ai/models/music |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Generate Music routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-music-generation-api` when the user needs broad music generation guidance across APIDot music workflows.
- Use `apidot-minimax-music-2-6-api` when the user specifically asks for MiniMax Music 2.6.
- Use this skill when the user is specifically building with Generate Music through APIDot.
- Ask whether the user needs a full song, instrumental track, vocal style, background music, or music detail retrieval before choosing a request mode.
- Persist `task_id`, selected model, user ID, prompt metadata, request status, and final audio URLs together.
- Treat callback_url and webhook handlers as idempotent. Duplicate deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, generated audio URLs, callback_url values, or webhook payloads with sensitive user content.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Generate Music model page: https://apidot.ai/models/generate-music
- Generate Music docs: https://apidot.ai/docs/generate-music
- Music detail docs: https://apidot.ai/docs/music-detail
- Music models: https://apidot.ai/models/music
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
