## Description: <br>
EIGRP DUAL algorithm analysis for Cisco IOS-XE and NX-OS covering successor and feasible successor evaluation, stuck-in-active diagnosis, K-value validation, redistribution loop detection, and protocol-first reasoning for classic and named EIGRP modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and operations teams use this skill to troubleshoot Cisco EIGRP behavior, including missing or suboptimal routes, stuck-in-active events, neighbor issues, metric mismatches, and redistribution loops. It guides read-only evidence collection and produces diagnostic reasoning for IOS-XE and NX-OS environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collected Cisco routing and configuration outputs can expose sensitive network topology, device state, or operational details. <br>
Mitigation: Use read-only device credentials where possible and limit command output collection to the troubleshooting scope. <br>
Risk: Suggested EIGRP configuration changes could affect production routing if applied without review. <br>
Mitigation: Require explicit change-control approval and human network-engineer review before applying any configuration changes. <br>


## Reference(s): <br>
- [EIGRP CLI Reference - IOS-XE / NX-OS](references/cli-reference.md) <br>
- [EIGRP DUAL Finite State Machine](references/state-machine.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown diagnostic guidance with Cisco IOS-XE and NX-OS command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only troubleshooting workflow; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
