# APIDot Claude Opus 4.7 Reference

This reference gives agents a safer, non-executable summary for APIDot Claude Opus 4.7 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/claude-opus-4-7
- API docs: https://apidot.ai/docs/claude-opus-4-7
- Quickstart: https://apidot.ai/docs/quickstart
- Error guidance: https://apidot.ai/docs/errors
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Claude Opus 4.7 on APIDot is for Claude-compatible chat workflows that need 1M-token long-context reasoning, complex coding, long-horizon agents, self-checking workflows, high-resolution visual review, streaming-aware UI behavior, and tool-use planning when supported by the selected request mode.

Documented Claude Opus 4.7 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `claude-opus-4-7` | Long-context reasoning, complex coding, agent planning, self-checking workflows, and visual review. |

Do not assume every Claude request shape is supported. Check the APIDot Claude Opus 4.7 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the application expects Claude Messages semantics or another chat interface described by the current docs.
- Whether the task needs Claude Opus 4.7 specifically or can use another APIDot chat model.
- Whether the workflow needs streaming, tool use, long-context reasoning, complex coding, document analysis, visual review, or agent planning.
- Which conversation roles, system instructions, message history, tool definitions, thinking controls, output settings, token limits, and response fields the current APIDot docs support.
- Where the backend will persist request metadata, user identity, model choice, usage records, and error details if auditability is needed.
- Which prompts, documents, tool inputs, private context, and generated outputs must be kept out of public logs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Chat Flow

Claude Opus 4.7 chat workflows may not need the generated-media async task pattern. Start from the live APIDot Claude Opus 4.7 docs and follow the documented request and response style for the selected path.

For any workflow that uses APIDot task behavior, persist the returned task identifier before retries or status checks, and treat callback or retry handling as idempotent.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate conversation roles, content shape, tool definitions, thinking controls, and streaming choices before sending requests from a backend.
- Keep request metadata, model selection, user identity, and usage records together when the application needs traceability.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging API keys, private prompts, customer data, private documents, tool arguments, private context, or generated responses that may contain sensitive data.
- Do not copy fields from another Claude or chat model family unless the APIDot docs show the same field for Claude Opus 4.7.
