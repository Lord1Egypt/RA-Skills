## Description:

Analyze errors, stack traces, and logs to diagnose root causes and suggest actionable fixes for Python, Node.js, Go, Bash, Docker, Kubernetes, Git, and database errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly interpret cryptic error messages, stack traces, and logs from common application, container, Kubernetes, Git, and database workflows. It helps identify likely causes and returns practical fix suggestions without leaving the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script uses a predictable temporary file under /tmp, which can overwrite user-writable files on shared systems.

Mitigation: Review before installing on shared machines or privileged accounts; the publisher should replace the fixed temporary path with in-memory data or a private temporary directory.

Risk: Debug logs and stack traces may contain sensitive values.

Mitigation: Avoid providing sensitive logs unless local processing is acceptable, and redact secrets before analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/debugger)
- [Publisher profile](https://clawhub.ai/user/loutai0307-prog)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with diagnostic findings and fix suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-provided error text or local log files and emits local-only analysis.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
