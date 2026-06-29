---
name: apidot-gemini-3-api
description: "Use APIDot for Gemini 3 API workflows, including Gemini 3 Flash Preview, Gemini 3 Pro Preview, native generateContent, streamGenerateContent, Gemini chat, coding assistants, streaming, tool planning, API key safety guidance, and APIDot docs routing."
homepage: https://apidot.ai/models/gemini-3
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Gemini 3 API

Use APIDot as a Gemini 3-focused API surface for native Gemini chat, generateContent workflows, streaming responses, coding assistants, production support bots, and Gemini-compatible request planning.

This skill is for routing Gemini 3 questions to the right APIDot docs, model pages, reference notes, and integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a Gemini 3 API integration with APIDot.
- Choose between Gemini 3 Flash Preview and Gemini 3 Pro Preview through APIDot.
- Use native Gemini request semantics through APIDot.
- Implement chat, coding assistant, support assistant, or tool-planning workflows.
- Plan non-streaming or streaming Gemini responses.
- Find APIDot Gemini 3 docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Gemini 3 Workflow

APIDot Gemini 3 integrations usually start by choosing the correct native Gemini route and model:

1. Confirm whether the application needs a normal JSON response or a streaming response.
2. Choose the Gemini 3 model from the current APIDot docs.
3. Keep conversation contents, system instructions, generation settings, safety settings, tools, and tool configuration within the documented native Gemini schema.
4. Read non-streaming responses from the APIDot wrapper described in the current docs.
5. Treat streaming responses as server-sent events if the selected route uses streaming.
6. Keep user prompts, tool inputs, private context, and API keys out of public logs.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Gemini 3 task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Gemini 3 model page | https://apidot.ai/models/gemini-3 |
| Build with Gemini 3 | https://apidot.ai/docs/gemini-3 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Review errors and retries | https://apidot.ai/docs/errors |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Gemini 3 request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another chat model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Gemini 3 model routing, request planning, and integration notes.

## Integration Guidance

- Use `apidot-ai-api` when the user needs a broad APIDot overview across image, video, chat, music, and 3D.
- Use this skill when the user is specifically building with Gemini 3 through APIDot.
- Ask whether the application needs lower-latency interactive chat, deeper reasoning, coding assistance, tool planning, or streaming before choosing request shape.
- Prefer the current APIDot docs for supported model IDs, request fields, streaming behavior, and response wrappers.
- Validate conversation roles and content parts before sending requests from a backend.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, customer data, tool arguments, private context, or generated responses that may contain sensitive data.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Gemini 3 model page: https://apidot.ai/models/gemini-3
- Gemini 3 docs: https://apidot.ai/docs/gemini-3
- Quickstart: https://apidot.ai/docs/quickstart
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
