## Description:

Pre/post change verification with baseline capture, diff analysis, and rollback decision guidance across Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers and operations teams use this skill to plan and verify a single network change window, compare pre- and post-change state, classify deviations, and decide whether to accept or roll back the change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes commands that can change or roll back production network device configurations.

Mitigation: Use it only for authorized network operations with approved change tickets, scoped device lists, maintenance windows, and validated rollback plans.

Risk: Incorrect rollback or change-execution guidance could disrupt network services.

Mitigation: Review the proposed commands against the target vendor platform and confirm baseline captures, success criteria, escalation contacts, and rollback triggers before execution.

## Reference(s):

- [Change Verification skill page](https://clawhub.ai/vahagn-madatyan/skills/change-verification)
- [Change Verification Checklist Templates](references/checklist-templates.md)
- [Change Verification CLI Reference](references/cli-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with vendor-specific CLI command blocks, checklist tables, and rollback decision criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read/write safety labels for commands that archive, apply, or roll back device configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
