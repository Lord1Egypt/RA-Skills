## Description:

Use APIDot as one AI API for image generation API, video generation API, chat API, music generation API, and 3D generation API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao71727](https://clawhub.ai/user/jiehao71727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external builders use this skill to integrate APIDot workflows for image, video, chat, music, and 3D generation while following APIDot documentation for model fields, async task handling, polling, webhooks, and API-key safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real APIDot API workflows require an API key.

Mitigation: Store APIDOT_API_KEY only in server-side environment variables or a backend secret manager, and never expose it in browser code, public repositories, logs, screenshots, or chat output.

Risk: Model fields, availability, and pricing can change outside the skill artifact.

Mitigation: Verify current request fields, model availability, and pricing in APIDot's live documentation and model pages before using or adapting examples.

Risk: Generated media tasks use asynchronous polling or webhooks and can be mishandled if task IDs or callbacks are not persisted safely.

Mitigation: Persist returned task IDs immediately, make webhook handling idempotent, and retry only transient failures with backoff.

## Reference(s):

- [APIDot API Docs](https://apidot.ai/docs)
- [APIDot Models](https://apidot.ai/models)
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples)
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-ai-api)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with links, code snippets, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to current APIDot docs and official examples for request fields; no executable files are bundled.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
