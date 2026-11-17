## Description:

Execute commands with real-time console output while logging all stdin, stdout, and stderr to a customizable log file for monitoring and debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run commands while preserving a complete stdin, stdout, and stderr log for debugging, build monitoring, CI/CD tracing, and later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command I/O logs may include passwords, tokens, private keys, or other sensitive input.

Mitigation: Use only when full logging is intentional; avoid sensitive interactive sessions and choose log paths and retention policies appropriate for the data.

Risk: High-volume commands can produce large log files.

Mitigation: Confirm sufficient disk space and select a log location suitable for large outputs before long-running commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and log-file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose command invocations that record full command I/O to disk.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
