## Description:

Use APIDot for image generation API and image editing API workflows, including text-to-image API, image-to-image API, GPT Image 2 API, Nano Banana API, Nano Banana Pro API, Seedream API, Flux API, async task submission, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route APIDot image generation, image editing, async polling, and webhook integration work to the right APIDot documentation, examples, and implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if placed in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Store APIDOT_API_KEY only in server-side environment variables or a backend secret manager, and avoid logging keys, private prompts, private image URLs, or callback URLs.

Risk: Live APIDot API calls may spend credits or submit real media and prompts.

Mitigation: Only authorize live API calls when the user explicitly asks and provides a safe server-side environment.

Risk: Model fields, pricing, availability, and product behavior may change over time.

Mitigation: Verify current APIDot docs and model pages before relying on model-specific request fields, pricing, availability, or operational claims.

## Reference(s):

- [APIDot API Docs](https://apidot.ai/docs)
- [APIDot Image Models](https://apidot.ai/models/image)
- [APIDot Models](https://apidot.ai/models)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [GPT Image 2 Docs](https://apidot.ai/docs/gpt-image-2)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [GPT Image 2 API Examples](https://github.com/APIDotAI/gpt-image-2-api)
- [Nano Banana 2 API Examples](https://github.com/APIDotAI/nano-banana-2-api)
- [Nano Banana Pro API Examples](https://github.com/APIDotAI/nano-banana-pro-api)
- [Seedream 4.5 API Examples](https://github.com/APIDotAI/seedream-4.5-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code or shell snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; may guide optional APIDot API calls when the user explicitly authorizes live use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
