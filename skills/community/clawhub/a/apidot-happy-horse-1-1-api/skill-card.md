## Description:

Use APIDot for Happy Horse 1.1 API workflows, including Alibaba Happy Horse 1.1, audio-synced short video, text-to-video API, image-to-video API, reference-to-video API, 720p or 1080p planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan APIDot Happy Horse 1.1 integrations for text-to-video, image-to-video, reference-to-video, polling, and webhook workflows. It helps route users to current APIDot docs and non-executable implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY could be exposed if used in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY server-side in environment variables or a backend secret manager, and avoid logging credentials or private request data.

Risk: APIDot request fields, limits, model availability, or commercial terms may change after release.

Mitigation: Confirm current Happy Horse 1.1 request fields and terms in the live APIDot docs before building live integrations.

Risk: Webhook retries or duplicate deliveries could create duplicate visible results in production integrations.

Mitigation: Implement webhook handlers as idempotent and persist task_id, selected model, source media references, status, and final video URLs together.

## Reference(s):

- [APIDot Happy Horse 1.1 Reference](references/api.md)
- [Happy Horse 1.1 model page](https://apidot.ai/models/happy-horse-1-1)
- [Happy Horse 1.1 API docs](https://apidot.ai/docs/happy-horse-1-1)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with documentation links and integration planning notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable code, automated API calls, or stored credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
