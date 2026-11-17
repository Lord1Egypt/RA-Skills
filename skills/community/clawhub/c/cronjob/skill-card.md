## Description:

Manage cron jobs with execution logging and failure alert tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to record local notes about cron-related scans, monitoring observations, alerts, fixes, backups, and exports. It should be treated as a note logger, not as a tool that inspects or changes real cron jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented as cron management and monitoring but the security summary says it behaves as a local note logger.

Mitigation: Do not rely on it to inspect, add, monitor, fix, back up, or restore actual cron jobs; verify real cron state with trusted system tools.

Risk: The skill stores recorded entries locally in plaintext and can export them to CSV, JSON, or TXT.

Mitigation: Avoid recording secrets, credentials, sensitive paths, incident details, or other information that should not be stored or exported in plaintext.

## Reference(s):

- [Cronjob on ClawHub](https://clawhub.ai/xueyetianya/skills/cronjob)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local plaintext logs and JSON, CSV, or TXT exports under the configured cronjob data directory.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
