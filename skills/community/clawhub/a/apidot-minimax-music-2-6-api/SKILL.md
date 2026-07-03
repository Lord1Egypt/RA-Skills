---
name: apidot-minimax-music-2-6-api
description: "Use APIDot for MiniMax Music 2.6 API workflows, including AI music generation, lyrics, instrumentals, audio export planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing."
homepage: https://apidot.ai/models/minimax-music-2-6
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot MiniMax Music 2.6 API

Use APIDot as a MiniMax Music 2.6-focused API surface for AI music generation, lyrics, instrumentals, audio export planning, polling, and webhook delivery.

This skill is for routing MiniMax Music 2.6 questions to the right APIDot docs, model pages, reference notes, and async integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a MiniMax Music 2.6 API integration with APIDot.
- Generate songs, instrumentals, backing tracks, lyrics, or prompt-driven audio through APIDot.
- Plan music task submission, task status polling, webhook callbacks, or final audio URL handling.
- Choose MiniMax Music 2.6 instead of a broad APIDot music category workflow.
- Find APIDot MiniMax Music 2.6 docs, model pages, or integration notes.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## MiniMax Music 2.6 Workflow

APIDot MiniMax Music 2.6 jobs follow the shared async media generation pattern:

1. Choose the MiniMax Music 2.6 request mode from the current APIDot docs.
2. Submit the music request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final audio URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's music task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot MiniMax Music 2.6 model page | https://apidot.ai/models/minimax-music-2-6 |
| Build with MiniMax Music 2.6 | https://apidot.ai/docs/minimax-music-2-6 |
| Browse APIDot music models | https://apidot.ai/models/music |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of MiniMax Music 2.6 model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-music-generation-api` when the user needs broad music generation guidance across APIDot music workflows.
- Use this skill when the user is specifically building with MiniMax Music 2.6 through APIDot.
- Ask whether the user needs song generation, instrumental generation, lyrics, backing track generation, or audio export guidance before choosing a request mode.
- Persist `task_id`, selected model, user ID, prompt metadata, request status, and final audio URLs together.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, generated audio URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- MiniMax Music 2.6 model page: https://apidot.ai/models/minimax-music-2-6
- MiniMax Music 2.6 docs: https://apidot.ai/docs/minimax-music-2-6
- Music models: https://apidot.ai/models/music
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
