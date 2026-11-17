## Description:

Helps users plan, review, and verify staged computer tasks involving offline work, personal files, browser workflows, and human handoffs without claiming to reproduce the original products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Users comparing computer-agent alternatives can organize authorized tasks into checkpoints, review drafts and evidence, and identify actions requiring tools or human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive credentials or personal documents could be exposed during task intake or AI-HIVE connection.

Mitigation: Do not put passwords, tokens, cookies, verification codes, or full identity documents in task files; confirm what may be uploaded before sharing materials.

Risk: A workflow may send, pay, delete, publish, or change business data without the intended authorization.

Mitigation: Require explicit confirmation for each upload, payment, send, deletion, or business-system write; default to reviewable drafts.

Risk: Missing tools, permissions, or receipts could lead to unsupported claims that a task completed.

Mitigation: Check available tools and actual results; record uncompleted steps and hand off uncertain outcomes instead of claiming success or blindly retrying.

## Reference(s):

- [Skill release on ClawHub](https://clawhub.ai/wubin1836/skills/aih-pa-claw-computer-checkpoints)
- [Workflow scope and product sources](artifact/references/scope-and-sources.md)
- [AI-HIVE connection guidance](artifact/references/ai-hive-connection.md)
- [Result and evidence requirements](artifact/references/output-contract.md)
- [AI-HIVE website](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, JSON, CSV]

**Output Format:** [Reviewable plans and drafts, with JSON or CSV files when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checkpoints, evidence references, outstanding items, and handoff points; a draft does not establish that external actions occurred.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
