## Description: <br>
BGP protocol analysis with peer state diagnosis, path selection verification, route filtering validation, and convergence assessment across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and operations teams use this skill to investigate BGP peer state, route propagation, path selection, filtering, and convergence issues using read-only diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Router diagnostic access can expose sensitive network topology, routing policy, and peer state. <br>
Mitigation: Use least-privilege read-only network accounts and limit access to the devices being investigated. <br>
Risk: BGP findings may be incomplete if expected topology, policy intent, or baseline prefix counts are missing. <br>
Mitigation: Validate findings against known topology and routing policy before taking operational action. <br>
Risk: Suggested routing or policy changes could disrupt production traffic if applied without review. <br>
Mitigation: Treat recommendations as proposals and have qualified operators review and apply changes manually. <br>


## Reference(s): <br>
- [BGP CLI Reference - Cisco / JunOS / EOS](references/cli-reference.md) <br>
- [BGP Finite State Machine (FSM)](references/state-machine.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/bgp-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with read-only network diagnostic commands and structured findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces diagnostic reasoning and recommendations; any operational changes should be reviewed and applied manually.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
