## Description:

Cisco IOS-XE and NX-OS device health check and triage procedure for troubleshooting routers, switches, and Nexus platforms across CPU, memory, interface, routing, and environmental health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers and operations teams use this skill to collect read-only Cisco IOS-XE and NX-OS health signals, classify device risk, and prepare a prioritized findings report for troubleshooting, audits, incident response, post-change checks, and capacity planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release declares a read-only safety posture, but evidence.security reports potentially state-changing or service-disrupting NX-OS commands.

Mitigation: Use the skill only for diagnostic collection unless the workflow blocks or requires explicit human approval for switchto vdc, poweroff module, and no poweroff module.

Risk: Crash and core data collected during health triage may contain sensitive operational information.

Mitigation: Handle crashinfo, core files, and logs according to the organization's sensitive-data handling and change-control process.

## Reference(s):

- [Cisco IOS-XE / NX-OS CLI Reference](artifact/references/cli-reference.md)
- [Cisco IOS-XE / NX-OS Threshold Tables](artifact/references/threshold-tables.md)
- [ClawHub skill release](https://clawhub.ai/vahagn-madatyan/skills/cisco-device-health)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with Cisco show-command snippets, severity classifications, findings, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic workflow; any potentially disruptive device action requires separate human approval and change-control review]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
