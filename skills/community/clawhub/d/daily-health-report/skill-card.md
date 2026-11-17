## Description:

Generates and publishes a daily Raspberry Pi system health report covering uptime, memory, swap, load, disk, and temperature metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welderjustin](https://clawhub.ai/user/welderjustin)

### License/Terms of Use:

MIT-0

## Use Case:

Raspberry Pi owners and operators use this skill to generate a consistent daily health snapshot for quick review, chat posting, journaling, or operational logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher depends on a hard-coded user-specific health_report.sh script that is not included in the artifact.

Mitigation: Package or verify the health-report script before installation, and review it before scheduling automated execution.

Risk: Report publishing and log storage may expose system health details if the destination or log directory is too broad.

Mitigation: Set an explicit approved publish destination and ensure the log directory is private.

## Reference(s):

- [Daily Health Report on ClawHub](https://clawhub.ai/welderjustin/skills/daily-health-report)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text report printed to stdout and saved as latest-health-report.txt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local health_report.sh script and a writable private log directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
