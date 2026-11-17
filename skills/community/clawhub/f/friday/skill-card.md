## Description:

星期五 is a Chinese-language programming-agent skill for using the opencode CLI to write, review, refactor, test, and debug code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easeclick](https://clawhub.ai/user/easeclick)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run opencode-based coding workflows for feature implementation, code review, refactoring, debugging, testing, and technical documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide opencode workflows that modify project files.

Mitigation: Run it only in trusted project directories and use read-only or interactive mode for unfamiliar repositories.

Risk: Automatic code changes may be incorrect, unsafe, or misaligned with project requirements.

Mitigation: Review generated diffs, run tests and linters, and inspect critical changes before committing or deploying.

Risk: Prompts or project context may expose sensitive information to the configured coding agent or model provider.

Mitigation: Avoid including secrets, passwords, API keys, or other sensitive data in prompts or shared context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/easeclick/skills/friday)
- [Skill source](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, code-oriented recommendations, and review findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include changed-file lists, change summaries, decision notes, risk notes, issue severity, fix suggestions, and code examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
