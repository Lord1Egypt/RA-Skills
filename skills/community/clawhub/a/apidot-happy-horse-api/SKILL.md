---
name: apidot-happy-horse-api
description: "Use APIDot for Happy Horse API workflows, including Alibaba Happy Horse video generation, text-to-video API, image-to-video API, reference-to-video API, video editing API, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs."
homepage: https://apidot.ai/models/happy-horse
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Happy Horse API

Use APIDot as a Happy Horse-focused API surface for text-to-video, image-to-video, reference-to-video, video editing, polling, and webhook workflows.

This skill is for routing Happy Horse questions to the right APIDot docs, examples, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Happy Horse API integration with APIDot.
- Generate videos from prompts, source images, reference images, or short source clips.
- Use Alibaba Happy Horse, Happy Horse video generation, reference-to-video, or video editing through APIDot.
- Choose between Happy Horse request modes.
- Implement APIDot async Happy Horse jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Happy Horse docs, model pages, or runnable examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Happy Horse Workflow

APIDot Happy Horse generation usually follows an async task pattern:

1. Choose the Happy Horse request mode from the current APIDot docs.
2. Submit the video generation or edit request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or the matching APIDot GitHub example.

## Model Routing

Start from the user's Happy Horse task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Happy Horse model page | https://apidot.ai/models/happy-horse |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with Happy Horse | https://apidot.ai/docs/happy-horse |
| Use runnable Happy Horse examples | https://github.com/APIDotAI/happy-horse-api |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Happy Horse request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Happy Horse model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use this skill when the user is specifically building with Happy Horse through APIDot.
- Ask which Happy Horse task the user needs before choosing a model-specific example: text-to-video, image-to-video, reference-to-video, or video editing.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source media URLs before submitting workflows that depend on images or video inputs.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Happy Horse model page: https://apidot.ai/models/happy-horse
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Happy Horse docs: https://apidot.ai/docs/happy-horse
- Happy Horse examples: https://github.com/APIDotAI/happy-horse-api
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
