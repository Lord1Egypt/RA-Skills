## Description:

Execute long-running tasks autonomously using Claude Code headless sessions or hook-based loops with structured task decomposition and lightweight iterative modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiskyer](https://clawhub.ai/user/feiskyer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run sustained Claude Code work across multiple sessions, including complex project builds, test-driven fixes, refactoring, and batch iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended child agents may continue work with broad authority and persistent loop behavior.

Mitigation: Run only in isolated workspaces, set explicit max session or iteration limits, and avoid bypassPermissions unless unattended broad access is intentional.

Risk: The skill writes local task logs, transcripts, and hook state.

Mitigation: Review and clean .autonomous and .claude state files after use, especially before sharing a workspace.

Risk: Autonomous execution on untrusted prompts or repositories can amplify unsafe or unwanted changes.

Mitigation: Review the skill before installing and use sandboxing for untrusted repositories or task prompts.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, generated task/progress files, session logs, and hook configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local task state under .autonomous and hook state under .claude when used.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
