## Description:

This skill helps users interpret tender documents, generate bid documents, review bids for compliance risks, and compare bid files for similarity using the 百炼®标书 cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and bidding teams use this skill to process tender and bid documents they are authorized to upload: tender interpretation, bid document generation, bid compliance review, and duplicate/similarity risk checking. It is suited to procurement response workflows where generated reports and .docx outputs need human review before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents can contain sensitive commercial, pricing, and personal information and are processed by the external 百炼®标书 service.

Mitigation: Use only documents the user is authorized to upload, confirm upload consent before processing, and avoid files or links the user did not explicitly provide.

Risk: The skill depends on an API key that grants access to the user's 百炼®标书 account.

Mitigation: Keep the API key in the skill-local config file with restricted file permissions, and do not paste, echo, or embed it in chat or links.

Risk: Bid generation, review, and duplicate checking may consume the user's account balance.

Mitigation: Confirm billable actions before submission and explain that any estimates are informational while final consumption is determined by the service.

Risk: Server security guidance identifies review-worthy gaps around custom output paths, redirects, and metadata storage.

Mitigation: Avoid custom output paths or basenames until containment and overwrite behavior are fixed; the publisher should enforce same-origin redirects and document or relocate ~/.zcm metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-assistant-business)
- [百炼®标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [百炼®标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [智能解读与标书制作 API](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [知识库字段说明](references/knowledge-fields.md)
- [执行细节（操作手册）](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with structured summaries, JSON API results, HTML or Word reports, and generated .docx bid documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided local tender or bid files and a skill-local API key; paid actions may consume the user's account balance and service download links may expire.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
