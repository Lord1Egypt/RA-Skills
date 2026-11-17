## Description:

Harden an agent's command interception layer safely: snapshot the baseline, test a matrix of should-block, negative-control, and known-bypass cases, verify classification rather than executing destructive commands, and document the bypass surface. Use when adding or changing guards around rm, mv, chmod, sudo, launchctl, dd, or any command wrapper. Tool-agnostic; includes a matrix runner and a bypass scanner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cengcengcai-creator](https://clawhub.ai/user/cengcengcai-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when adding or changing command guards. It guides them through recording a baseline, testing allow and deny classifications without executing the test commands, and documenting remaining bypass paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security record reports command arguments logged without a warning about sensitive data, and the shell scope is unclear.

Mitigation: Review where command arguments are logged and avoid passing sensitive values; define which shells and invocation paths are covered before relying on the guard.

Risk: The security scan was partial: it covered 8 of 9 components, and its tool-misuse analysis was degraded, so the evidence is incomplete.

Mitigation: Review the uncovered component and repeat the security assessment with complete component coverage before installation.

Risk: The documented PATH wrapper can be bypassed by absolute paths, nested interpreters, and direct syscalls, and does not provide a security boundary.

Mitigation: Treat the wrapper as classification and logging guidance; use operating-system permissions or sandboxing where enforcement is required, and document the residual bypass surface.

## Reference(s):

- [Bypass surfaces](references/bypass-surfaces.md)
- [ClawHub skill page](https://clawhub.ai/cengcengcai-creator/skills/agent-command-guard-hardening)
- [Publisher profile](https://clawhub.ai/user/cengcengcai-creator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON test matrices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a classifier test matrix and read-only bypass scan examples; test cases are classified rather than executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
