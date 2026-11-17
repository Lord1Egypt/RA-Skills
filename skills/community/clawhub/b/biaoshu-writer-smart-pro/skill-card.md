## Description:

上传招标或投标文件后，该 skill helps an agent use the 百炼标书 service to interpret tender requirements, generate finished bid documents, review bid compliance risks, and compare bid documents for similarity risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process legally held tender and bid files through 百炼标书 for tender interpretation, bid document generation, compliance review, and bid similarity checking. It is suited to bid-preparation workflows where generated documents and risk reports still need user review before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive tender and bid documents are uploaded to the 百炼标书 cloud service for processing.

Mitigation: Use the skill only after confirming the user is comfortable sending those files to that service and has authority to process the documents.

Risk: The required API key can spend the account's available word balance.

Mitigation: Keep the API key out of chat, store it only in the local skill config, and review balance-related prompts before paid actions.

Risk: Security evidence flags under-scoped local file-writing and persistence behavior, including output-path handling and an undeclared ~/.zcm project metadata cache.

Mitigation: Review or constrain output paths and avoid custom --out-dir, --basename, ZCM_HOME, ZCM_OUTPUT_DIR, or arbitrary save paths unless the execution context is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-smart-pro)
- [百炼标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [百炼标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [智能解读与标书制作 API](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [知识库字段说明](references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance and concise status text, with generated DOCX bid documents, HTML or Word reports, JSON-style result summaries, and local configuration instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include short-lived download links, local report paths, compliance or duplicate-risk summaries, and account word-balance notices from the upstream service.]

## Skill Version(s):

3.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
