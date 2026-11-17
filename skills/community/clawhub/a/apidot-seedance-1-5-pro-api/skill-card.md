## Description:

Use APIDot for Seedance 1.5 Pro API workflows, including ByteDance Seedance 1.5 Pro, text-to-video API, image-to-video API, synchronized audio planning, first frame and last frame control, fixed camera video, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Seedance 1.5 Pro integration questions to APIDot documentation and plan async text-to-video or image-to-video workflows with polling, webhooks, frame guidance, and API-key handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY only in server-side environment variables or a backend secret manager, and avoid logging private prompts, media URLs, callback URLs, generated video URLs, or credentials.

Risk: The skill may lead an agent to make live APIDot API calls or help write integration code that has external side effects.

Mitigation: Require explicit user approval and a safe server-side environment before any live API call; use documentation and examples for planning until approval is given.

Risk: Model-specific request fields, availability, limits, or commercial terms may change outside the skill artifact.

Mitigation: Use the current APIDot Seedance 1.5 Pro docs and model page as the source of truth before preparing copyable payloads or production guidance.

## Reference(s):

- [APIDot documentation](https://apidot.ai/docs)
- [APIDot Seedance 1.5 Pro model page](https://apidot.ai/models/seedance-1-5-pro)
- [APIDot Seedance 1.5 Pro API docs](https://apidot.ai/docs/seedance-1-5-pro)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Seedance 1.5 Pro reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with optional code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; does not execute network calls or store credentials.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
