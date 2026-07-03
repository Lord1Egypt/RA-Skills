---
name: apidot-model-catalog-api
description: "Use APIDot model catalog guidance to choose currently available APIDot image, video, chat, music, and 3D model pages, avoid offline model routes, prevent duplicate skill selection, and route users to the right APIDot docs and model-specific skills."
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

# APIDot Model Catalog API

Use APIDot model catalog guidance to choose currently available APIDot model pages across image, video, chat, music, and 3D workflows.

This skill is for routing model-selection questions to the right live APIDot model page, category skill, or model-specific skill. It is documentation-only: it includes no scripts, makes no network requests, and does not store credentials.

This category skill contains only `SKILL.md`. It includes no executable files, install-time automation, shell automation, bundled API clients, automatic network calls, or stored credentials.

## When To Use

Use this skill when the user asks to:

- Choose an APIDot model family before building an integration.
- Check whether a model route should use image, video, chat, music, or 3D guidance.
- Avoid routing to model pages that are not live on APIDot.
- Decide whether a broad category skill or exact model skill is the right starting point.
- Find APIDot model pages, docs, quickstart, examples, or API key guidance.
- Compare APIDot model routing options without inventing availability or pricing details.

## Security Rules

- Treat `APIDOT_API_KEY` as a secret.
- Keep APIDot API keys in server-side environment variables or a backend secret manager.
- Never place an API key in browser code, frontend bundles, public repos, logs, screenshots, or chat output.
- Do not make live API calls unless the user explicitly asks and provides a safe server-side environment.
- Do not invent model availability, commercial terms, reliability claims, performance claims, benchmark claims, or competitor comparisons.
- Use the current APIDot model catalog and model pages for model availability and current product details.

## Catalog Routing

Start from the user's task, then choose the narrowest confirmed-live APIDot route:

| User Goal | Start Here |
| --- | --- |
| Browse all APIDot models | https://apidot.ai/models |
| Browse image generation models | https://apidot.ai/models/image |
| Browse video generation models | https://apidot.ai/models/video |
| Browse chat and coding models | https://apidot.ai/models/chat |
| Browse music models | https://apidot.ai/models/music |
| Browse 3D models | https://apidot.ai/models/3d |
| Read APIDot API docs | https://apidot.ai/docs |
| Learn APIDot quickstart flow | https://apidot.ai/docs/quickstart |
| Use general APIDot examples | https://github.com/APIDotAI/apidot-examples |

Prefer exact model skills when they exist and the user names a specific model. Prefer category skills when the user is still choosing a model family.

## Skill Routing

- Use `apidot-ai-api` for broad APIDot integration questions across multiple model families.
- Use `apidot-image-generation-api`, `apidot-video-generation-api`, `apidot-chat-api`, `apidot-music-generation-api`, or `apidot-3d-generation-api` when the user has chosen a category but not a specific model.
- Use exact model skills such as `apidot-seedance-2-api`, `apidot-veo-3-1-api`, `apidot-gpt-image-2-api`, `apidot-generate-music-api`, or `apidot-kling-o1-image-api` when the user names that model.
- Before routing to a model-specific page that is not already covered by a skill, verify that the APIDot model page is live.
- Do not present local draft docs, local branch files, tests, or migration scripts as proof that a model is live.

## Integration Guidance

- Ask what the user is building: image, video, chat, music, 3D, or mixed media.
- Ask for the model name only when the task cannot be routed from the user's stated goal.
- Keep API keys server-side and avoid logging private prompts, private media URLs, generated result URLs, callback URLs, or user identifiers.
- For async media models, persist `task_id`, selected model, request status, user ID, and final media URLs together.
- For chat models, keep system prompts, private messages, transcripts, and API keys in approved secure storage.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.

## Official Links

- Website: https://apidot.ai
- Docs: https://apidot.ai/docs
- Models: https://apidot.ai/models
- Image models: https://apidot.ai/models/image
- Video models: https://apidot.ai/models/video
- Chat models: https://apidot.ai/models/chat
- Music models: https://apidot.ai/models/music
- 3D models: https://apidot.ai/models/3d
- Quickstart: https://apidot.ai/docs/quickstart
- API key dashboard: https://apidot.ai/dashboard/api-key
- Main examples: https://github.com/APIDotAI/apidot-examples
- GitHub organization: https://github.com/APIDotAI
- Support: support@apidot.ai
