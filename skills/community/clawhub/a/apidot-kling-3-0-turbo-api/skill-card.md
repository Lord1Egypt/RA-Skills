## Description:

Use APIDot for Kling 3.0 Turbo API workflows, including fast video previews, Kling 3.0 Turbo Standard, Kling 3.0 Turbo Pro, text-to-video, image-to-video, multi-shot video, multi_prompt, task_id, polling, webhooks, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route APIDot Kling 3.0 Turbo integration work to the right docs and plan async text-to-video, image-to-video, multi-shot, polling, and webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if placed in browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Store APIDOT_API_KEY only in server-side environment variables or a backend secret manager, and avoid echoing secrets into generated guidance.

Risk: Prompts, source media URLs, generated video URLs, callback URLs, customer data, and task IDs may reveal sensitive user or project data.

Mitigation: Treat generated media and task data as sensitive by default, persist only what the workflow needs, and avoid logging private prompts, URLs, callbacks, or task IDs.

Risk: Live API calls from unsafe environments can leak credentials or user data.

Mitigation: Only make live APIDot calls when the user explicitly asks and provides a controlled server-side environment.

Risk: Model-specific request fields, limits, availability, or commercial terms may change over time.

Mitigation: Use the current APIDot docs and model page as the source of truth before preparing copyable payloads or making product claims.

## Reference(s):

- [Local APIDot Kling 3.0 Turbo Reference](references/api.md)
- [APIDot Docs](https://apidot.ai/docs)
- [APIDot Kling 3.0 Turbo Docs](https://apidot.ai/docs/kling-3-0-turbo)
- [APIDot Kling 3.0 Turbo Model Page](https://apidot.ai/models/kling-3-0-turbo)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional API planning notes and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files or bundled API client; live API calls require an explicit user request and a safe server-side environment.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
