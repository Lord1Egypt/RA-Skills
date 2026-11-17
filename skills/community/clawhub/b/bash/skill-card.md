## Description:

Writes, debugs, and hardens Bash shell scripts for quoting, arrays, strict mode, traps, argument parsing, testing, portability, CI, cron, HTTP calls, and safe file or process handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, review, debug, harden, and port Bash scripts used in CI steps, deployment scripts, container entrypoints, cron jobs, one-liners, and operational glue code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or revised Bash commands can alter files, privileges, services, network endpoints, or deployment environments when copied into sensitive systems.

Mitigation: Review generated scripts before execution, run dry runs where practical, and pay special attention to sudo, rm/rm -rf, cron, systemd, launchd, remote pushes, and network downloads.

Risk: Shell scripts can expose secrets through argv, debug tracing, logs, temporary files, or process environments.

Mitigation: Keep secrets out of command arguments and logs, disable tracing around credential handling, use restrictive temporary files, and prefer short-lived credentials.

Risk: Bash and common Unix tools differ across Linux, macOS, WSL, and POSIX sh environments, which can make otherwise correct guidance fail on another target.

Mitigation: State the Bash version and target operating system, use portable fallbacks where required, and test on the intended runtime before deployment.

## Reference(s):

- [ClawHub Bash skill page](https://clawhub.ai/ivangdavila/skills/bash)
- [Clawic Bash skill page](https://clawic.com/skills/bash)
- [Bash skill definition](artifact/SKILL.md)
- [Security guide](artifact/security.md)
- [Portability guide](artifact/portability.md)
- [Testing guide](artifact/testing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Bash snippets, review findings, lint or test commands, portability notes, and configuration guidance.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
