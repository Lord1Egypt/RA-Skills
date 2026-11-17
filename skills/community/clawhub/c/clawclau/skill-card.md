## Description:

Asynchronous Claude Code task scheduling toolkit based on tmux, with background dispatch, progress reporting, completion notifications, status checks, result retrieval, task termination, and mid-task steering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barryyjj](https://clawhub.ai/user/barryyjj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to dispatch Claude Code work into isolated tmux sessions, monitor long-running tasks, collect results, stop jobs, and steer interactive runs from a controlling agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spawned Claude Code tasks may run unattended with high execution authority and bypass interactive permission prompts.

Mitigation: Use only in trusted workspaces, review prompts before dispatch, and reserve it for environments where unattended Claude Code execution is acceptable.

Risk: Untrusted repositories, prompt content, model names, or paths can influence background task execution.

Mitigation: Avoid untrusted repositories and prompt content, validate model names and work directories, and keep CC_HOME pointed at a normal trusted directory.

Risk: Prompts, logs, result snippets, and notifications may persist locally or be sent to Feishu when notifications are configured.

Mitigation: Treat task content as persistent operational data, avoid sensitive prompts unless retention is acceptable, and configure notification targets carefully.

## Reference(s):

- [ClawClau schema and task state reference](references/schema.md)
- [ClawClau design principles and runtime modes](references/design.md)
- [ClawHub skill page](https://clawhub.ai/barryyjj/skills/clawclau)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, Markdown, Guidance]

**Output Format:** [Terminal text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local task registry entries, prompt backups, wrapper scripts, and log files under CC_HOME.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
