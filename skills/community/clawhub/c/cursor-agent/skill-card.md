## Description:

A comprehensive skill for using the Cursor CLI agent for various software engineering tasks, including 2026 features and tmux automation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftlysingh](https://clawhub.ai/user/swiftlysingh)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate Cursor CLI from the terminal for software engineering workflows, including installation, authentication, model and session management, code review, refactoring, debugging, and CI-style automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands may execute unverified remote code when using curl piped directly to a shell.

Mitigation: Prefer a package-managed or verified Cursor CLI installer and review installation scripts before execution.

Risk: Workspace trust automation and force mode can bypass human review or apply changes in an unreviewed repository.

Mitigation: Use controlled branches or sandboxes, avoid force mode unless rollback is available, and review resulting changes before merging or deploying.

Risk: Automated Cursor CLI runs can hang when launched without a real terminal.

Mitigation: Run automated invocations through a managed TTY such as tmux, monitor execution with timeouts, and capture output for review.

## Reference(s):

- [Cursor CLI Agent on ClawHub](https://clawhub.ai/swiftlysingh/skills/cursor-agent)
- [Cursor CLI Installer](https://cursor.com/install)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Cursor CLI examples for text, JSON, and streaming JSON modes; the skill itself emits guidance rather than a structured API response.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
