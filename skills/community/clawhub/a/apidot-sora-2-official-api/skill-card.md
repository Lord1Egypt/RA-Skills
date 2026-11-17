## Description:

Guides agents through APIDot Sora 2 Official API workflows for prompt-to-video, image-guided video, async task submission, polling, status handling, and webhook integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Sora 2 Official integration work to APIDot documentation, examples, model pages, and async job patterns. It helps plan prompt-to-video, image-guided video, polling, and webhook workflows without bundling executable code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY, prompts, private media URLs, callback URLs, or generated video URLs could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep the API key in a backend secret store or server environment, and redact prompts, media URLs, callback URLs, API keys, and generated video URLs from logs and shared output.

Risk: APIDot model availability, supported fields, limits, and commercial terms may change over time.

Mitigation: Verify current APIDot documentation and model pages before preparing payloads, making API calls, or describing product terms.

Risk: Live API calls may send user prompts or media references to APIDot before the user has confirmed a safe server-side environment.

Mitigation: Do not make live API calls unless the user explicitly asks and provides an appropriate server-side environment.

## Reference(s):

- [APIDot Sora 2 Official Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Sora 2 Official Docs](https://apidot.ai/docs/sora-2-official)
- [APIDot Sora 2 Official Model Page](https://apidot.ai/models/sora-2-official)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot API Key Dashboard](https://apidot.ai/dashboard/api-key)
- [APIDot Sora 2 Official Examples](https://github.com/APIDotAI/sora-2-official-api)
- [APIDot General Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown text with optional code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable files, automatic network calls, bundled clients, or stored credentials are included.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
