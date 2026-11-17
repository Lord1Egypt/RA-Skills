## Description:

Browse and curate Alibaba Cloud DataWorks Data Map metadata, including catalogs, databases, tables, columns, partitions, lineage, datasets, versions, and metadata collections, through Aliyun CLI read and non-destructive write workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and metadata stewards use this skill to inspect DataWorks metadata, trace lineage, manage dataset and collection records, and apply confirmed non-destructive metadata updates from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require broad Alibaba Cloud DataWorks metadata permissions, including non-destructive write actions.

Mitigation: Use a dedicated low-privilege Aliyun identity, prefer the documented read-only RAM policy unless writes are required, and narrow RAM resources or conditions to approved projects and workspaces wherever supported.

Risk: Confirmed write actions can change DataWorks business metadata, lineage relationships, datasets, versions, collections, or collection membership.

Mitigation: Require explicit user confirmation for each write, perform check-then-act reads before create or add operations, and verify state with follow-up list or get commands.

Risk: Destructive DataWorks operations could remove metadata resources or relationships if granted and invoked outside the skill's intended scope.

Mitigation: Do not grant Delete or Remove actions to the operator account for this skill; the artifact explicitly excludes deletion and removal commands and directs deletions to the DataWorks console.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-dataworks-metadata)
- [Aliyun CLI installation documentation](https://help.aliyun.com/document_detail/121541.html)
- [Entity ID Format Reference](references/entity-id-formats.md)
- [RAM Policies - DataWorks Metadata](references/ram-policies.md)
- [Related CLI Commands - DataWorks Metadata](references/related-commands.md)
- [Verification Method - DataWorks Metadata](references/verification-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied Alibaba Cloud region, resource identifiers, credentials, and explicit confirmation before write operations.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
