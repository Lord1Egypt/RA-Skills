## Description: <br>
Cisco IOS-XE device health check and triage procedure for troubleshooting routers and switches, interpreting CPU, memory, interface, routing, and platform signals, and producing a structured handoff report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and operations teams use this skill to collect read-only IOS-XE health signals, classify device condition, and prepare a prioritized findings report during outages, audits, post-change checks, and incident response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized inspection of Cisco IOS-XE devices could expose operational details. <br>
Mitigation: Use the skill only when authorized to inspect the target devices. <br>
Risk: Recommended remediation actions such as reloads, filtering changes, QoS changes, or hardware replacement can affect production networks. <br>
Mitigation: Treat remediation items as recommendations that require normal change control and explicit approval. <br>


## Reference(s): <br>
- [IOS-XE Device Health CLI Reference](references/cli-reference.md) <br>
- [Device Health Threshold Tables](references/threshold-tables.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with IOS-XE CLI command blocks and a structured device health report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only triage guidance; no executable code or hidden data flow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
