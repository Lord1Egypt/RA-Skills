## Description:

Use APIDot for Happy Horse API workflows, including Alibaba Happy Horse video generation, text-to-video API, image-to-video API, reference-to-video API, video editing API, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route APIDot Happy Horse integration questions to the right docs, examples, request-planning notes, async task handling guidance, polling workflow, and webhook guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An APIDot API key could be exposed through browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY server-side in environment variables or a backend secret manager, and avoid logging or displaying it.

Risk: Private prompts, media URLs, generated video URLs, or callback URLs could be exposed during integration work.

Mitigation: Avoid logging private prompts or media URLs, and treat generated video and callback URLs as sensitive workflow data.

Risk: Happy Horse request fields, model availability, limits, or commercial terms may change outside the local skill notes.

Mitigation: Use the current APIDot docs and model pages as the source of truth before preparing payloads or making live calls.

## Reference(s):

- [APIDot docs](https://apidot.ai/docs)
- [APIDot Happy Horse model page](https://apidot.ai/models/happy-horse)
- [APIDot Happy Horse API docs](https://apidot.ai/docs/happy-horse)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Happy Horse examples](https://github.com/APIDotAI/happy-horse-api)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Happy Horse Reference](references/api.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with links and integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable automation, bundled API clients, network calls, or stored credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
