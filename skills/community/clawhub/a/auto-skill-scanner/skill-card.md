## Description:

Auto Skill Scanner scans installed OpenClaw skills for hardcoded credentials, shell-injection patterns, environment leaks, and network exfiltration, then reports findings to configured messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohmanymoneygomyhome-creator](https://clawhub.ai/user/ohmanymoneygomyhome-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to monitor installed skills for common security issues and receive periodic or on-demand audit reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because one invocation can create persistent daily OpenClaw cron jobs.

Mitigation: Review before installing, test in a controlled OpenClaw profile, and inspect or remove created cron jobs if persistence is not desired.

Risk: Reports may be sent to every channel and recipient discovered in OpenClaw session metadata.

Mitigation: Confirm configured messaging channels and recipients before activation, and use an isolated environment when broad report distribution is not acceptable.

## Reference(s):

- [Security Checks Reference](references/security-checks.md)
- [ClawHub Skill Page](https://clawhub.ai/ohmanymoneygomyhome-creator/skills/auto-skill-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style audit reports with issue counts, affected skills, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create daily OpenClaw cron jobs and send reports to discovered active channels after initial activation.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
