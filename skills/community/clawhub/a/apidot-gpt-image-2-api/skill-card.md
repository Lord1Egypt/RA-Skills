## Description:

Use APIDot for GPT Image 2 API workflows, including text-to-image API, image editing API, image-to-image API, reference image generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this documentation-only skill to route GPT Image 2 integration questions to APIDot documentation, examples, and async workflow guidance. It supports planning for image generation, image editing, task polling, and webhook-based delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, prompts, private image URLs, callback URLs, or generated URLs could be exposed if copied into frontend code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and avoid logging sensitive prompts, media URLs, callback URLs, generated URLs, or credentials.

Risk: Agents may treat the skill as a runnable client and attempt unintended live APIDot calls.

Mitigation: Treat the artifact as reference guidance only; make live APIDot calls only when explicitly requested and when a safe server-side environment is available.

Risk: Model availability, request fields, limits, or commercial terms may change after publication.

Mitigation: Check the live APIDot docs and model page before preparing copyable payloads or making claims about current product behavior.

## Reference(s):

- [APIDot GPT Image 2 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot GPT Image 2 Docs](https://apidot.ai/docs/gpt-image-2)
- [APIDot GPT Image 2 Model Page](https://apidot.ai/models/gpt-image-2)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot GPT Image 2 Examples](https://github.com/APIDotAI/gpt-image-2-api)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with API integration notes and links to current APIDot documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, bundled API client, stored credentials, or automatic network calls.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
