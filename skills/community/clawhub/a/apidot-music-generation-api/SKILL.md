---
name: apidot-music-generation-api
description: "Use APIDot for music generation API workflows, including text-to-music API, song generation API, Generate Music API, MiniMax Music 2.6 API, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs."
homepage: https://apidot.ai/models/music
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Music Generation API

Use APIDot as a music-focused API surface for text-to-music, song generation, audio generation, polling, and webhook workflows.

This skill is for routing music generation questions to the right APIDot docs, examples, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains only `SKILL.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a music generation API integration with APIDot.
- Generate songs, instrumentals, background music, or prompt-driven audio through APIDot.
- Use Generate Music, MiniMax Music 2.6, or related music model APIs through APIDot.
- Choose between music model families or music request modes.
- Implement APIDot async music jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot music docs, model pages, or runnable music examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, pricing, model availability, reliability claims, refund behavior, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Music Workflow

APIDot music generation usually follows an async task pattern:

1. Choose the music model and request mode from the current APIDot docs.
2. Submit the music generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final audio URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or the matching APIDot GitHub example.

## Model Routing

Start from the user's music task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot music models | https://apidot.ai/models/music |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with Generate Music | https://apidot.ai/docs/generate-music |
| Build with MiniMax Music 2.6 | https://apidot.ai/docs/minimax-music-2-6 |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For MiniMax, Generate Music, or other music model families, prefer the live APIDot model page and docs page for that exact model. Do not copy request fields from another model family unless the APIDot docs show the same field.

## Integration Guidance

- Use the broad `apidot-ai-api` skill when the user needs APIDot across image, video, chat, music, and 3D.
- Use this skill when the user is specifically building music generation, music polling, or music webhook workflows.
- Ask which music task the user needs before choosing a model-specific example: song generation, instrumental music, prompt-driven audio, or background music.
- Persist `task_id`, selected model, user ID, prompt metadata, request status, and final audio URLs together.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, generated audio URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Music models: https://apidot.ai/models/music
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Generate Music docs: https://apidot.ai/docs/generate-music
- MiniMax Music 2.6 docs: https://apidot.ai/docs/minimax-music-2-6
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
