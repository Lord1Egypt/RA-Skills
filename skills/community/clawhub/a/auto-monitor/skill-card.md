## Description: <br>
Proactively monitors system status, periodically checks server health, and reports without waiting for a user request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and system operators use this skill to have an agent periodically check disk, memory, CPU, network, and process health, then generate health reports and abnormal-condition alerts. The release also describes immediate remediation for fixable problems, so deployments should constrain that authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent recurring system-monitoring authority. <br>
Mitigation: Use read-only monitoring by default and define the exact hosts, checks, thresholds, and interval before enabling it. <br>
Risk: The artifact describes immediate repair for fixable problems, which could include disruptive system actions. <br>
Mitigation: Require explicit confirmation before any restart, deletion, configuration change, process kill, or other repair action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/auto-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text health reports, alerts, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports cover disk, memory, CPU load, network status, and process status, with documented alert thresholds for disk, memory, and CPU load.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
