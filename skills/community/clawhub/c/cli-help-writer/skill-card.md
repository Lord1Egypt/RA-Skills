## Description:

Generates standard terminal-style help text and man-page summaries for command line tools from raw commands, flags, arguments, and descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunny0826](https://clawhub.ai/user/sunny0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to turn rough CLI option lists into polished help output with usage, description, commands, options, and examples. It supports English and Chinese output based on the user's prompt language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples could expose credentials if user-provided secrets are repeated verbatim.

Mitigation: Redact real API keys, passwords, tokens, and similar credentials before including them in generated help text.

Risk: Inferred flags, defaults, or examples may not match the actual CLI implementation.

Mitigation: Review generated help text before copying it into a project, especially inferred defaults and example commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunny0826/skills/cli-help-writer)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text terminal-style help output inside a markdown text code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include inferred flags, defaults, subcommands, and examples when the user provides incomplete CLI details.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
