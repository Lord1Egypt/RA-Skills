## Description:

Agent Emacs gives agents a persistent Emacs daemon for stateful context, structural code editing, Magit workflows, and remote node management through TRAMP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pitze](https://clawhub.ai/user/pitze)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run AI coding agents inside a persistent Emacs daemon that keeps buffers, terminals, remote sessions, and project context available across turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Emacs daemon state can retain buffers, terminals, remote sessions, and memory files after a task ends.

Mitigation: Use the skill only where persistent agent state is intended, and define a cleanup process for daemon buffers, remote sessions, and memory files after each task.

Risk: TRAMP and shell-command workflows can give agents broad persistent authority over remote systems.

Mitigation: Restrict use to approved hosts and accounts, scope SSH credentials and remote permissions tightly, and review remote commands before execution in sensitive environments.

Risk: The bootstrap script starts an Emacs daemon and may copy an init file into the user's Emacs configuration.

Mitigation: Run scripts/bootstrap.sh only from trusted artifact directories and verify the Emacs init file source before installation.

## Reference(s):

- [Usage Guide: Emacs-Agent Interaction](references/usage.md)
- [Advanced Agent Workflows in Emacs](references/agent-workflows.md)
- [ClawHub Skill Page](https://clawhub.ai/pitze/skills/agent-emacs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Emacs Lisp examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that start or interact with a persistent Emacs daemon, local buffers, TRAMP remote sessions, Magit, and REPL workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
