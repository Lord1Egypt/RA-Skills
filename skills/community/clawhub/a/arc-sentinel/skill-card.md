## Description:

Security monitoring and infrastructure health checks for OpenClaw agents covering breach monitoring, SSL certificate expiry checks, GitHub security audits, credential rotation tracking, secret scanning, git hygiene, token watchdog checks, and permission audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to run security and infrastructure health checks for OpenClaw environments, including SSL expiry monitoring, credential rotation review, repository hygiene, permission audits, and secret scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some scripts inspect local credential metadata and selected credential files under the user's home directory.

Mitigation: Review the scripts and configuration before installation, then run only the individual checks needed for the intended scope.

Risk: The JSON mode in secret-scanner.sh can print matched secret values into logs.

Mitigation: Avoid secret-scanner.sh --format=json until matches are masked or removed, and treat generated reports and logs as sensitive.

Risk: Running the full audit can scan broader local state than needed for a single repository review.

Mitigation: Prefer individual scripts for targeted audits and limit scan directories to the repositories or files intended for review.

## Reference(s):

- [Arc Sentinel ClawHub skill page](https://clawhub.ai/arc-claw-bot/skills/arc-sentinel)
- [arc-claw-bot ClawHub publisher profile](https://clawhub.ai/user/arc-claw-bot)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Terminal text output and JSON reports, with Markdown guidance for agent use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated JSON reports and uses exit codes 0, 1, and 2 to indicate clear, warning, and critical results.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
