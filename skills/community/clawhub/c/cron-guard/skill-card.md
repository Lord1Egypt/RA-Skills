## Description:

定时守护 helps agents create and harden cron jobs and background tasks with script-first structure, explicit runtime environment setup, quiet success behavior, cross-platform POSIX and PowerShell patterns, and pre-release reliability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to draft, review, and harden cron jobs, scheduled scripts, and unattended background tasks. It focuses on shell quoting failures, cwd and PATH drift, environment variable checks, quiet success output, cleanup traps, file locks, and safe git-push recovery patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests read, write, and exec authority while providing cron and command-execution guidance.

Mitigation: Require explicit approval before state-changing commands and keep generated cron jobs scoped to known files and commands.

Risk: The security summary flags API key, credential, network, and execution guidance as broader than the stated cron reliability purpose.

Mitigation: Do not provide API keys unless a specific guarded script truly needs them, and prefer documented environment variables over embedded credentials.

Risk: Generated cron jobs or background scripts can run unattended and repeatedly.

Mitigation: Review proposed scripts and cron entries before installation, including PATH, cwd, cleanup, locking, and failure-notification behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cron-guard)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and bash, PowerShell, and cron code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose cron entries, script templates, environment checks, locking patterns, and reliability review checklists.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
