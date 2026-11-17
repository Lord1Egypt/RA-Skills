## Description:

Foreman dispatches coding tasks to background agents in separate Git worktrees and accepts delivered commits through scoped verification gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use foreman to delegate repository implementation work to configured coding agents and review committed changes against task-specific acceptance checks before merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dispatching tasks sends repository content to configured background agent backends.

Mitigation: Use only approved backends and avoid dispatching sensitive repositories without appropriate network controls.

Risk: Backend probes and the optional container worker can use an API key.

Mitigation: Use a dedicated low-limit key, avoid global shell exports, and apply network allowlisting to the container for sensitive work.

Risk: Custom backend probe commands run with shell access, and task state may contain repository details.

Mitigation: Review custom probe commands before enabling them and keep .foreman gitignored.

## Reference(s):

- [foreman on ClawHub](https://clawhub.ai/xiaoba-dev/skills/foreman)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with shell commands and verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task work orders, committed changes, and acceptance reports]

## Skill Version(s):

2.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
