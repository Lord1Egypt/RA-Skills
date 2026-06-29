---
name: apidot-veo-3-1-api
description: "Use APIDot for Veo 3.1 API workflows, including Google Veo API, veo3.1-lite, veo3.1-fast, veo3.1-quality, text-to-video API, image-to-video API, reference image video, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs."
homepage: https://apidot.ai/models/veo-3-1
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    requires:
      bins:
        - curl
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Veo 3.1 API

Use APIDot as a Veo 3.1-focused API surface for text-to-video, image-to-video, reference-guided video, polling, and webhook workflows.

This skill is for routing Veo 3.1 questions to the right APIDot docs, examples, reference notes, async integration pattern, and optional user-run submit helper.

This ClawHub package contains `SKILL.md`, non-executable notes in `references/api.md`, and one optional script at `scripts/submit_veo_3_1.sh`. The package includes no install-time automation, review automation helpers, background jobs, bundled API clients, automatic network calls, or stored credentials. The script runs only when a user explicitly invokes it with a reviewed JSON payload and a server-side `APIDOT_API_KEY` environment variable.

## When To Use

Use this skill when the user asks to:

- Build a Veo 3.1 API integration with APIDot.
- Generate videos from prompts, source images, reference images, or frame guidance.
- Use Google Veo API, Veo 3.1, veo3.1-lite, veo3.1-fast, veo3.1-quality, or related Veo model entries through APIDot.
- Choose between Veo 3.1 request modes.
- Implement APIDot async Veo jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Veo 3.1 docs, model pages, or runnable examples.
- Submit a reviewed Veo 3.1 payload from a trusted server-side shell when the user explicitly asks for a live request.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Only run `scripts/submit_veo_3_1.sh` from a trusted server-side shell.
- Review every payload before submission. Do not place API keys in payload files, prompt text, filenames, logs, screenshots, or command history.
- Treat prompts, source media URLs, generated video URLs, callback URLs, customer data, and task IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Veo 3.1 Workflow

APIDot Veo 3.1 generation usually follows an async task pattern:

1. Choose the Veo 3.1 model entry and request mode from the current APIDot docs.
2. Submit the video generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or the matching APIDot GitHub example.

## Model Routing

Start from the user's Veo task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Veo 3.1 model page | https://apidot.ai/models/veo-3-1 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with Veo 3.1 | https://apidot.ai/docs/veo-3-1 |
| Use runnable Veo 3.1 examples | https://github.com/APIDotAI/veo-3.1-api |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Veo 3.1 model routing, request planning, and async workflow notes.

For Veo 3.1 variants and request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

## Optional Submit Script

Use `scripts/submit_veo_3_1.sh` only when the user explicitly asks to submit a Veo 3.1 task and has already reviewed the JSON payload.

- Input is a JSON payload file path or JSON from standard input.
- The script requires `APIDOT_API_KEY` in the server-side environment.
- The script requires `curl`.
- The script submits the payload to the APIDot generation submit endpoint.
- The script does not create payloads, poll status, register webhooks, store credentials, write local state, save generated media, or print API keys.
- After a successful submit, save the returned `data.task_id` privately and follow APIDot docs for polling or webhook handling.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use this skill when the user is specifically building with Veo 3.1 or Google Veo API through APIDot.
- Ask which Veo task the user needs before choosing a model-specific example: text-to-video, image-to-video, frame-guided, or reference-guided video.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source media URLs before submitting workflows that depend on images or references.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Veo 3.1 model page: https://apidot.ai/models/veo-3-1
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Veo 3.1 docs: https://apidot.ai/docs/veo-3-1
- Veo 3.1 examples: https://github.com/APIDotAI/veo-3.1-api
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
