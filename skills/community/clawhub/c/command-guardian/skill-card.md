## Description:

Preflight safety guard for shell and infrastructure commands. Use before running commands that delete, overwrite, move, deploy, rewrite git history, change permissions, use shell wrappers like bash -c or powershell -Command, chain multiple commands with &&/||/; or may expose inline secrets. Especially for shell, git, docker, kubectl, terraform, npm, curl, wget, rsync, chmod, chown, and PowerShell file operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before running shell, git, Docker, Kubernetes, Terraform, package-manager, file-operation, or PowerShell commands with possible side effects. It helps classify command risk, identify broad targets or inline secrets, suggest safer rewrites, and provide rollback guidance before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports can echo the reviewed command, which may expose inline credentials in logs or shared transcripts.

Mitigation: Avoid passing live secrets via --command, keep command files or stdin transcripts controlled, and redact credentials before sharing output.

Risk: Path-escape findings are advisory and may not fully protect against symlink or filesystem edge cases.

Mitigation: Manually verify resolved targets, symlinks, and allowed roots before executing destructive file operations.

Risk: The skill is a local preflight checker, not a hard security boundary for command execution.

Mitigation: Require human confirmation for high or critical reports and prefer dry runs, backups, or staged safer commands before proceeding.

## Reference(s):

- [Risk Rules](references/risk-rules.md)
- [Tool Patterns](references/tool-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style risk review with labeled sections; helper scripts can emit JSON or text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk level, reasons, safer command suggestions, rollback guidance, and approval recommendation.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
