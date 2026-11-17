## Description:

Use APIDot for Grok Imagine Image Quality API workflows, including high-fidelity image generation, image editing, reference-guided images, 1K, 2K, output formats, task_id, polling, webhooks, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration teams use this skill to route Grok Imagine Image Quality questions to APIDot documentation, plan async image generation or editing workflows, and handle task IDs, polling, webhooks, and API-key safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid displaying or logging it.

Risk: Prompts, source image URLs, generated image URLs, callback URLs, customer data, and task IDs may contain sensitive information.

Mitigation: Treat these values as sensitive by default and avoid sharing or logging them unless the user explicitly approves.

Risk: Model-specific payload fields, limits, pricing, or availability may change over time.

Mitigation: Use the current APIDot model page and API docs as the source of truth before preparing copyable request examples.

Risk: Unintended live API calls could consume credits or send private data to APIDot.

Mitigation: Make live calls only when the user explicitly asks and provides a safe backend environment.

## Reference(s):

- [Local APIDot Grok Imagine Image Quality Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-grok-imagine-image-quality-api)
- [APIDot Docs](https://apidot.ai/docs)
- [Grok Imagine Image Quality Model Page](https://apidot.ai/models/grok-imagine-image-quality)
- [Grok Imagine Image Quality API Docs](https://apidot.ai/docs/grok-imagine-image-quality)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown text with links and code-oriented integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; live API calls require an explicit user request and a safe server-side environment.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
