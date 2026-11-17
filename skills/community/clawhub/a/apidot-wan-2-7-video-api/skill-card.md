## Description:

Use APIDot for Wan 2.7 Video API workflows, including text-to-video API, image-to-video API, reference-to-video, edit-video, Wan 2.7, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Wan 2.7 Video integration questions to APIDot documentation, examples, and async workflow guidance for text-to-video, image-to-video, reference-to-video, edit-video, polling, and webhook-based delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real APIDot API use requires an APIDOT_API_KEY that could be exposed if placed in browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep API keys in server-side environment variables or a backend secret manager, and avoid logging keys, private prompts, private media URLs, generated video URLs, or callback URLs.

Risk: Wan 2.7 Video request fields, model availability, limits, and commercial terms may change in APIDot's live service.

Mitigation: Use the current APIDot model page and API documentation for model-specific fields and product details; do not invent payload fields or copy fields from another model family unless APIDot documents them for Wan 2.7 Video.

Risk: Async video workflows can lose task state or duplicate visible results if polling and webhook callbacks are not reconciled carefully.

Mitigation: Persist task_id, selected model, user ID, source media references, request status, and final video URLs together; treat webhook handlers as idempotent and retry only transient failures with backoff.

## Reference(s):

- [APIDot Wan 2.7 Video Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Wan 2.7 Video Model Page](https://apidot.ai/models/wan-2-7-video)
- [Wan 2.7 Video API Docs](https://apidot.ai/docs/wan-2-7-video)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with optional code snippets and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; it does not include executable files, bundled API clients, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
