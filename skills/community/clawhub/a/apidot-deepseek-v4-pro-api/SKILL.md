---
name: apidot-deepseek-v4-pro-api
description: "Use APIDot for DeepSeek V4 Pro API workflows, including OpenAI-compatible chat, 1M-token long-context reasoning, complex coding, document review, agent planning, streaming planning, usage tracking, API key safety guidance, and APIDot docs routing."
homepage: https://apidot.ai/models/deepseek-v4-pro
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot DeepSeek V4 Pro API

Use APIDot as a DeepSeek V4 Pro-focused API surface for OpenAI-compatible chat, million-token long-context reasoning, complex coding, document review, agent planning, streaming-aware UI behavior, and usage-aware routing.

This skill is for routing DeepSeek V4 Pro questions to the right APIDot docs, model page, reference notes, and integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This release contains `SKILL.md` plus non-executable notes in `references/api.md`. It includes no executable files, install-time automation, review automation helpers, bundled API clients, automatic network calls, or stored credentials.

## Start on APIDot

Use these APIDot entry points when coming from ClawHub:

- Open the DeepSeek V4 Pro model page: https://apidot.ai/models/deepseek-v4-pro
- Read DeepSeek V4 Pro API docs: https://apidot.ai/docs/deepseek-v4-pro
- Open the account dashboard: https://apidot.ai/dashboard/api-key
- Use general APIDot examples: https://github.com/APIDotAI/apidot-examples

## Search Terms

Use this skill for searches and requests phrased as DeepSeek V4 Pro, DeepSeek V4, deepseek-v4-pro, DeepSeek API, million-token reasoning, long-context chat, complex coding, codebase analysis, document review, agent planning, or APIDot DeepSeek API.

## When To Use

Use this skill when the user asks to:

- Build a DeepSeek V4 Pro API integration with APIDot.
- Use DeepSeek V4 Pro for long-context reasoning, complex coding, codebase review, or document analysis.
- Plan OpenAI-compatible chat request handling, response parsing, streaming behavior, or usage tracking.
- Choose between DeepSeek V4 Pro and faster or cheaper APIDot chat models.
- Design prompts for deep reasoning tasks without assuming hidden request fields.
- Find APIDot DeepSeek V4 Pro docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Treat prompts, source documents, customer data, tool inputs, generated responses, usage records, and request IDs as sensitive unless the user explicitly says they can be shared.
- Do not invent API facts, commercial terms, model availability, reliability claims, performance claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## DeepSeek V4 Pro Workflow

APIDot DeepSeek V4 Pro integrations usually start by choosing the correct OpenAI-compatible chat path and model-routing policy:

1. Confirm whether the application expects OpenAI-compatible chat behavior.
2. Use DeepSeek V4 Pro for tasks that need deeper reasoning than a Flash or routine chat model.
3. Keep messages, system instructions, token limits, sampling controls, and streaming choices within the documented request shape.
4. Read response fields and usage fields from the APIDot wrapper described in the current docs.
5. Store request metadata, model choice, user identity, and usage records server-side when auditability or cost routing matters.
6. Keep prompts, private documents, customer data, tool inputs, and generated responses out of public logs.

Do not guess model-specific payload fields. If the user needs copyable request examples, point them to the current APIDot docs or general APIDot examples.

## Model Routing

Start from the user's DeepSeek V4 Pro task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot DeepSeek V4 Pro model page | https://apidot.ai/models/deepseek-v4-pro |
| Build with DeepSeek V4 Pro | https://apidot.ai/docs/deepseek-v4-pro |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Review errors and retries | https://apidot.ai/docs/errors |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

For DeepSeek V4 Pro request modes, prefer the live APIDot model page and docs page. Do not copy request fields from another chat model family unless the APIDot docs show the same field.

Use `references/api.md` for a local, non-executable summary of DeepSeek V4 Pro model routing, request planning, and integration notes.

## Integration Guidance

- Use `apidot-chat-api` when the user needs broad APIDot chat guidance across several model families.
- Use this skill when the user is specifically building with DeepSeek V4 Pro through APIDot.
- Ask whether the application needs long-context coding, full-codebase analysis, document review, deep reasoning, agent planning, support escalation, or streaming before choosing request shape.
- Prefer the current APIDot docs for supported model IDs, request fields, streaming behavior, response wrappers, and usage fields.
- Validate conversation roles, content shape, token settings, and streaming choices before sending requests from a backend.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging API keys, private prompts, customer data, private documents, tool arguments, private context, or generated responses that may contain sensitive data.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- DeepSeek V4 Pro model page: https://apidot.ai/models/deepseek-v4-pro
- DeepSeek V4 Pro docs: https://apidot.ai/docs/deepseek-v4-pro
- Quickstart: https://apidot.ai/docs/quickstart
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
