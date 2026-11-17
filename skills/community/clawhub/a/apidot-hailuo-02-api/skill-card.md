## Description:

Use APIDot for Hailuo 02 API workflows, including MiniMax Hailuo 02, Hailuo 02 Pro, text-to-video API, image-to-video API, first frame and last frame guidance, physics-aware short video, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Hailuo 02 integration questions to APIDot documentation, model pages, async workflow notes, polling guidance, and webhook planning for video generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys or private media details could be exposed during a real API integration.

Mitigation: Keep APIDOT_API_KEY server-side, use a backend secret manager or environment variable, and avoid logging API keys, private prompts, media URLs, callback URLs, or generated video URLs.

Risk: Webhook delivery or polling logic could create duplicate records or inconsistent job state.

Mitigation: Persist task_id with request metadata and final URLs, treat webhook handlers as idempotent, and only store final video URLs after a terminal success state.

Risk: Model-specific fields, limits, availability, or commercial terms may change outside the skill artifact.

Mitigation: Use the current APIDot docs and model pages for live request fields, limits, model availability, and commercial terms before implementing or making API calls.

## Reference(s):

- [APIDot Hailuo 02 Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Hailuo 02 Docs](https://apidot.ai/docs/hailuo-02)
- [APIDot Hailuo 02 Model Page](https://apidot.ai/models/hailuo-02)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown guidance with links and implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; does not execute code, make network requests, or store credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
