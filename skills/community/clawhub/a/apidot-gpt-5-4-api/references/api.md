# APIDot GPT 5.4 Reference

This reference gives agents a safer, non-executable summary for APIDot GPT 5.4 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/gpt-5-4
- API docs: https://apidot.ai/docs/gpt-5-4
- Quickstart: https://apidot.ai/docs/quickstart
- Error guidance: https://apidot.ai/docs/errors
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

GPT 5.4 on APIDot is for professional chat workflows that need spreadsheet analysis, document analysis, tool-oriented planning, coding and testing handoffs, streaming-aware UI behavior, and usage-based model routing when supported by the selected request mode.

Documented GPT 5.4 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `gpt-5.4` | Professional execution, documents, spreadsheets, tool planning, and code handoffs. |

Do not assume every OpenAI-adjacent request shape is supported. Check the APIDot GPT 5.4 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the application expects OpenAI-compatible chat behavior or another workflow described by the current docs.
- Whether the task needs GPT 5.4 specifically or can use another APIDot chat model.
- Whether the workflow needs streaming, code handoffs, spreadsheet analysis, document analysis, tool planning, or support escalation.
- Which conversation roles, system instructions, message history, sampling controls, token limits, and response fields the current APIDot docs support.
- Where the backend will persist request metadata, user identity, model choice, usage records, and error details if auditability is needed.
- Which prompts, documents, tool inputs, private context, and generated outputs must be kept out of public logs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Chat Flow

GPT 5.4 chat workflows may not need the generated-media async task pattern. Start from the live APIDot GPT 5.4 docs and follow the documented request and response style for the selected path.

For any workflow that uses APIDot task behavior, persist the returned task identifier before retries or status checks, and treat callback or retry handling as idempotent.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate conversation roles, content shape, token settings, and streaming choices before sending requests from a backend.
- Keep request metadata, model selection, user identity, and usage records together when the application needs traceability.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging API keys, private prompts, customer data, private documents, tool arguments, private context, or generated responses that may contain sensitive data.
- Do not copy fields from another chat model family unless the APIDot docs show the same field for GPT 5.4.
