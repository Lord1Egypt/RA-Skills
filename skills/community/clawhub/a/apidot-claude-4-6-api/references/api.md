# APIDot Claude 4.6 Reference

This reference gives agents a safer, non-executable summary for APIDot Claude 4.6 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/claude-4-6
- API docs: https://apidot.ai/docs/claude-4-6
- Quickstart: https://apidot.ai/docs/quickstart
- Error guidance: https://apidot.ai/docs/errors
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Claude 4.6 on APIDot is for production chat, coding agents, long-context analysis, support assistants, tool-use planning, and streaming response workflows when supported by the selected request mode.

Documented Claude 4.6 model entries may include Sonnet and Opus variants. Do not assume the same request details across variants. Check the APIDot Claude 4.6 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the application expects Anthropic Messages semantics or a chat-completions style interface.
- Whether the workflow needs streaming, tool use, coding-agent behavior, long-context reasoning, or support-assistant responses.
- Which conversation roles, system instructions, message history, and tool definitions the current APIDot docs support.
- Where the backend will persist request metadata, user identity, usage records, and error details if auditability is needed.
- Which prompts, tool inputs, private context, and generated outputs must be kept out of public logs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

Claude 4.6 chat workflows may not need the shared generated-media async task pattern. Start from the live APIDot Claude 4.6 docs and follow the documented request and response style for the selected model entry.

For any workflow that uses APIDot task-style behavior, persist the returned task identifier before retries or status checks, and treat any callback or retry handling as idempotent.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate conversation roles, content shape, tool definitions, and streaming choices before sending requests from a backend.
- Keep request metadata, model selection, user identity, and usage records together when the application needs traceability.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging API keys, private prompts, customer data, tool arguments, private context, or generated responses that may contain sensitive data.
- Do not copy fields from another chat model family unless the APIDot docs show the same field for Claude 4.6.
