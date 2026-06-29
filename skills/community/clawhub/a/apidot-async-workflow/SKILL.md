---
name: apidot-async-workflow
description: "Use APIDot async workflow for AI generation APIs, including task submission, task_id handling, polling API, task status API, callback_url, webhook API, retry guidance, idempotent webhook handling, image generation, video generation, music generation, and 3D generation based on APIDot docs."
homepage: https://apidot.ai/docs/webhooks
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Async Workflow

Use APIDot's async workflow for generation tasks that return a `task_id`, then complete through polling or webhook delivery.

This skill is for routing async integration questions to the right APIDot docs, examples, and production workflow guidance. It is documentation-only: it includes no executable files, setup-time automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build an async APIDot integration for image, video, music, or 3D generation.
- Understand task submission, `task_id` persistence, polling API, task status API, `callback_url`, or webhook API behavior.
- Decide when to use polling versus webhook delivery.
- Design backend storage for task state, result URLs, retries, and user ownership.
- Make webhook handlers idempotent and safe for duplicate callback delivery.
- Find APIDot async workflow docs, webhook docs, model pages, or runnable examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, pricing, model availability, reliability claims, refund behavior, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Async Workflow

Use this stable flow when explaining APIDot generation tasks:

1. Choose the model and request fields from the current APIDot docs.
2. Submit the generation request through the documented APIDot async generation flow.
3. Persist the returned `data.task_id` before waiting, retrying, polling, or showing progress.
4. Use the documented task status API for local testing, simple backend jobs, or short-lived workflows.
5. Use `callback_url` webhook delivery for production queues or user workflows that may outlive the current page.
6. Store final result URLs only after the task reaches a terminal success state.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or the matching APIDot GitHub example repository.

## Polling Guidance

- Use polling for local testing, admin tools, small backend jobs, and workflows where the user stays in the current session.
- Store `task_id`, selected model, request owner, request status, created time, and last checked time together.
- Use moderate polling intervals and stop polling after a terminal task state.
- Do not block a user-facing request lifecycle while waiting for long-running media generation.
- Treat unknown or delayed states as pending until the current APIDot docs say otherwise.

## Webhook Guidance

- Use webhook delivery when generation may take longer than the current page, tab, or request lifecycle.
- Pass `callback_url` only to a backend endpoint controlled by the application.
- Verify task ownership before attaching callback results to a user-visible record.
- Make webhook handlers idempotent because duplicate deliveries can happen.
- Persist callback events before downstream processing when the workflow needs auditability.
- Return a success response quickly after accepting a valid callback, then process heavier work in the backend.
- Avoid logging API keys, private prompts, source media URLs, final result URLs, or callback URLs.

## Retry And Failure Guidance

- Retry transient network or timeout failures with backoff.
- Do not retry invalid payloads unchanged.
- Keep submit retries separate from status polling retries so duplicate tasks are not created by accident.
- Reconcile webhook results and polling results by `task_id`.
- Use current APIDot docs for terminal statuses, error classes, and model-specific failure behavior.

## Model Routing

Start from the user's async workflow, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Read APIDot docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Implement webhooks | https://apidot.ai/docs/webhooks |
| Browse APIDot models | https://apidot.ai/models |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |
| Build image workflows | https://clawhub.ai/jiehao71727/apidot-image-generation-api |
| Build video workflows | https://clawhub.ai/jiehao71727/apidot-video-generation-api |
| Use the broad APIDot skill | https://clawhub.ai/jiehao71727/apidot-ai-api |

Use this skill for async workflow design across APIDot model families. Use the image, video, or broad APIDot skills when the user needs model-category guidance.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Models: https://apidot.ai/models
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
