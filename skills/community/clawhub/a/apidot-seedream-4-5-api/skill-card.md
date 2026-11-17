## Description:

Use APIDot for Seedream 4.5 API workflows, including image generation, image editing, image-to-image, reference image generation, prompt-based image creation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan APIDot Seedream 4.5 image generation and editing integrations, choose the relevant APIDot documentation path, and handle async task polling or webhook delivery safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in a backend secret store or server-side environment variable and avoid echoing credentials in generated guidance.

Risk: Live API calls may submit private prompts, source image URLs, callback URLs, or generated image URLs to APIDot.

Mitigation: Only make live calls when the user intentionally provides a safe server-side runtime, and minimize logging of prompts, private media URLs, generated URLs, and callback URLs.

Risk: Model-specific payload fields, availability, limits, or commercial terms may change after the skill release.

Mitigation: Use the current APIDot docs and model page as the source of truth before producing copyable request examples or integration decisions.

## Reference(s):

- [APIDot docs](https://apidot.ai/docs)
- [APIDot Seedream 4.5 model page](https://apidot.ai/models/seedream-4-5)
- [APIDot Seedream 4.5 API docs](https://apidot.ai/docs/seedream-4-5)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot API key dashboard](https://apidot.ai/dashboard/api-key)
- [Local API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with documentation links and integration planning notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; agents should consult current APIDot docs before producing copyable request payloads.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
