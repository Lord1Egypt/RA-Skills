## Description:

Routes agents to APIDot Wan 2.7 Image documentation and integration guidance for text-to-image, image editing, image-to-image, multi-reference generation, async polling, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to find current APIDot Wan 2.7 Image docs and plan integrations for image generation, editing, async task polling, and webhook delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into frontend code, logs, repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid displaying or logging it.

Risk: Live API calls could run from an uncontrolled environment.

Mitigation: Make live APIDot requests only from a controlled server-side environment.

Risk: Model-specific fields, availability, limits, or commercial terms may change in APIDot documentation.

Mitigation: Use the current APIDot docs and model pages before preparing payloads or making product claims.

## Reference(s):

- [APIDot Wan 2.7 Image Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Wan 2.7 Image Model Page](https://apidot.ai/models/wan-2-7-image)
- [APIDot Wan 2.7 Image Docs](https://apidot.ai/docs/wan-2-7-image)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with links and integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable code, persistence, network calls, or stored credentials.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
