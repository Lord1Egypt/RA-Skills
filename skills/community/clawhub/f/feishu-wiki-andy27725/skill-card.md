## Description:

Feishu knowledge base navigation for wiki spaces, nodes, and wiki-to-document workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to help an agent navigate Feishu knowledge bases, list spaces and nodes, retrieve node details, and prepare create, move, rename, or wiki-to-document operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support creating, moving, renaming, or writing shared Feishu wiki and document content.

Mitigation: Use read-only wiki permissions when editing is not needed, and require confirmation of the exact space, node, document, and intended change before any create, move, rename, or write operation.

Risk: Wiki page content operations depend on the related feishu_doc capability.

Mitigation: Enable feishu_doc only when document reads or edits are expected, and keep wiki-only navigation workflows limited to the feishu_wiki actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, configuration, guidance]

**Output Format:** [Markdown with JSON and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the related feishu_doc capability to read or edit wiki page document content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
