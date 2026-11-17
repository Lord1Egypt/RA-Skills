## Description:

Use APIDot for Kling 2.1 API workflows, including Kling 2.1 Standard, Kling 2.1 Pro, image-to-video API, start-frame guidance, optional end-frame control, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route APIDot Kling 2.1 integration work to the right model pages, API docs, async task workflow, polling, and webhook guidance. It supports planning image-to-video workflows while keeping API keys and private media handled server-side.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if placed in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid displaying or logging it.

Risk: Private prompts, media URLs, callback URLs, or generated video links could leak through application logs or debugging output.

Mitigation: Avoid logging sensitive prompts and URLs; redact these values before storage, support, or debugging workflows.

Risk: Model-specific request fields, limits, availability, or commercial terms may change outside the skill artifact.

Mitigation: Verify current APIDot docs and model pages before sending real requests or relying on product details.

## Reference(s):

- [Local APIDot Kling 2.1 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Kling 2.1 Model Page](https://apidot.ai/models/kling-2-1)
- [APIDot Kling 2.1 API Docs](https://apidot.ai/docs/kling-2-1)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-kling-2-1-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with optional code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable payloads, automatic network calls, or stored credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
