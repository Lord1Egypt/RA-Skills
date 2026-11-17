## Description:

Invokes Claude Code through `claude -p` for single-prompt tasks inside a Git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to invoke Claude Code for one-off investigation, analysis, code review, or data-query tasks in a Git repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's default command uses `--dangerously-skip-permissions`, allowing unattended file, command, credential, and network access by Claude Code.

Mitigation: Remove `--dangerously-skip-permissions` unless that access has been explicitly accepted, and run the skill only in a trusted, disposable or well-scoped repository.

Risk: User-supplied prompt text or paths may lead to unsafe shell invocation.

Mitigation: Avoid untrusted prompt text or paths, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gold3bear/skills/claude-code-invoke)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the `claude` binary and a Git repository; examples are oriented toward Windows PowerShell.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
