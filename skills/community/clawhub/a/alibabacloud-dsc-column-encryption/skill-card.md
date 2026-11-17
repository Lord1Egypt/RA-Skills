## Description:

Helps users find sensitive database columns and manage column encryption and plaintext access in Alibaba Cloud Data Security Center.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Database security operators use this skill to find columns, plan encryption changes, and manage database-account plaintext access, algorithms, keys, asset synchronization, or kernel upgrades through Alibaba Cloud DSC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud write actions can change column encryption or database-account plaintext access.

Mitigation: Start with query-only RAM permissions, grant change permissions only to approved operators, and approve each exact preflight plan before a write.

Risk: A cloud credential profile with broad or long-lived access increases the impact of mistakes.

Mitigation: Use a named Alibaba Cloud CLI profile and prefer OAuth or temporary credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-dsc-column-encryption)
- [Column encryption API contract](artifact/references/api-contract.md)
- [Query guide](artifact/references/query-guide.md)
- [Write guide](artifact/references/write-guide.md)
- [RAM policies](artifact/references/ram-policies.md)
- [Runtime constraints](artifact/references/runtime-constraints.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance and commands; JSON plans and query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require a reviewed preflight plan and explicit approval.]

## Skill Version(s):

0.0.1-beta.1 (source: release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
