## Description:

Execute AI coding CLI tools (Claude Code / Gemini CLI / qodercli) on behalf of Workers when a Worker sends a coding-request message asking Manager to run coding operations in their workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montycn](https://clawhub.ai/user/montycn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let a Manager coordinate coding work by detecting available AI coding CLIs, configuring delegation, running Worker-provided prompts in a task workspace, and returning success or failure notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute Worker-provided prompts through AI coding CLIs with approval-bypass flags, which can modify workspace code without normal interactive review.

Mitigation: Install only in a contained task runner with trusted Workers, task-scoped CLI credentials, workspace-only filesystem access, restricted network access, and reviewed diffs before synchronization.

Risk: Prompts, CLI output, logs, and task data may contain sensitive repository or task information that is persisted or synchronized.

Mitigation: Define retention and redaction rules for prompts and logs, and avoid using the skill on sensitive repositories until the approval-bypass flags and prompt-saving pattern are fixed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline JSON and bash command examples, plus shell scripts that produce JSON status and CLI execution logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local configuration, prompt files, workspace files, task synchronization state, and coding CLI log files.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
