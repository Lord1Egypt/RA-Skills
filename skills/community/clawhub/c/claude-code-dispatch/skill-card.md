## Description:

Invoke Claude Code CLI as a subprocess for coding tasks that require file access, editing, and shell execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezpeasydave](https://clawhub.ai/user/ezpeasydave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to delegate local coding tasks to an authenticated Claude Code CLI when work requires file access, file editing, shell command execution, tests, code review, or multi-file debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegating local coding tasks can expose project data and local environment secrets to Claude Code.

Mitigation: Run the skill from an environment with only the credentials needed for the task, avoid passing secrets in prompts, and prefer read-only tool access for review work.

Risk: Broad filesystem or shell access can modify files or execute commands beyond the intended task.

Mitigation: Use the narrowest Claude Code tool preset that works and pre-authorize only the required tools in Claude Code settings.

Risk: Unpinned CLI dependencies can affect reproducibility across installs.

Mitigation: Pin or separately manage the Claude Code dependency when reproducible installs matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ezpeasydave/skills/claude-code-dispatch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text structured summary with status, model, cost, duration, and result fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results longer than 2000 characters are truncated at a line boundary.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
