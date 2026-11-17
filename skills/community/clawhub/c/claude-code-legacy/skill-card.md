## Description:

Trigger Claude Code development tasks in observable tmux sessions with stable startup, progress visibility, and completion callback to OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaxuan42](https://clawhub.ai/user/yaxuan42)

### License/Terms of Use:


## Use Case:

Developers use this skill to start, monitor, summarize, and complete long-running Claude Code coding tasks in observable tmux sessions, including local or SSH-targeted workflows and completion reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start autonomous Claude Code sessions with normal permission prompts disabled.

Mitigation: Run it only in a sandbox, VM, container, or dedicated low-privilege account, and review the launch mode before use on sensitive repositories.

Risk: Task text, work paths, prompt files, SSH/SCP operations, and temporary report files may affect repositories or expose sensitive workflow data if misused.

Mitigation: Use trusted task inputs and paths, review SSH/SCP behavior, and validate or relocate /tmp report handling before production use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/yaxuan42/skills/claude-code-legacy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, JSON task summaries, and completion reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit tmux session names, attach commands, status lines, task JSON arrays, and report file paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
