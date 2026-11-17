## Description:

Guides OpenClaw agents through Feishu document writing workflows, including source reading, document creation, incremental updates, focused editing, proposal formalization, human-sounding rewrites, and link-based delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyilt](https://clawhub.ai/user/tianyilt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help agents produce Feishu documents from source material, refine existing drafts, formalize proposal-style content, and return a document URL as the final deliverable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad document mutation guidance can lead an agent to edit or delete the wrong Feishu content.

Mitigation: Confirm the exact target document or workspace before write operations, and prefer fetch plus precise range replacement over delete_range, replace_all, or overwrite.

Risk: Permission-expansion guidance can encourage broader tool access than the task requires.

Mitigation: Grant only the Feishu permissions needed for the requested document workflow, and do not enable an unrestricted full tool profile solely to resolve a Feishu permission error.

Risk: Generated or rewritten documents can introduce incorrect or misleading guidance.

Mitigation: Review source context and generated document content before sharing or treating the Feishu document as final.

## Reference(s):

- [Feishu document writing quick reference](references/quick-reference.md)
- [OpenClaw Feishu document writing best practices](references/best-practices.md)
- [Open-box and permission handling rules](references/open-box-rules.md)
- [Feishu writing workflows](references/workflows.md)
- [Feishu writing style guide](references/style-guide.md)
- [Self-contained capability map](references/skill-map.md)
- [Reference documents](references/reference-docs.md)
- [OpenClaw Feishu writing best practices example](https://fudan-nlp.feishu.cn/wiki/WZVMwUEnXiHUqLkfzDycSp9en2c?from=from_copylink)
- [Feishu writing reference document](https://fudan-nlp.feishu.cn/docx/HdWfdNomtoGd7yxL3gVcFgrhnnb)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Feishu tool-call patterns and concise delivery text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu document URLs after create or update workflows when the required Feishu tools and permissions are available.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
