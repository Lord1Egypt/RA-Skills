## Description:

Use APIDot for Seedance 1.0 Pro API workflows, including ByteDance Seedance 1.0 Pro, text-to-video API, image-to-video API, short video generation, 720p and 1080p planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Seedance 1.0 Pro integration work through APIDot documentation, including text-to-video, image-to-video, async task handling, polling, and webhook planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid displaying it in generated examples.

Risk: Private prompts, media URLs, callback URLs, or generated video URLs could be shared in logs or public contexts.

Mitigation: Treat those values as sensitive workflow data and redact them from logs, public issues, screenshots, and shared conversations.

Risk: Model-specific request fields, availability, limits, or commercial terms may change outside the skill artifact.

Mitigation: Use current APIDot docs and model pages as the source of truth before preparing copyable payloads or production integrations.

## Reference(s):

- [APIDot Seedance 1.0 Pro Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Seedance 1.0 Pro Docs](https://apidot.ai/docs/seedance-1-0-pro)
- [Seedance 1.0 Pro Model Page](https://apidot.ai/models/seedance-1-0-pro)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with optional code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; the skill includes no executable files, bundled clients, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
