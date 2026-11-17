## Description:

智能体安全管家 performs OpenClaw and TeleClaw security patrols with local offline checks, optional consent-based threat-intelligence upload to Changeway endpoints, and optional OpenClaw cron scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smbbws2](https://clawhub.ai/user/smbbws2)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw and TeleClaw users and administrators use this skill to run security audits, inspect local agent and system posture, and optionally request a threat-intelligence score after explicit consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit reads broad local system, workspace, SSH/GPG, process, and agent-memory metadata and writes persistent files under ~/.openclaw.

Mitigation: Review the skill before installing, avoid running it as root, and remove reports or baselines under ~/.openclaw when persistence is not desired.

Risk: --push mode sends device and skill-inventory data to Changeway-operated endpoints.

Mitigation: Use local mode by default and enable --push only after explicit consent and when the user trusts Changeway with that data.

Risk: Scheduled scans can leave ongoing OpenClaw cron jobs and local persistence.

Mitigation: Configure scheduled scans without --push and remove unwanted openclaw cron jobs if ongoing scanning is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smbbws2/skills/ct-security-patrol)
- [Cron setup guide](references/cron-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local text/JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces summarized scan results for the user while detailed audit reports and baselines are stored under ~/.openclaw.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
