## Description:

Feishu permission management for documents and files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumuzhi4843-a](https://clawhub.ai/user/sumuzhi4843-a)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using Feishu documents and files can use this skill to have an agent list collaborators and add or remove access. It is suited for controlled permission administration on documents, sheets, folders, wiki nodes, and related Feishu assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change document and folder access, including granting full_access permissions.

Mitigation: Keep the tool disabled by default and require explicit user confirmation before adding, removing, or granting full_access permissions.

Risk: Broad activation wording could cause the agent to handle sensitive sharing or collaborator requests without enough context.

Mitigation: Confirm the target Feishu asset, member identifier, member type, and requested permission level before executing any permission-changing action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sumuzhi4843-a/skills/feishu-perm)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu permission-management guidance and command payload examples for listing, adding, and removing collaborators.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
