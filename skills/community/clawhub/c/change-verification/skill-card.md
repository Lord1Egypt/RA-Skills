## Description: <br>
Pre/post change verification with baseline capture, diff analysis, and rollback decision guidance across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS, structured around a single change event lifecycle with impact classification and rollback criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and operations teams use this skill during planned or emergency network changes to capture baselines, compare post-change state, classify deviations, and decide whether to accept or roll back the change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and rollback guidance can modify production network device state. <br>
Mitigation: Require change-ticket authorization and human approval before any write or rollback command, and restrict SSH or MCP access to devices in the approved change scope. <br>
Risk: Saved configuration baselines can contain sensitive topology, configuration, and access details. <br>
Mitigation: Store baselines only in approved protected locations with access controls appropriate for network configuration data. <br>
Risk: Incorrect post-change interpretation could lead to accepting a harmful change or rolling back unnecessarily. <br>
Mitigation: Use the documented success and rollback criteria, compare against the approved change plan, and escalate unexpected critical deviations before continuing. <br>


## Reference(s): <br>
- [Change Verification Checklist Templates](references/checklist-templates.md) <br>
- [Change Verification CLI Reference](references/cli-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/change-verification) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with vendor-labeled CLI command blocks, checklists, threshold tables, decision trees, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-reviewed operational guidance for a single network change event; write and rollback commands require explicit authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
