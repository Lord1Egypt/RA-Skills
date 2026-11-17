## Description:

Use APIDot for Kling 3.0 API workflows, including Kling 3.0 Standard, Kling 3.0 Pro, Kling 3.0 4K, text-to-video API, image-to-video API, multi-shot video, Native Audio, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external builders use this skill to route Kling 3.0 video-generation integration work through APIDot documentation, including model selection, async task submission, polling, webhook delivery, and API-key handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys or private media details could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in a server-side secret store and avoid logging API keys, private prompts, private media URLs, generated video URLs, and callback URLs.

Risk: Live APIDot calls may spend credits or submit real media-generation jobs.

Mitigation: Authorize live API calls only when the user explicitly asks and provides a safe server-side environment.

Risk: Outdated or guessed model fields could produce incorrect Kling 3.0 integration guidance.

Mitigation: Use current APIDot documentation and model pages for model-specific request fields, availability, limits, and commercial terms.

## Reference(s):

- [APIDot Kling 3.0 Reference](references/api.md)
- [APIDot Documentation](https://apidot.ai/docs)
- [APIDot Kling 3.0 Model Page](https://apidot.ai/models/kling-3-0)
- [APIDot Kling 3.0 API Docs](https://apidot.ai/docs/kling-3-0)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with documentation links and integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no executable files, bundled API clients, live API calls, or credential storage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
