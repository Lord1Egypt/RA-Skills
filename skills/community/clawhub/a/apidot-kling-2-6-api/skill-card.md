## Description:

Use APIDot for Kling 2.6 API workflows, including text-to-video API, image-to-video API, native audio video generation, prompt-driven clips, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find APIDot Kling 2.6 documentation and plan text-to-video, image-to-video, native-audio, polling, and webhook workflows. It provides documentation routing and integration guidance without executable behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIDOT_API_KEY or private media details could be exposed if copied into frontend code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep API keys in server-side environment variables or a backend secret manager, avoid logging private prompts, media URLs, generated video URLs, callback URLs, and API keys, and verify current APIDot docs before live calls.

Risk: Model-specific request fields, availability, limits, or terms may change outside this documentation-only skill.

Mitigation: Use the live APIDot docs and model pages as the source of truth before preparing payloads or making production requests.

## Reference(s):

- [APIDot documentation](https://apidot.ai/docs)
- [APIDot Kling 2.6 model page](https://apidot.ai/models/kling-2-6)
- [APIDot Kling 2.6 API docs](https://apidot.ai/docs/kling-2-6)
- [APIDot quickstart](https://apidot.ai/docs/quickstart)
- [APIDot webhooks](https://apidot.ai/docs/webhooks)
- [APIDot examples](https://github.com/APIDotAI/apidot-examples)
- [APIDot Kling 2.6 Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with links and code-oriented integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no bundled executable files, network calls, or stored credentials.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
