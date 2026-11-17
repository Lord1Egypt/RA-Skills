## Description:

CLI tool generator. Project scaffolding, command adding, argument parsing, help docs, config handling, publish checklist, interactive prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold command-line tools, add commands and argument parsers, generate help and configuration guidance, and prepare release checklists for Python, Node.js, Bash, and Go CLIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated code and shell snippets may be unsafe or unsuitable if copied into a project without review.

Mitigation: Inspect generated snippets and commands before running or committing them, especially when inputs come from an untrusted source.

Risk: One bundled script can create a local history file containing command arguments.

Mitigation: Avoid passing secrets or sensitive project data as command arguments, and review or clear the local cli-builder history file when needed.

## Reference(s):

- [Cli Builder on ClawHub](https://clawhub.ai/ckchzh/skills/cli-builder)
- [BytesAgain homepage](https://bytesagain.com)
- [BytesAgain feedback](https://bytesagain.com/feedback)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated snippets and commands should be reviewed before execution.]

## Skill Version(s):

2.3.5 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
