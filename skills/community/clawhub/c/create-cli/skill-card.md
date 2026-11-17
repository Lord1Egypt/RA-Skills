## Description:

Design command-line interface parameters and UX, including arguments, flags, subcommands, help text, output formats, error messages, exit codes, prompts, configuration precedence, and safe dry-run behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design or refactor a CLI surface before implementation, producing a compact interface specification for human-friendly and scriptable command-line tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CLI specifications may include destructive workflows, secret handling, telemetry, or configuration behavior that would be risky if implemented without review.

Mitigation: Review resulting implementations for dry-run behavior, confirmations, force and no-input controls, secret-safe input paths, telemetry consent, and clear configuration precedence.

Risk: Generated CLI guidance may be incomplete or unsuitable for a specific runtime, platform, or user audience.

Mitigation: Validate the proposed command tree, output contract, error handling, and platform assumptions against the target users and implementation environment before release.

## Reference(s):

- [Command Line Interface Guidelines](references/cli-guidelines.md)
- [Full Command Line Interface Guidelines](https://clig.dev/)
- [CLI Guidelines GitHub Repository](https://github.com/cli-guidelines/cli-guidelines)
- [ClawHub Skill Page](https://clawhub.ai/steipete/skills/create-cli)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with CLI usage synopses, argument and flag tables, examples, exit codes, and configuration rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and specifications only; it does not execute commands or implement the CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
