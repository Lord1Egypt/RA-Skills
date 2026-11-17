## Description:

Trae Agent helps repository-level code agents analyze large codebases, combine keyword, semantic, and structural search strategies, plan multi-file edits, and validate code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to understand repositories, find relevant code across large codebases, plan safe edit sequences, and report validation results for create, fix, refactor, test, understand, and modify tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes broad repository editing and command-execution workflows without clear built-in user-control boundaries.

Mitigation: Use it only in trusted repositories, require explicit approval before edits or shell commands, and run validation in a sandbox without secrets.

Risk: Generated edit plans or validation commands could be incorrect or unsafe for a target repository.

Mitigation: Review proposed code changes and commands before applying them, and rely on project-specific tests, linting, and type checks before deployment.

## Reference(s):

- [Trae Agent Code Examples](artifact/references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/skills/ah-trae-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with structured summaries, search results, edit plans, execution logs, validation results, and status metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed code edits and validation commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
