## Description:

Amplifier delegates complex research, coding, architecture, and review tasks to a multi-agent framework through the amplifier-openclaw CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkrabach](https://clawhub.ai/user/bkrabach)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to delegate substantial research, comparison, coding, refactoring, debugging, and architecture review tasks that benefit from parallel specialist agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates prompts and possibly project context to an external multi-agent CLI.

Mitigation: Use only with repositories and prompts appropriate for that tool, and verify its data handling and session deletion behavior before using sensitive material.

Risk: The install path uses a remote executable package from source metadata.

Mitigation: Prefer an install pinned to a reviewed commit or verified release artifact before deployment.

Risk: Persistent Amplifier sessions may retain task context across runs.

Mitigation: Use named sessions deliberately and clean up sessions containing sensitive or project-specific context.

## Reference(s):

- [Amplifier ClawHub skill page](https://clawhub.ai/bkrabach/skills/amplifier-openclaw)
- [Amplifier OpenClaw install package](https://github.com/microsoft/amplifier-app-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON results from the Amplifier CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated runs may include response text, usage data, estimated cost, tool invocation counts, and completion status.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
