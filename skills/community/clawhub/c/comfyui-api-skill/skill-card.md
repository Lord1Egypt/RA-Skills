## Description:

ComfyUI执行器 interacts with ComfyUI over HTTP APIs to submit and execute workflows, manage queues, upload files, probe capabilities, and summarize generated image, video, audio, and file outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chsengni](https://clawhub.ai/user/chsengni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI workflow operators use this skill to run ComfyUI image, video, audio, and other generation workflows, upload inputs, inspect server capabilities, and manage queue or memory state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path or filename handling could overwrite, read, or delete local files when interacting with a malicious server or bad argument.

Mitigation: Use only ComfyUI servers you control, patch filename and path validation before important workspaces, and review workflow show or delete targets before execution.

Risk: API keys may be exposed if sent over non-local HTTP endpoints or printed during use.

Mitigation: Prefer localhost or trusted HTTPS endpoints, avoid sending API keys over non-local HTTP, and stop printing API keys before using the skill on important workspaces.

Risk: Queue interrupt, history clearing, and delete actions can disrupt or remove work.

Mitigation: Require explicit confirmation before running delete, history, or interrupt actions.

## Reference(s):

- [ComfyUI API Specification](references/api-specification.md)
- [ComfyUI Workflow Format](references/workflow-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON workflow snippets, and concise execution summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task IDs, queue status, uploaded file paths, and downloaded output file paths when commands are run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
