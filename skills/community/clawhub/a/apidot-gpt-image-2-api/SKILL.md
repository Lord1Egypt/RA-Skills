---
name: apidot-gpt-image-2-api
description: "Use APIDot for GPT Image 2 API workflows, including text-to-image API, image editing API, image-to-image API, reference image generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs."
homepage: https://apidot.ai/models/gpt-image-2
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot GPT Image 2 API

Use APIDot as a GPT Image 2-focused API surface for text-to-image generation, image editing, image-to-image workflows, polling, and webhook delivery.

This skill is for routing GPT Image 2 questions to the right APIDot docs, examples, reference notes, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a GPT Image 2 API integration with APIDot.
- Generate images from prompts, product briefs, campaign concepts, or design directions.
- Edit or transform source images with reference-guided workflows.
- Use GPT Image 2 through APIDot for image generation or image editing.
- Implement APIDot async image jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot GPT Image 2 docs, model pages, or runnable examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## GPT Image 2 Workflow

APIDot GPT Image 2 generation usually follows an async task pattern:

1. Choose the GPT Image 2 request mode from the current APIDot docs.
2. Submit the generation or edit request through the documented APIDot async generation flow.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the documented task status API for local tests.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final image URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or the matching APIDot GitHub example.

## Model Routing

Start from the user's GPT Image 2 task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot GPT Image 2 model page | https://apidot.ai/models/gpt-image-2 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with GPT Image 2 | https://apidot.ai/docs/gpt-image-2 |
| Use runnable GPT Image 2 examples | https://github.com/APIDotAI/gpt-image-2-api |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For GPT Image 2 request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another image model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of GPT Image 2 model routing, request planning, and async workflow notes.

## Integration Guidance

- Use `apidot-image-generation-api` when the user needs broad image generation guidance across several model families.
- Use this skill when the user is specifically building with GPT Image 2 through APIDot.
- Ask which image task the user needs before choosing a model-specific example: text-to-image, image editing, image-to-image, product visual, UI mockup, ad creative, or reference-guided generation.
- Persist `task_id`, selected model, user ID, source media references, request status, and final image URLs together.
- Validate source image URLs before submitting workflows that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private image URLs, generated image URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- GPT Image 2 model page: https://apidot.ai/models/gpt-image-2
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- API key dashboard: https://apidot.ai/dashboard/api-key
- GPT Image 2 docs: https://apidot.ai/docs/gpt-image-2
- GPT Image 2 examples: https://github.com/APIDotAI/gpt-image-2-api
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
