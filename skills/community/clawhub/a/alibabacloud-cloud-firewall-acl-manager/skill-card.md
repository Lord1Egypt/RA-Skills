## Description:

Manages Alibaba Cloud Cloud Firewall ACL policy backup, restore, export, analysis, and single-policy add or enable/disable operations across Internet, NAT, and VPC boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud firewall operators and security engineers use this skill to back up, restore, inspect, and make narrowly scoped changes to Alibaba Cloud Cloud Firewall ACL policies and supporting address book or sync-node configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated logs and Excel backup files can contain sensitive firewall policy and address book details.

Mitigation: Protect backup workbooks and command output as sensitive security configuration and avoid broad log exposure.

Risk: Restore and single-policy change operations can modify live Alibaba Cloud Cloud Firewall ACLs.

Mitigation: Install only for operators who intentionally manage Cloud Firewall ACLs and use the documented dedicated RAM user or role permissions instead of broad access where feasible.

Risk: Restoring policies in the wrong scenario or order can duplicate ACLs, alter policy ordering, or fail because dependencies are missing.

Mitigation: Follow the documented restore order, use differential restore for same-resource recovery, and require explicit target gateways or policy groups for NAT and VPC restores.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-cloud-firewall-acl-manager)
- [Required RAM Permissions](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and generated backup or restore files from the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Excel backup workbooks and command output containing firewall policy details; treat those outputs as sensitive security configuration.]

## Skill Version(s):

0.0.1 (source: server release evidence and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
