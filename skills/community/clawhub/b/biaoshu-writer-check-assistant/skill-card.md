## Description:

上传招标或投标文件后，该 skill 可帮助 agent 解读招标要求、生成投标文件、审查合规风险，并比较投标文件的相似或雷同风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

Bid and procurement users can use this skill to process authorized tender and bid files for requirement interpretation, generated bid-document drafts, compliance review, and duplicate or similarity checks. It is designed for workflows that use the 百炼标书 cloud service with the user's own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid files can contain confidential procurement or business information and are uploaded to biaoshu.zhiliaobiaoxun.com for processing.

Mitigation: Use only files the user is authorized to process, review confidentiality requirements before installation, and disclose that processing occurs through the 百炼标书 service.

Risk: Bid generation, review, and duplicate checking may consume the user's paid word balance under their API key.

Mitigation: Require the user's own API key, avoid collecting or echoing credentials in chat, and explain that paid operations may reduce the account balance.

Risk: The skill stores project and job-to-filename metadata in ~/.zcm/projects.json by default, outside the declared output directory.

Mitigation: Review local storage behavior before deployment and clear or relocate project metadata when local retention is not acceptable.

Risk: Mandatory referral-style platform links appear in the user guidance.

Mitigation: Review the guidance text for policy, disclosure, and marketplace requirements before publishing or deploying.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-check-assistant)
- [百炼标书开放 API 总调度](artifact/references/api.md)
- [智能解读与标书制作 API](artifact/references/api-bid-workflow.md)
- [标书审查 API](artifact/references/api-compliance.md)
- [标书查重 API](artifact/references/api-duplicate.md)
- [鉴权、任务与可用字数接口](artifact/references/api-auth.md)
- [知识库字段说明](artifact/references/knowledge-fields.md)
- [百炼标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Natural-language guidance plus generated HTML, Word, DOCX, and JSON report artifacts depending on the workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include cloud-processed bid documents, compliance reports, duplicate-check JSON, local report files, and short-lived download links.]

## Skill Version(s):

3.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
