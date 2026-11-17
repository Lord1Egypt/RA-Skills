## Description:

标书合规性审查工具 helps agents use 百炼®标书 to interpret tender requirements, generate bid documents, review bid compliance risks, and compare bid files for similarity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, proposal, and bid teams use this skill to process tender and bid documents through 百炼®标书 for tender interpretation, bid drafting, compliance review, and duplicate or similarity checks before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents may contain confidential business or personal data and are sent to biaoshu.zhiliaobiaoxun.com for processing.

Mitigation: Use the skill only with documents the user is authorized to upload, and confirm the user accepts cloud processing under their Api Key and account billing before submission.

Risk: The security review flags forced referral-linked user output and local write behavior beyond the stated boundary.

Mitigation: Review user-facing platform links and local output settings before use, and constrain generated files to an intended output directory.

Risk: The Api Key controls account access and billing.

Mitigation: Keep the Api Key out of chat, store it only in the skill-local config file with restricted permissions, and do not forward links that include credential or bind-key parameters.

Risk: Local filename-to-job metadata may be retained in ~/.zcm/projects.json.

Mitigation: Inspect or delete ~/.zcm/projects.json when retained local task metadata is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-review)
- [百炼®标书 platform](https://biaoshu.zhiliaobiaoxun.com/)
- [百炼®标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [标书制作 API workflow](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [知识库字段参考](references/knowledge-fields.md)
- [执行细节](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with API-derived summaries, JSON results, local HTML or Word reports, and generated .docx bid documents or short-lived download links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on 百炼®标书 API processing, account word balance, user-provided files, and local output-path configuration.]

## Skill Version(s):

3.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
