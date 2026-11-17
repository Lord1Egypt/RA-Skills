## Description:

Use APIDot for Kling 2.6 Motion Control API workflows, including motion transfer, controllable animation, async task submission, polling, webhook integration, and docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Kling 2.6 Motion Control integration work through APIDot documentation, including motion transfer, controllable character animation, async task handling, polling, and webhook planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY could be exposed if used in browser code, public repos, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and avoid echoing secrets into logs or user-visible output.

Risk: Private media URLs, generated video URLs, or callback URLs could leak through logging or debugging output.

Mitigation: Avoid logging private prompts, private media URLs, callback URLs, API keys, and generated video URLs.

Risk: Stale or guessed request fields could lead to failed or misleading APIDot workflows.

Mitigation: Verify current model availability, request fields, limits, and commercial terms in APIDot's live documentation before making API calls.

## Reference(s):

- [APIDot Kling 2.6 Motion Control Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Kling 2.6 Motion Control Model Page](https://apidot.ai/models/kling-2-6-motion-control)
- [Kling 2.6 Motion Control API Docs](https://apidot.ai/docs/kling-2-6-motion-control)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with documentation links and optional code or configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; live APIDot calls require explicit user request and a safe server-side environment.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
