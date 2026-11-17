## Description:

Use APIDot for FLUX.2 API workflows, including Flux 2 API, image generation API, image editing API, multi-reference editing, text-to-image, reference image generation, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route APIDot FLUX.2 image generation and editing questions to the right APIDot documentation, model pages, examples, and async integration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in a backend secret store or server-side environment variable and avoid echoing it in generated guidance or examples.

Risk: Private prompts, source image URLs, generated image URLs, or callback URLs could leak through logs or copied integration examples.

Mitigation: Avoid logging private prompts, image URLs, generated outputs, callback URLs, and other sensitive workflow metadata.

Risk: APIDot model fields, availability, limits, pricing, or commercial terms may change after this documentation-only skill was released.

Mitigation: Verify current APIDot docs, model pages, and pricing before making real API calls or committing to an integration plan.

## Reference(s):

- [APIDot FLUX.2 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot FLUX.2 Model Page](https://apidot.ai/models/flux-2)
- [APIDot FLUX.2 Docs](https://apidot.ai/docs/flux-2)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with documentation links and optional code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no bundled executable behavior, API client, network calls, or stored credentials.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
