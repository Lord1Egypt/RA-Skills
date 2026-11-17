## Description:

上传招标或投标文件后，该 skill helps an agent interpret tender requirements, identify bid-disqualification and scoring risks, generate finished bid documents, review bid compliance, and compare bid files for similarity or duplication risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and bidding teams use this skill to process authorized tender and bid documents for interpretation, bid-document drafting, compliance review, and similarity checks before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents may be uploaded to a third-party vendor service and processed under that service's account retention and billing model.

Mitigation: Before installation or use, confirm that the user is authorized to upload the documents to the vendor service and accepts the service's retention and billing behavior.

Risk: Generated reports or state may be written outside the declared output boundary, including possible local state under ~/.zcm/projects.json.

Mitigation: Use a dedicated output directory, review local writes during installation, and avoid granting broader filesystem access than the task requires.

Risk: Untrusted document text or third-party instructions could influence output paths or report basenames.

Mitigation: Keep output paths user-controlled or confined to the dedicated output directory, and sanitize report names before writing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-insight)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼®标书 platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [百炼®标书开放 API 总调度](artifact/references/api.md)
- [鉴权、任务与可用字数接口](artifact/references/api-auth.md)
- [智能解读与标书制作 API](artifact/references/api-bid-workflow.md)
- [标书审查 API](artifact/references/api-compliance.md)
- [标书查重 API](artifact/references/api-duplicate.md)
- [知识库字段说明](artifact/references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational text, Markdown reports, generated .docx bid documents, HTML/Word review reports, JSON duplicate-check results, and local command/configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local report paths, short-lived document download links, account usage messages, and zh-CN bidding terminology from the vendor platform.]

## Skill Version(s):

3.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
