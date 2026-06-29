# APIDot Gemini 3 Reference

This reference gives agents a safer, non-executable summary for APIDot Gemini 3 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/gemini-3
- API docs: https://apidot.ai/docs/gemini-3
- Quickstart: https://apidot.ai/docs/quickstart
- Error guidance: https://apidot.ai/docs/errors
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Gemini 3 on APIDot is for production chat, multimodal reasoning when supported, coding assistants, long-context analysis, streaming responses, and Google-style generateContent workflows when the current docs expose them.

Do not assume request details from another chat model family. Check the APIDot Gemini 3 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the application expects native Gemini generateContent semantics or a chat-completions style interface.
- Whether the workflow needs streaming, multimodal inputs, coding-assistant behavior, long-context analysis, or structured output planning.
- Which roles, content parts, tool definitions, media references, and response fields the current APIDot docs support.
- Where the backend will persist request metadata, user identity, usage records, and error details if auditability is needed.
- Which prompts, media references, tool inputs, private context, and generated outputs must be kept out of public logs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

Gemini 3 chat workflows may not need the shared generated-media async task pattern. Start from the live APIDot Gemini 3 docs and follow the documented request and response style for the selected model entry.

For any workflow that uses APIDot task-style behavior, persist the returned task identifier before retries or status checks, and treat any callback or retry handling as idempotent.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate conversation roles, content parts, media references, tool definitions, and streaming choices before sending requests from a backend.
- Keep request metadata, model selection, user identity, and usage records together when the application needs traceability.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, customer data, tool arguments, private context, media references, or generated responses that may contain sensitive data.
- Do not copy fields from another chat model family unless the APIDot docs show the same field for Gemini 3.
