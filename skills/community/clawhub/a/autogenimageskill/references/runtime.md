# Runtime Notes

## Relationship to `gpt_image`

The local `gpt_image` project has two relevant implementations:

- `frontend/generate-gpt-image2.js`: a direct one-shot Node script that posts to a Responses endpoint, streams SSE, extracts the final `image_generation_call.result`, and writes a PNG.
- `frontend/server.js`: a long-running relay service with provider fallback, job polling, image-to-image support, sessions, free quota, purchase-key redemption, and provider admin endpoints.

This skill preserves the same core generation contract but keeps credentials out of the skill package.

## Direct Generation Contract

Direct `official` and `proxy` modes:

1. Build a Responses payload with `model: gpt-5.4`.
2. Add a single tool `{ "type": "image_generation", "model": "gpt-image-2" }`.
3. Force `tool_choice` to `image_generation`.
4. Request `stream: true`.
5. Parse SSE events until an `image_generation_call` output item contains `result`.
6. Decode `result` as base64 and write the PNG.

If an input image is provided, send `input` as a user message with `input_text` and `input_image`.

## Relay Generation Contract

Reserved mode assumes a relay shaped like the local `frontend/server.js`:

- `POST /api/session`
- `POST /api/session/register`
- `POST /api/keys`
- `POST /api/generate/jobs`
- `GET /api/generate/jobs/:jobId`
- `GET /api/generate/jobs/:jobId/image`

The relay may protect job status and image download with `X-User-Id`; keep this header whenever a user ID is available.

## OpenClaw and Hermes Packaging

The reference `tonghuashun-ifind-skill` uses a GitHub repo whose actual skill root is a subdirectory containing:

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/*`
- `references/*`

OpenClaw and ClawHub expect a skill folder with `SKILL.md` plus optional supporting text files. This project follows that source shape: the publishable skill root is `autoGenImageSkill/`. Keep this repository as generated source unless the user explicitly asks for an installation step later.

The `SKILL.md` frontmatter includes:

- `name`
- `version`
- `description`
- `metadata.openclaw.requires.bins: ["node"]`

Do not add an install script or copy files into an OpenClaw skill directory unless explicitly requested.

## Security and Logging

- Do not print API keys, permission codes, purchase keys, or provider tokens.
- Do not copy the original `providers.json` secrets into this skill.
- Summaries may include endpoint host/path, provider name, job ID, output path, byte count, and revised prompt.
- If a relay returns detailed provider failures, summarize only status, provider, retryability, and short error text.
