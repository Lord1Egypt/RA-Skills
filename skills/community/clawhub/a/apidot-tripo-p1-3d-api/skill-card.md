## Description:

Use APIDot for Tripo P1 3D API workflows, including Tripo P1 API, text-to-3D API, image-to-3D API, 3D asset generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external ClawHub users use this documentation-only skill to plan APIDot Tripo P1 integrations for text-to-3D, image-to-3D, asynchronous task handling, polling, and webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys or private request data could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep APIDOT_API_KEY in a backend secret store or server-side environment variable, and avoid logging API keys, private prompts, source image URLs, generated asset URLs, or callback URLs.

Risk: APIDot model availability, request fields, limits, and commercial terms may change after the skill release.

Mitigation: Review the live APIDot docs and model page before making paid or production API calls, and do not invent model-specific payload fields.

Risk: Asynchronous 3D generation workflows can lose task state or duplicate visible assets if polling, retries, or webhooks are handled incorrectly.

Mitigation: Persist task_id with request state, use idempotent webhook handlers, retry transient failures with backoff, and do not retry invalid payloads unchanged.

## Reference(s):

- [APIDot Tripo P1 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Tripo P1 3D Docs](https://apidot.ai/docs/tripo-p1-3d)
- [APIDot Tripo P1 Model Page](https://apidot.ai/models/tripo-p1-3d)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with links and optional code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no live API calls unless explicitly requested and safely configured.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
