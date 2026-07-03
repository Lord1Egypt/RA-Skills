---
name: apidot-chat-api
description: "Use APIDot for chat API workflows, including OpenAI-compatible chat completions, coding assistants, reasoning models, multimodal assistant routing, streaming planning, server-side API key safety, and APIDot chat model docs routing."
homepage: https://apidot.ai/models/chat
metadata:
  openclaw:
    homepage: https://apidot.ai/docs
    primaryEnv: APIDOT_API_KEY
    envVars:
      - name: APIDOT_API_KEY
        required: false
        description: APIDot API key for real API calls. Store it server-side only.
---

# APIDot Chat API

Use APIDot as a chat-focused API surface for OpenAI-compatible chat completions, coding assistants, reasoning workflows, multimodal assistant routing, and server-side API key safety.

This skill is for routing APIDot chat questions to the right model pages, chat docs, model-specific skill, and integration guidance. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This category skill contains only `SKILL.md`. It includes no executable files, install-time automation, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Build a chat API integration with APIDot.
- Use APIDot for coding assistants, reasoning agents, support bots, internal copilots, or multimodal chat workflows.
- Choose between APIDot chat and coding model families.
- Route to Claude, Gemini, DeepSeek, or other APIDot chat model pages after checking live availability.
- Plan streaming, request storage, rate-limit handling, or server-side API key handling for chat workloads.
- Find APIDot chat docs, model pages, or examples.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent API facts, commercial terms, model availability, reliability claims, benchmark claims, or competitor comparisons.
- Use current APIDot docs and model pages for model-specific request fields and current product details.

## Chat Routing

Start from the user's chat task, then open the matching APIDot source:

| User Goal | Start Here |
| --- | --- |
| Browse APIDot chat model lineup | https://apidot.ai/models/chat |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Use Claude 4.6 through APIDot | https://apidot.ai/models/claude-4-6 |
| Use Claude 4.5 through APIDot | https://apidot.ai/models/claude-4-5 |
| Use Gemini 3 through APIDot | https://apidot.ai/models/gemini-3 |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Use the live APIDot model catalog before selecting a model-specific route. Do not route to a model page that currently returns 404.

## Integration Guidance

- Use `apidot-ai-api` when the user needs APIDot across image, video, chat, music, and 3D.
- Use `apidot-claude-4-6-api`, `apidot-claude-4-5-api`, or `apidot-gemini-3-api` when the user names those exact models.
- Use this skill when the user is choosing or building chat workflows across APIDot chat models.
- Ask whether the user needs coding, long-context reasoning, support automation, structured output, streaming, or multimodal behavior before choosing a model.
- Keep API keys, system prompts, private user messages, transcripts, and logs server-side or in approved secure storage.
- Avoid logging private prompts, model outputs with sensitive content, API keys, or user identifiers.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Chat models: https://apidot.ai/models/chat
- Quickstart: https://apidot.ai/docs/quickstart
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
