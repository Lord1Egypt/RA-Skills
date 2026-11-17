---
name: apidot-gpt-5-2-api
description: "Use APIDot for GPT 5.2 API workflows, including OpenAI-compatible chat, legacy professional-work compatibility, 400K-token long-context synthesis, agentic coding handoffs, chart reasoning, streaming planning, usage tracking, API key safety guidance, and APIDot docs routing."
homepage: https://apidot.ai/models/gpt-5-2
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot GPT 5.2 API

Use APIDot as a GPT 5.2-focused API surface for legacy professional-work compatibility, long-context synthesis, agentic coding handoffs, chart reasoning, streaming-aware chat, and usage-aware routing.

This skill is for routing GPT 5.2 questions to the right APIDot docs, model page, reference notes, and integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the GPT 5.2 model page: https://apidot.ai/models/gpt-5-2
- Read GPT 5.2 API docs: https://apidot.ai/docs/gpt-5-2
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## Search Terms

Use this skill for searches and requests phrased as GPT 5.2, GPT 5 2, gpt-5.2, gpt-5-2, GPT API, OpenAI-compatible chat, 400K context, long-context synthesis, agentic coding, chart reasoning, or APIDot GPT API.

## When To Use

Use this skill when the user asks to:

- Build a GPT 5.2 API integration with APIDot.
- Use GPT 5.2 for long-context synthesis, coding handoffs, chart reasoning, or compatibility with an existing GPT 5.2 workflow.
- Plan OpenAI-compatible chat request handling, response parsing, streaming behavior, or usage tracking.
- Compare GPT 5.2 with newer APIDot chat models for routing decisions.
- Find APIDot GPT 5.2 docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Treat prompts, source documents, customer data, tool inputs, generated responses, usage records, and request IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## GPT 5.2 Workflow

APIDot GPT 5.2 integrations usually start by choosing the right chat path and compatibility requirement:

1. Confirm whether the application needs OpenAI-compatible chat behavior or another workflow described by the current docs.
2. Use GPT 5.2 when an existing workflow depends on its context, cost, or behavior profile.
3. Keep system instructions, conversation history, token limits, sampling controls, and streaming choices within the documented request shape.
4. Read response fields and usage fields from the current APIDot docs.
5. Store request metadata, model choice, user identity, and usage records server-side when auditability or cost routing matters.
6. Keep prompts, private documents, customer data, tool inputs, and generated responses out of public logs.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's GPT 5.2 task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot GPT 5.2 model page | https://apidot.ai/models/gpt-5-2 |
| Build with GPT 5.2 | https://apidot.ai/docs/gpt-5-2 |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Review errors and retries | https://apidot.ai/docs/errors |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For GPT 5.2 request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another chat model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of GPT 5.2 model routing, request planning, and integration notes.

## Integration Guidance

- Use `apidot-chat-api` when the user needs broad APIDot chat guidance across several model families.
- Use `apidot-gpt-5-5-api` or `apidot-gpt-5-4-api` when the user specifically needs those newer GPT model entries.
- Use this skill when the user is specifically building with GPT 5.2 through APIDot.
- Ask whether the application needs long-context synthesis, compatibility routing, chart reasoning, coding handoffs, or streaming before choosing request shape.
- Prefer the current APIDot docs for supported model IDs, request fields, streaming behavior, response wrappers, and usage fields.
- Validate conversation roles, content shape, token settings, and streaming choices before sending requests from a backend.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging API keys, private prompts, customer data, private documents, tool arguments, private context, or generated responses that may contain sensitive data.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- GPT 5.2 model page: https://apidot.ai/models/gpt-5-2
- GPT 5.2 docs: https://apidot.ai/docs/gpt-5-2
- Quickstart: https://apidot.ai/docs/quickstart
- Account dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
