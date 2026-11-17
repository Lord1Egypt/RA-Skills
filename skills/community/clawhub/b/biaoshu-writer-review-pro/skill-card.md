## Description:

标书检查工具 helps agents use 百炼®标书 to interpret tender files, generate bid documents, review bid compliance risks, and compare bid files for similarity or duplicate-risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External bidding teams and agents use this skill to process legally held tender and bid documents for tender interpretation, bid document drafting, compliance review, and bid-file similarity checks. It is oriented toward Chinese bidding workflows and produces review summaries, reports, and bid-document outputs through the 百炼®标书 service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles confidential tender and bid files and uses an account API key.

Mitigation: Install only when the publisher is trusted with these files and credentials; keep the API key out of chat and rotate it if exposure is suspected.

Risk: Server evidence says review is needed because some code and instructions exceed the declared boundaries.

Mitigation: Review the skill before deployment, confirm the allowed network and file-access boundaries, prefer the default output directory, and avoid broad custom output paths.

Risk: Uploaded files and generated results are retained under the API-key account on the 百炼®标书 service.

Mitigation: Confirm server-side retention is acceptable before first use and manage historical data through the platform account.

Risk: Bid generation, compliance review, and duplicate checking can consume account word quota.

Mitigation: Confirm paid operations and page-count choices before submission, and treat estimated usage as advisory until final platform settlement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-review-pro)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼®标书 platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [百炼®标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [智能解读与标书制作 API](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [知识库字段说明](references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown or text guidance, JSON results, HTML or Word reports, local files, and generated .docx bid documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some operations upload user-provided documents to 百炼®标书, use an account API key, consume available word quota, and may return short-lived download links.]

## Skill Version(s):

3.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
