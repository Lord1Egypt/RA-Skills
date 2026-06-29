---
name: apidot-image-generation-api
description: "Use APIDot for image generation API and image editing API workflows, including text-to-image API, image-to-image API, GPT Image 2 API, Nano Banana API, Nano Banana Pro API, Seedream API, Flux API, async task submission, polling, task status, and webhook integration based on APIDot docs."
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

# APIDot Image Generation API

Use APIDot as an image-focused API surface for text-to-image generation, image editing, image-to-image workflows, polling, and webhook delivery.

This skill is for routing image generation questions to the right APIDot docs, examples, and async integration pattern. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

## When To Use

Use this skill when the user asks to:

- Build an image generation API integration with APIDot.
- Generate images from prompts, product briefs, campaign ideas, UI mockup requests, or design directions.
- Edit or transform source images using reference images.
- Use GPT Image 2, Nano Banana, Nano Banana Pro, Seedream, Flux, or related image model APIs through APIDot.
- Implement APIDot async image jobs with task submission, task status polling, or webhook callbacks.
- Find APIDot image docs, model pages, or runnable image examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, pricing, model availability, reliability claims, refund behavior, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Image Workflow

APIDot image generation usually follows an async task pattern:

1. Choose the image model and generation mode from the current APIDot docs.
2. Submit the generation or edit request through the APIDot async generation endpoint.
3. Save the returned `data.task_id` immediately.
4. Poll task status with the APIDot status endpoint for local tests.
5. Use `callback_url` webhooks for production queues or user workflows that may outlive the current page.
6. Store final image URLs only after the task reaches a terminal success state.

Use polling for local testing and webhooks for production systems where users may close the page before image processing finishes.

## Model Routing

Start from the user's image task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot models | https://apidot.ai/models |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Build with GPT Image 2 | https://apidot.ai/docs/gpt-image-2 |
| Use runnable GPT Image 2 examples | https://github.com/APIDotAI/gpt-image-2-api |
| Use runnable Nano Banana 2 examples | https://github.com/APIDotAI/nano-banana-2-api |
| Use runnable Nano Banana Pro examples | https://github.com/APIDotAI/nano-banana-pro-api |
| Use runnable Seedream 4.5 examples | https://github.com/APIDotAI/seedream-4.5-api |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Flux, Seedream, Nano Banana, GPT Image, or other image model families, prefer the live APIDot model page and docs page for that exact model. Do not copy request fields from another model family unless the APIDot docs show the same field.

## Integration Guidance

- Use the broad `apidot-ai-api` skill when the user needs APIDot across image, video, chat, music, and 3D.
- Use this skill when the user is specifically building image generation, image editing, image polling, or image webhook workflows.
- Ask which image task the user needs before choosing a model-specific example: text-to-image, image editing, image-to-image, product visual, UI mockup, ad creative, or reference-guided generation.
- Persist `task_id`, selected model, user ID, source media references, request status, and final image URLs together.
- Validate source image URLs before submitting requests that depend on reference images.
- Treat webhook handlers as idempotent. Duplicate callback deliveries should not create duplicate visible results.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, private image URLs, or callback URLs.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Models: https://apidot.ai/models
- API key dashboard: https://apidot.ai/dashboard/api-key
- GPT Image 2 docs: https://apidot.ai/docs/gpt-image-2
- GPT Image 2 examples: https://github.com/APIDotAI/gpt-image-2-api
- Nano Banana 2 examples: https://github.com/APIDotAI/nano-banana-2-api
- Nano Banana Pro examples: https://github.com/APIDotAI/nano-banana-pro-api
- Seedream 4.5 examples: https://github.com/APIDotAI/seedream-4.5-api
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
