## Description:

Code formatting best practices and quick references for Python, JavaScript, JSON, Markdown, and common languages with Prettier, Black, ESLint, and other formatters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and run common formatting, linting, editor, and pre-commit commands for Python, JavaScript, TypeScript, JSON, Markdown, shell, Go, and Rust projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formatter and linter commands can modify many files when run with write or fix options.

Mitigation: Review commands before execution, prefer project-pinned dependencies and committed lockfiles, and run broad formatting changes in a controlled workspace.

Risk: Installing unpinned formatter packages can introduce dependency drift across environments.

Mitigation: Use project package scripts, pinned dependency versions, and existing repository configuration where available.

## Reference(s):

- [Code Formatter ClawHub Release](https://clawhub.ai/terrycarter1985/skills/code-formatter)
- [Black Formatter](https://github.com/psf/black)
- [isort](https://github.com/pycqa/isort)
- [Prettier Pre-commit Mirror](https://github.com/pre-commit/mirrors-prettier)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include formatter, linter, editor, and pre-commit configuration examples.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
