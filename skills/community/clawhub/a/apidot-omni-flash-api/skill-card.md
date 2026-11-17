## Description:

Use APIDot for Omni Flash API workflows, including multimodal video generation, prompt-to-video, image-guided video, video-guided revision, 720p, 1080p, 4K, task_id, polling, webhooks, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Omni Flash API work to APIDot documentation, model pages, async task patterns, polling, and webhook guidance for video generation integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY or other credentials could be exposed if placed in client code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid echoing secrets in generated guidance.

Risk: APIDot model fields, limits, availability, and commercial terms may change after the skill release.

Mitigation: Verify the current APIDot Omni Flash docs and model page before preparing real requests or making product commitments.

Risk: Prompts, source media URLs, generated video URLs, callback URLs, customer data, and task IDs can contain sensitive information.

Mitigation: Treat these values as sensitive, avoid logging them, and share them only when the user explicitly confirms they are safe to disclose.

Risk: The skill may be invoked for broad video-generation phrasing even when Omni Flash is not explicitly named.

Mitigation: Confirm the user wants APIDot Omni Flash guidance before applying model-specific routing or assumptions.

## Reference(s):

- [APIDot Omni Flash Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Omni Flash Docs](https://apidot.ai/docs/omni-flash)
- [APIDot Omni Flash Model Page](https://apidot.ai/models/omni-flash)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; does not execute API calls or store credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
