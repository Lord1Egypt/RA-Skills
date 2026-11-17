---
name: apidot-gemini-3-5-flash-api
description: "Use APIDot for Gemini 3.5 Flash API workflows, including stable Gemini Native generateContent, streamGenerateContent, long-context chat, coding iteration, knowledge-base Q&A, streaming planning, usage tracking, API key safety guidance, and APIDot docs routing."
homepage: https://apidot.ai/models/gemini-3-5-flash
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Gemini 3.5 Flash API

Use APIDot as a Gemini 3.5 Flash-focused API surface for stable Gemini Native chat, long-context reasoning, coding iteration, knowledge-base Q&A, streaming-aware UI behavior, and usage-aware routing.

This skill is for routing Gemini 3.5 Flash questions to the right APIDot docs, model page, reference notes, and integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the Gemini 3.5 Flash model page: https://apidot.ai/models/gemini-3-5-flash
- Read Gemini 3.5 Flash API docs: https://apidot.ai/docs/gemini-3-5-flash
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## Search Terms

Use this skill for searches and requests phrased as Gemini 3.5 Flash, Gemini 3 5 Flash, gemini-3.5-flash, gemini-3-5-flash, Gemini Native, generateContent, streamGenerateContent, long-context chat, coding assistant, knowledge-base Q&A, or APIDot Gemini API.

## When To Use

Use this skill when the user asks to:

- Build a Gemini 3.5 Flash API integration with APIDot.
- Use stable Gemini Native request semantics through APIDot.
- Implement fast production chat, coding iteration, long-context analysis, or knowledge-base Q&A.
- Plan non-streaming or streaming Gemini responses.
- Read APIDot-wrapped Gemini response fields and usage metadata.
- Find APIDot Gemini 3.5 Flash docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Treat prompts, source documents, customer data, tool inputs, generated responses, usage records, and request IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Gemini 3.5 Flash Workflow

APIDot Gemini 3.5 Flash integrations usually start by choosing the correct Gemini Native route and response mode:

1. Confirm whether the application needs a normal JSON response or streaming response.
2. Keep the Gemini 3.5 Flash model identity in the documented path and keep the request body focused on supported Gemini Native fields.
3. Keep contents, system instruction, generation settings, safety settings, tools, and tool configuration within the documented request shape.
4. Read non-streaming responses and usage metadata from the APIDot wrapper described in the current docs.
5. Treat streaming responses as event streams only when the client is prepared to consume them.
6. Keep prompts, source documents, customer data, tool inputs, and generated responses out of public logs.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's Gemini 3.5 Flash task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot Gemini 3.5 Flash model page | https://apidot.ai/models/gemini-3-5-flash |
| Build with Gemini 3.5 Flash | https://apidot.ai/docs/gemini-3-5-flash |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Review errors and retries | https://apidot.ai/docs/errors |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For Gemini 3.5 Flash request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another Gemini or chat model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of Gemini 3.5 Flash model routing, request planning, and integration notes.

## Integration Guidance

- Use `apidot-chat-api` when the user needs broad APIDot chat guidance across several model families.
- Use `apidot-gemini-3-api` when the user specifically needs the existing Gemini 3 family coverage.
- Use this skill when the user is specifically building with stable Gemini 3.5 Flash through APIDot.
- Ask whether the application needs fast chat, long-context analysis, coding iteration, knowledge-base Q&A, tool planning, or streaming before choosing request shape.
- Prefer the current APIDot docs for supported paths, request fields, streaming behavior, response wrappers, and usage fields.
- Validate conversation roles, content parts, tool definitions, and streaming choices before sending requests from a backend.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging API keys, private prompts, customer data, private documents, tool arguments, private context, or generated responses that may contain sensitive data.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Gemini 3.5 Flash model page: https://apidot.ai/models/gemini-3-5-flash
- Gemini 3.5 Flash docs: https://apidot.ai/docs/gemini-3-5-flash
- Quickstart: https://apidot.ai/docs/quickstart
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
