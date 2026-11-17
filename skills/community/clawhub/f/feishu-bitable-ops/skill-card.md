## Description:

Guides agents through Feishu Bitable operations, including wiki and base URL token handling, field write formats, batch operations, CRUD workflows, and common error resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbj375767338-arch](https://clawhub.ai/user/bbj375767338-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent needs to read or update Feishu Bitable bases, create or query records, manage table fields, resolve wiki URLs into Bitable app tokens, and prepare correctly formatted field values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Create, update, batch_create, or delete operations can change Feishu Bitable records if the agent targets the wrong base, table, records, or fields.

Mitigation: Before any write or delete action, require the agent to summarize the exact base, table, records, and fields, then confirm the change explicitly.

Risk: Using a wiki node token as a Bitable app token can cause failed or misdirected operations.

Mitigation: For wiki URLs, resolve the node token first and use the returned object token as the Bitable app token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bbj375767338-arch/skills/feishu-bitable-ops)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline command examples and structured tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu Bitable URL parsing guidance, field value formats, CRUD examples, batch operation limits, and common error handling notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
