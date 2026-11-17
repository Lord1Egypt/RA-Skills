## Description:

Use APIDot for Veo 3.1 Official API workflows, including model routing, text-to-video and image-to-video planning, async task submission, polling, webhook delivery, and safe APIDOT_API_KEY handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration teams use this skill to route APIDot Veo 3.1 Official questions to the right docs, model pages, and async workflow guidance. It helps plan text-to-video, image-guided video, first/last-frame control, reference media, native audio, polling, and webhook delivery without bundling executable automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY could be exposed if a user places it in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in a server-side environment variable or backend secret store, and avoid logging credentials.

Risk: Prompts, media URLs, generated video URLs, callback URLs, and results may contain private workflow data.

Mitigation: Avoid logging or displaying private prompts, media URLs, callback URLs, generated URLs, or task results unless the user explicitly approves the handling.

Risk: Model fields, availability, pricing, and commercial terms may change outside the skill artifact.

Mitigation: Verify current model-specific request fields, limits, availability, pricing, and commercial terms in APIDot's live docs before making real API calls.

## Reference(s):

- [APIDot Veo 3.1 Official Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Veo 3.1 Official Model Page](https://apidot.ai/models/veo-3-1-official)
- [APIDot Veo 3.1 Official API Docs](https://apidot.ai/docs/veo-3-1-official)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-veo-3-1-official-api)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with links and non-executable integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable files, stored credentials, or automatic API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
