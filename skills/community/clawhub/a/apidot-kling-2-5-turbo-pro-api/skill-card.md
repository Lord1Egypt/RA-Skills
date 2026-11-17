## Description:

Kling 2.5 Turbo Pro API on APIDot for text-to-video, image-to-video, frame-guided video workflows, asynchronous task handling, polling, webhooks, API key safety, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to find the right APIDot Kling 2.5 Turbo Pro documentation paths and plan prompt-only, start-frame, or start-and-end-frame video generation integrations with asynchronous task handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or private generation inputs could be exposed when users adapt the guidance into live APIDot calls.

Mitigation: Keep APIDOT_API_KEY in server-side secrets, avoid logging private prompts or media URLs, and verify live request fields in APIDot documentation before making calls.

## Reference(s):

- [APIDot Kling 2.5 Turbo Pro Reference](references/api.md)
- [APIDot docs](https://apidot.ai/docs)
- [Kling 2.5 Turbo Pro model page](https://apidot.ai/models/kling-2-5-turbo-pro)
- [Kling 2.5 Turbo Pro API docs](https://apidot.ai/docs/kling-2-5-turbo-pro)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)
- [ClawHub skill page](https://clawhub.ai/jiehao71727/skills/apidot-kling-2-5-turbo-pro-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with optional code snippets and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; directs users to live APIDot documentation for current request fields.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
