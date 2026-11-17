## Description:

Policy-based monitoring and command-line enforcement for high-risk agent operations that intercepts sensitive commands and logs them for human auditing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balkanblbn](https://clawhub.ai/user/balkanblbn)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to monitor high-risk agent terminal operations, require pause-and-ask review, and preserve an audit trail for forensic review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command audit logs can expose sensitive paths, usernames, and secrets embedded in terminal commands.

Mitigation: Before deployment, confirm where .logs/SECURITY.json is stored, restrict read access to authorized reviewers, and avoid entering secrets directly in shell commands.

Risk: Pause-on-risk enforcement can interrupt legitimate administrative or incident-response commands.

Mitigation: Review and maintain the local allowlist so expected high-privilege workflows are routed to the right human approval path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/balkanblbn/skills/audit-log-firewall)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe command interception decisions and audit log records for human review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
