## Description:

Feishu Wiki Writer guides agents through creating, fully writing, and validating large Feishu Wiki or cloud-drive documents while avoiding ordering conflicts and duplicate documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwz119](https://clawhub.ai/user/xwz119)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to create or update large Feishu Wiki documents, assemble Markdown locally, write it in one pass, and read the document back for verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hard-coded Feishu knowledge base space ID in the creation example could direct content to the wrong workspace.

Mitigation: Before creating or overwriting content, confirm the target Feishu workspace, parent node, and document token with the user.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, API calls, Configuration]

**Output Format:** [Markdown guidance with JSON examples and Feishu command sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advises full-document writes and post-write readback validation for large Feishu documents.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
