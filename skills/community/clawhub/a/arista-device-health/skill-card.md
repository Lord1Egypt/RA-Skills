## Description: <br>
Arista EOS device health check and triage procedure for assessing CPU, memory, interfaces, environment, agent health, MLAG state, and VXLAN/EVPN health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and operators use this skill to troubleshoot or audit Arista EOS switches, classify device health findings by severity, and produce a prioritized remediation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is labeled read-only but includes an agent restart procedure that changes switch configuration state. <br>
Mitigation: Keep normal use to show commands and diagnostics; run any agent restart only after explicit approval from a qualified operator who understands the affected subsystem. <br>


## Reference(s): <br>
- [Arista EOS CLI Reference](references/cli-reference.md) <br>
- [Arista EOS Threshold Tables](references/threshold-tables.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline EOS and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces severity-classified findings, recommended actions, and a next-check interval.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
