## Description:

BGP protocol analysis for peer state diagnosis, path selection verification, route filtering validation, and convergence assessment across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network engineers, and operations teams use this skill to investigate BGP peering, route propagation, path-selection, route-policy, convergence, and prefix-scale issues using read-only device output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Router access can expose operationally sensitive network configuration or authentication material if broad command output is pasted into the agent.

Mitigation: Use read-only accounts, collect only task-relevant output, and redact authentication keys, shared secrets, and unrelated sensitive configuration before analysis.

Risk: BGP diagnosis can be misleading when expected topology, baseline prefix counts, or intended policy outcomes are incomplete or stale.

Mitigation: Validate findings against the current network design, expected peer inventory, route-policy intent, and recent change records before taking action.

Risk: Suggested remediation could affect routing behavior if applied directly to production routers.

Mitigation: Treat recommendations as operator-reviewed guidance and apply changes only through established change-control and validation procedures.

## Reference(s):

- [BGP CLI Reference](references/cli-reference.md)
- [BGP Finite State Machine](references/state-machine.md)
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/skills/bgp-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline read-only vendor CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces protocol-focused diagnostic findings and recommendations for Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
