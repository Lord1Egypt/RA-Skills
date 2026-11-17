## Description:

A developer toolkit skill for Git workflows, project scaffolding, CI/CD checks, testing, formatting, code review, technical debt tracking, dependency analysis, diffs, and refactoring guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g1776933879](https://clawhub.ai/user/g1776933879)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run local development workflows such as review checks, formatting, dependency inspection, debt tracking, and project scaffolding from a CLI-oriented toolkit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and CLI run broad, unpinned commands.

Mitigation: Use the skill only in trusted repositories, avoid running install.sh as root, and prefer pinned local tool dependencies.

Risk: Unsafe shell handling could execute unintended code in a crafted repository.

Mitigation: Do not run dev-tk review, fmt, or dep on untrusted code until the shell handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g1776933879/skills/dev-toolkit-pro)
- [Publisher profile](https://clawhub.ai/user/g1776933879)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, console text, shell command examples, and generated project or report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands may create project scaffolds, review output, dependency summaries, technical-debt entries, and documentation files under project directories.]

## Skill Version(s):

2.2.1 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
