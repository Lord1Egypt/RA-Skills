## Description:

Deepsop Genvis 助手 enables agents to generate AI images and videos asynchronously through the AI Artist API from text prompts and optional reference media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuoai](https://clawhub.ai/user/kukuoai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create AI-generated images and short videos from prompts and optional reference media. It helps an agent clarify generation intent, choose supported models and parameters, submit tasks, poll for completion, and return generated media as links, Markdown, JSON status, or local downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference media, generated-media URLs, or notification payloads may contain sensitive information.

Mitigation: Review prompts and media before use, and only set FEISHU_WEBHOOK_URL to a trusted HTTPS Feishu endpoint controlled by the user.

Risk: Inherited or unintended webhook configuration could disclose generated-media details to the wrong destination.

Mitigation: Check the runtime environment before execution and avoid inherited FEISHU_WEBHOOK_URL values in shared shells or agents.

Risk: The optional download path can fetch generated-media URLs into shared or sensitive environments.

Mitigation: Use --download only in trusted workspaces and verify the output directory before storing generated media locally.

Risk: Unpinned Python dependencies can change behavior during setup.

Mitigation: Prefer pinned dependency versions when provisioning the Python environment for requests and python-dotenv.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kukuoai/skills/deepsop-genvis-ai)
- [AI Artist API Detailed Documentation](references/api.md)
- [Chat Integration Examples](references/chat-integration.md)
- [Feishu Image Sending Guide](references/feishu-integration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown links, URLs, one-line JSON status, shell commands, configuration guidance, and optional downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AI_ARTIST_TOKEN; can upload local reference media, poll asynchronous tasks to completion, and optionally send Feishu webhook notifications.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
