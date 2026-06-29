---
name: apidot-seedance-2-api
description: "Use APIDot for Seedance 2 API workflows, including seedance-2-fast, text-to-video API, image-to-video API, native audio video generation, reference image video, reference video, reference audio, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs."
homepage: https://apidot.ai/models/seedance-2
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

# APIDot Seedance 2 API

Use APIDot as a Seedance 2-focused API surface for text-to-video, image-to-video, native-audio video generation, reference media workflows, polling, and webhook delivery.

This skill is for routing Seedance 2 questions to the right APIDot docs, examples, reference notes, async integration pattern, and optional user-run submit helper.

This ClawHub package contains `SKILL.md`, non-executable notes in `references/api.md`, and one optional script at `scripts/submit_seedance_2.sh`. The GitHub repository also keeps `skill-card.md` for public behavior, risk, and maintenance notes. The package includes no install-time automation, review automation helpers, background jobs, bundled API clients, automatic network calls, or stored credentials. The script runs only when a user explicitly invokes it with a reviewed JSON payload and a server-side `APIDOT_API_KEY` environment variable.

## When To Use

Use this skill when the user asks to:

- Build a Seedance 2 API integration with APIDot.
- Generate videos from prompts, source images, reference images, reference video, or reference audio.
- Use Seedance 2, seedance-2-fast, native audio video generation, or related Seedance model entries through APIDot.
- Choose between Seedance 2 request modes.
- Implement APIDot async Seedance jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot Seedance 2 docs, model pages, or runnable examples.
- Submit a reviewed Seedance 2 payload from a trusted server-side shell when the user explicitly asks for a live request.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Only run `scripts/submit_seedance_2.sh` from a trusted server-side shell.
- Review every payload before submission. Do not place API keys in payload files, prompt text, filenames, logs, screenshots, or command history.
- Do not invent API facts, commercial terms, model availability, reliability claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Seedance 2 Workflow

APIDot Seedance 2 generation usually follows an async task pattern:

1. Choose the Seedance 2 model entry and request mode from the current APIDot docs.
2. Submit the video generation request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final video URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or the matching APIDot GitHub example.

## Model Routing

Start from the user's Seedance task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Seedance 2 model page | https://apidot.ai/models/seedance-2 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with Seedance 2 | https://apidot.ai/docs/seedance-2 |
| Use runnable Seedance 2 examples | https://github.com/APIDotAI/seedance-2-api |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use `references/api.md` for a local, non-executable summary of Seedance 2 model routing, request planning, and async workflow notes.

For Seedance 2 variants and request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another video model family unless the APIDot docs show the same field.

## Optional Submit Script

Use `scripts/submit_seedance_2.sh` only when the user explicitly asks to submit a Seedance 2 task and has already reviewed the JSON payload.

- Input is a JSON payload file path or JSON from standard input.
- The script requires `APIDOT_API_KEY` in the server-side environment.
- The script requires `curl`.
- The script submits the payload to the APIDot generation submit endpoint.
- The script does not create payloads, poll status, register webhooks, store credentials, write local state, or save generated media.
- After a successful submit, save the returned `data.task_id` and follow APIDot docs for polling or webhook handling.

## Integration Guidance

- Use `apidot-video-generation-api` when the user needs broad video generation guidance across several model families.
- Use this skill when the user is specifically building with Seedance 2 through APIDot.
- Ask which Seedance task the user needs before choosing a model-specific example: text-to-video, image-to-video, reference image, reference video, reference audio, or native-audio video generation.
- Persist `task_id`, selected model, user ID, source media references, request status, and final video URLs together.
- Validate source media URLs before submitting workflows that depend on images, video, or audio references.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, generated video URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Seedance 2 model page: https://apidot.ai/models/seedance-2
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- Seedance 2 docs: https://apidot.ai/docs/seedance-2
- Seedance 2 examples: https://github.com/APIDotAI/seedance-2-api
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
