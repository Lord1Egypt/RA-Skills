## Description:

Cisco IOS-XE device health check and triage procedure for troubleshooting routers or switches, checking CPU utilization, memory usage, interface errors, routing health, and producing structured handoff reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers and operations teams use this skill to collect read-only Cisco IOS-XE diagnostic commands, interpret device health thresholds, and produce a prioritized triage report during outages, audits, post-change checks, or incident response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may connect to network devices and summarize operational details.

Mitigation: Use the skill only with authorized Cisco IOS-XE devices and handle generated reports according to operational data handling rules.

Risk: Suggested remediation may include disruptive operational actions such as reload planning, hardware replacement, or QoS and ACL changes.

Mitigation: Have a qualified operator review recommendations and perform any changes manually through normal change-control procedures.

## Reference(s):

- [IOS-XE Device Health CLI Reference](references/cli-reference.md)
- [Device Health Threshold Tables](references/threshold-tables.md)
- [ClawHub skill page](https://clawhub.ai/vahagn-madatyan/skills/example-device-health)
- [ClawHub publisher profile](https://clawhub.ai/user/vahagn-madatyan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with Cisco IOS-XE show commands, findings, severity labels, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic workflow; requires authorized SSH or console access to the target Cisco IOS-XE device.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
