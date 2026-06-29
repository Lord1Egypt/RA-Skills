---
name: apidot-video-generation-api
description: "Use APIDot for video generation API workflows, including text-to-video API, image-to-video API, reference image video, Veo 3.1 API, Seedance 2 API, Sora API, Kling API, async task submission, polling, task status, and webhook integration based on APIDot docs."
homepage: https://apidot.ai/models
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Video Generation API

Use APIDot as a video-focused API surface for text-to-video, image-to-video, frame-guided video, reference image video, polling, and webhook workflows.

This skill is for routing video generation questions to the right APIDot docs, examples, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains only `SKILL.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a video generation API integration with APIDot.
- Generate video from text prompts, source images, reference images, or first/last frames.
- Use Veo 3.1, Seedance, Sora, Kling, Happy Horse, or related video model APIs through APIDot.
- Choose between video model families or video request modes.
- Implement APIDot async video jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot video docs, model pages, or runnable video examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, pricing, model availability, reliability claims, refund behavior, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Video Workflow

APIDot video generation usually follows an async task pattern:

1. Choose the video model and request mode from the current APIDot docs.
2. Submit the generation request through the APIDot async generation endpoint.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the APIDot status endpoint for local tests.
5. Use `callback_url` webhooks for production queues and long-running user workflows.
6. Store final result URLs only after the task reaches a terminal success state.

Use polling for local testing and webhooks for production systems where users may close the page before a video finishes.

## Model Routing

Start from the user's video task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot models | https://apidot.ai/models |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with Veo 3.1 | https://apidot.ai/docs/veo-3-1 |
| Use runnable Veo 3.1 examples | https://github.com/APIDotAI/veo-3.1-api |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Seedance, Sora, Kling, Happy Horse, or other video model families, prefer the live APIDot model page and docs page for that exact model. Do not copy request fields from another model family unless the APIDot docs show the same field.

## Integration Guidance

- Use the broad `apidot-ai-api` skill when the user needs APIDot across image, video, chat, music, and 3D.
- Use this skill when the user is specifically building video generation, video polling, or video webhook workflows.
- Ask which video task the user needs before choosing a model-specific example: text-to-video, image-to-video, frame-guided, or reference image.
- Persist `task_id`, selected model, user ID, source media references, and request status together.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private media URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Models: https://apidot.ai/models
- API key dashboard: https://apidot.ai/dashboard/api-key
- Veo 3.1 docs: https://apidot.ai/docs/veo-3-1
- Veo 3.1 examples: https://github.com/APIDotAI/veo-3.1-api
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
