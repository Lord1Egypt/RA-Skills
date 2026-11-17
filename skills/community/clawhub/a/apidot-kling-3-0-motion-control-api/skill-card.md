## Description:

Kling 3.0 Motion Control API on APIDot for kling 3 0 motion control, kling-3-0-motion-control, motion transfer, reference video to character image, dance transfer, action transfer, controllable animation, image-to-video, task_id, polling, webhooks, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this documentation-only skill to route APIDot Kling 3.0 Motion Control integration questions to current docs, model pages, async task patterns, polling, and webhook guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys, private media URLs, callback URLs, or generated video URLs could be exposed if copied into browser code, logs, screenshots, repositories, or chat output.

Mitigation: Keep APIDOT_API_KEY server-side, use a backend secret manager or environment variable, and avoid logging private media, callback, API key, or generated video URLs.

Risk: Model-specific request fields, limits, availability, or commercial terms may change outside this documentation-only artifact.

Mitigation: Use the current APIDot docs and model page before implementing requests, and do not rely on copied fields from other Kling or video model families.

Risk: Async motion-control workflows can create duplicate or inconsistent user-visible results if task IDs, statuses, or webhook callbacks are handled loosely.

Mitigation: Persist task_id, selected model, user ID, source media references, request status, and final URLs together; make webhook handlers idempotent.

## Reference(s):

- [APIDot Kling 3.0 Motion Control Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [Kling 3.0 Motion Control Model Page](https://apidot.ai/models/kling-3-0-motion-control)
- [Kling 3.0 Motion Control API Docs](https://apidot.ai/docs/kling-3-0-motion-control)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with references to current APIDot documentation and integration patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable payloads or automatic network calls.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
