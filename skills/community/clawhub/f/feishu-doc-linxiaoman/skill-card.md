## Description:

Guides agents to create, read, append, overwrite, and manage Feishu document blocks using Markdown content and document tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noir-hedgehog](https://clawhub.ai/user/noir-hedgehog)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to operate Feishu documents: create empty documents, append Markdown content, read existing documents, and update or delete specific blocks when document tokens and block IDs are known.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can overwrite, update, or delete Feishu document content if it is given incorrect document tokens or block IDs.

Mitigation: Confirm document tokens and block IDs before write, update, or delete actions; use read or list_blocks first when uncertain.

Risk: Reading or editing Feishu documents can expose confidential content to an agent that is not authorized for those documents.

Mitigation: Use the skill only with documents the agent is authorized to access, and avoid confidential documents unless access is explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noir-hedgehog/skills/feishu-doc-linxiaoman)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Text]

**Output Format:** [Markdown guidance with JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Feishu document actions for create, read, append, write, list_blocks, get_block, update_block, and delete_block.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
