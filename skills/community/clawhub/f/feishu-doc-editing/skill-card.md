## Description:

Performance-optimized guidance for editing Feishu and Lark documents with OpenClaw's feishu_doc tool while preserving formatting and reducing API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqunabc](https://clawhub.ai/user/guoqunabc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and execute targeted Feishu or Lark document edits, including block updates, inserts, tables, image placement, chunked writes, and rate-limit handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unconfirmed operations could modify or delete live Feishu document content.

Mitigation: Confirm the target document, requested edits, and any delete operations before running the workflow.

Risk: Image upload guidance could cause an agent to upload the wrong local file or expose private content.

Mitigation: Confirm each local image file path and destination document before upload, especially for business or private documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqunabc/skills/feishu-doc-editing)
- [ClawHub publisher profile](https://clawhub.ai/user/guoqunabc)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown guidance with Feishu tool-call patterns and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include edit plans, block-operation choices, rate-limit handling, image insertion instructions, and preservation guidance for existing rich text.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
