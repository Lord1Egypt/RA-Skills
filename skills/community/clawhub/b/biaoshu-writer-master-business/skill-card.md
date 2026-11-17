## Description:

Assists with Chinese tender and bid workflows by interpreting tender documents, generating bid documents, reviewing bid compliance risks, and checking similarity across bid files through the 百炼®标书 service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and bid teams use this skill to analyze tender requirements, generate .docx bid responses, review compliance risks, and compare legally held bid documents for similarity signals before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents may contain confidential commercial, pricing, and personal information and are processed by the 百炼®标书 service.

Mitigation: Use the skill only after confirming the user is authorized to upload the files and trusts the service with those materials.

Risk: The API key controls the user's account quota and could be exposed through chat history, screenshots, or forwarded key-bearing links.

Mitigation: Keep the API key out of chat, store it only in the skill-local config file with restricted permissions, and do not share URLs that contain key or bind-key parameters.

Risk: The security guidance flags custom report basenames and output paths as an area to avoid until path handling and metadata persistence are tightened.

Mitigation: Prefer the default output directory and generated names unless the path behavior has been reviewed.

Risk: Generated bid content, compliance review, and similarity checks may be incomplete, inaccurate, or unsuitable as a legal determination.

Mitigation: Require human review before submission and treat similarity results as internal risk signals rather than findings of misconduct or legal compliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-master-business)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼®标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [百炼®标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [智能解读与标书制作 API](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [执行细节（操作手册）](references/usage.md)
- [知识库字段说明](references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Plain text and Markdown responses, plus generated HTML, Word, JSON, and .docx bid artifacts when the upstream service returns them.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local report paths or short-lived download links; generated bid, review, and similarity results depend on uploaded user documents and the user's 百炼®标书 account quota.]

## Skill Version(s):

3.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
