## Description:

上传招标/投标文件后，该 skill 可调用百炼®标书开放 API 解读招标文件、生成 .docx 投标文件、审查废标风险并比较 2-3 份投标文件的相似或雷同风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and bidding teams use this skill to process legally held tender and bid files through 百炼®标书 for tender interpretation, bid document drafting, compliance review, and similarity checks before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid files may contain confidential commercial, pricing, or personal data and are uploaded to a third-party service for processing.

Mitigation: Confirm authorization and user consent before upload, and use only files the user is permitted to process with the service.

Risk: Paid operations may charge against the API key account's available words.

Mitigation: Tell the user before paid generation, review, or duplicate-check tasks begin, and do not paste or request the API key in chat.

Risk: The security evidence says the skill can write persistent local project metadata outside its stated area.

Mitigation: Review and disclose the ~/.zcm metadata behavior, or configure/relocate it before deployment.

Risk: The security evidence says reports can be written outside the approved output folder.

Mitigation: Constrain report filenames and output directories to the approved generated-output location before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-ace)
- [百炼®标书 Platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [百炼®标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [智能解读与标书制作 API](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [知识库字段说明](references/knowledge-fields.md)
- [执行细节（操作手册）](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Plain-language guidance plus generated DOCX, HTML or Word reports, JSON results, and short-lived download links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid operations may consume available words on the API key account; generated reports and bid files may be written locally or retrieved by short-lived service links.]

## Skill Version(s):

3.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
