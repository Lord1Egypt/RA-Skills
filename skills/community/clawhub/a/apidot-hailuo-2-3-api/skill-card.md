## Description:

Use APIDot for Hailuo 2.3 API workflows, including MiniMax Hailuo 2.3, text-to-video API, image-to-video API, start image guidance, prompt optimization, duration and resolution planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Hailuo 2.3 integration questions to APIDot documentation, plan text-to-video or image-to-video workflows, and handle async task submission, polling, and webhook delivery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Store the key only in a backend secret store or server-side environment variable and avoid logging private prompts, media URLs, generated video URLs, callback URLs, or credentials.

Risk: Model fields, pricing, limits, or availability may change after the skill release.

Mitigation: Verify current Hailuo 2.3 request fields and commercial details from APIDot's live docs before making real API calls.

Risk: Async video jobs can lose state or create duplicate visible results if task IDs and callbacks are handled loosely.

Mitigation: Persist task_id, selected model, source media references, request status, and final video URLs together, and make webhook handlers idempotent.

## Reference(s):

- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Hailuo 2.3 Model Page](https://apidot.ai/models/hailuo-2-3)
- [APIDot Hailuo 2.3 Docs](https://apidot.ai/docs/hailuo-2-3)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Hailuo 2.3 Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with optional code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable behavior is bundled.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
