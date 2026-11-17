## Description:

Use APIDot for Kling O1 Image API workflows, including cost-effective image editing, reference-guided image changes, text-to-image planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external builders use this skill to plan APIDot Kling O1 Image integrations, route to current APIDot docs, and design async image editing or generation workflows with task tracking, polling, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys or private image URLs could be exposed through frontend code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep API keys in server-side environment variables or a backend secret manager, and avoid logging API keys, private prompts, private image URLs, generated image URLs, or callback URLs.

Risk: Model-specific request fields, availability, limits, or commercial terms may be outdated if copied from memory or another model family.

Mitigation: Use the current APIDot Kling O1 Image docs and model page as the source of truth before preparing payloads or making product claims.

Risk: Async image jobs can lose state or create duplicate visible results if task IDs and webhook callbacks are not handled carefully.

Mitigation: Persist task_id, selected model, user ID, source media references, request status, and final image URLs together, and make webhook handlers idempotent.

## Reference(s):

- [APIDot Kling O1 Image Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Kling O1 Image Model Page](https://apidot.ai/models/kling-o1-image)
- [Kling O1 Image API Docs](https://apidot.ai/docs/kling-o1-image)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with optional code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; live API calls require an explicit user request and a safe server-side environment.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
