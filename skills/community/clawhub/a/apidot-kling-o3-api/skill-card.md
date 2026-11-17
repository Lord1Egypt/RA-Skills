## Description:

Use APIDot for Kling O3 API workflows, including Kling O3 Standard, Kling O3 Pro, Kling O3 4K, text-to-video API, image-to-video API, reference video generation, multi-shot video, Native Audio, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route Kling O3 integration questions to APIDot model pages, docs, async task guidance, polling, webhook notes, and safe credential handling practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDot API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid logging secrets, private prompts, private media URLs, generated video URLs, or callback URLs.

Risk: Live API calls or webhook setup could occur outside the user's intended workflow.

Mitigation: Treat the skill as documentation-only and allow live API calls or webhook setup only when explicitly requested in a safe server-side environment.

## Reference(s):

- [APIDot Kling O3 Reference](references/api.md)
- [APIDot Documentation](https://apidot.ai/docs)
- [APIDot Kling O3 Model Page](https://apidot.ai/models/kling-o3)
- [APIDot Kling O3 API Docs](https://apidot.ai/docs/kling-o3)
- [APIDot Quickstart](https://apidot.ai/docs/quickstart)
- [APIDot Webhooks](https://apidot.ai/docs/webhooks)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with API workflow notes and documentation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files or hidden automation; may reference APIDOT_API_KEY for server-side configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
