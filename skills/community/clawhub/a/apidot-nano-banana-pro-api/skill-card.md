## Description:

Use APIDot for Nano Banana Pro API workflows, including image generation API, image editing API, image-to-image API, reference image generation, prompt-based image creation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route Nano Banana Pro image generation and editing requests to APIDot documentation, examples, and async integration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret store and avoid logging keys or private request data.

Risk: APIDot API fields, model availability, limits, or commercial terms may change outside this documentation-only skill.

Mitigation: Review current APIDot docs and model pages before preparing requests or making live API calls.

Risk: External GitHub examples may contain behavior that is outside the packaged skill artifact.

Mitigation: Inspect external examples before running them and adapt them only in a safe server-side environment.

## Reference(s):

- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Nano Banana Pro Model Page](https://apidot.ai/models/nano-banana-pro)
- [APIDot Nano Banana Pro API Docs](https://apidot.ai/docs/nano-banana-pro)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Nano Banana Pro Examples](https://github.com/APIDotAI/nano-banana-pro-api)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Nano Banana Pro Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with API integration notes and links to current APIDot references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, bundled clients, network calls, or stored credentials.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
