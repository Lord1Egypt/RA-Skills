## Description: <br>
Cisco IOS-XE and NX-OS device health check and triage procedure for troubleshooting Cisco routers, switches, or Nexus platforms by assessing CPU, memory, interfaces, routing, and environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers, operators, and incident responders use this skill to run structured Cisco IOS-XE and NX-OS health checks, classify findings by severity, and produce prioritized remediation guidance for audits, post-change verification, troubleshooting, and capacity planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users could treat report-only remediation notes as automatic operational changes. <br>
Mitigation: Use read-only credentials where possible and require explicit maintenance approval before reloads, ACL or CoPP changes, VDC context switches, module shutdowns, or module power cycles. <br>
Risk: Health findings can be misleading if the operator checks the wrong platform context or lacks an accurate device baseline. <br>
Mitigation: Confirm the IOS-XE or NX-OS platform, NX-OS VDC context, and expected CPU, memory, route, and traffic baselines before acting on findings. <br>


## Reference(s): <br>
- [Cisco IOS-XE / NX-OS CLI Reference](artifact/references/cli-reference.md) <br>
- [Cisco IOS-XE / NX-OS Threshold Tables](artifact/references/threshold-tables.md) <br>
- [ClawHub Release Page](https://clawhub.ai/vahagn-madatyan/cisco-device-health) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with inline Cisco IOS-XE and NX-OS show commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces severity-classified findings, platform-specific notes, recommendations, and next-check timing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
