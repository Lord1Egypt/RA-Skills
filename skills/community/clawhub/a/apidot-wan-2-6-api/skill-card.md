## Description:

Use APIDot for Wan 2.6 API workflows, including Wan 2.6 text-to-video API, image-to-video API, video-to-video API, multi-shot video, 720p and 1080p planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Wan 2.6 integration questions to APIDot documentation and plan text-to-video, image-to-video, video-to-video, polling, and webhook workflows. It is documentation-only and does not execute API calls or store credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys, private prompts, media URLs, generated video URLs, or callback URLs could be exposed if copied into frontend code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep APIDOT_API_KEY server-side, use a backend secret manager or environment variable, and avoid logging private prompts, media URLs, generated video URLs, callback URLs, or API keys.

Risk: Live API calls or stale model-specific payload assumptions could cause unintended requests or incorrect integration guidance.

Mitigation: Make live API calls only when the user explicitly configures a safe backend environment, and use current APIDot docs and model pages for request fields, availability, limits, and commercial terms.

## Reference(s):

- [APIDot Wan 2.6 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Wan 2.6 Docs](https://apidot.ai/docs/wan-2-6)
- [APIDot Wan 2.6 Model Page](https://apidot.ai/models/wan-2-6)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with documentation links and integration planning notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable automation, bundled API client, stored credentials, or automatic network calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
