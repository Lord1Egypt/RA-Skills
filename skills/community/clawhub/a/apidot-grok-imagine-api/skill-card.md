## Description:

Use APIDot for Grok Imagine API workflows, including xAI Grok Imagine image generation, image editing, text-to-video, image-to-video, Grok Imagine Video 1.5, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route APIDot Grok Imagine integration questions to the right model pages, docs, examples, and async workflow guidance for image, editing, and video generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, private prompts, private media URLs, generated result URLs, or callback URLs could be exposed through client code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep APIDOT_API_KEY server-side, use a backend secret manager or environment variable, and avoid logging private prompts, media URLs, generated URLs, callback URLs, or credentials.

Risk: Stale or guessed model-specific request fields could cause incorrect APIDot Grok Imagine integrations.

Mitigation: Verify current model availability, request fields, limits, and commercial terms in the live APIDot docs and model pages before making real calls.

Risk: Async media jobs can lose task state or mishandle duplicate webhook deliveries.

Mitigation: Persist task_id, selected model, user ID, source media references, request status, and final media URLs together, and make webhook handlers idempotent.

## Reference(s):

- [APIDot Grok Imagine Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-grok-imagine-api)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Grok Imagine Model Page](https://apidot.ai/models/grok-imagine)
- [APIDot Grok Imagine Docs](https://apidot.ai/docs/grok-imagine)
- [APIDot Grok Imagine Video 1.5 Docs](https://apidot.ai/docs/grok-imagine-video-1-5)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text guidance with links and implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, bundled API clients, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
