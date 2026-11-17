## Description:

招标文件智能解读 helps agents use 百炼®标书 to interpret tender requirements, generate bid documents, review compliance risks, and compare bid files for similarity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users, bidding teams, and procurement-support agents use this skill to analyze tender files, prepare bid-document drafts, review submission risks, and check similarity across legally held bid files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive tender and bid files are uploaded to the named vendor service under the user's Api Key.

Mitigation: Install only if that data handling is acceptable; confirm consent before upload and avoid sending unrelated local files.

Risk: The security review says bundled scripts can exceed the declared local file read/write boundaries.

Mitigation: Confirm every file path before execution, use a dedicated output folder, and monitor files created in biaoshu-bailian-files and ~/.zcm.

Risk: Generated documents, reports, and local credential-related files may persist after use.

Mitigation: Use a dedicated output location, protect the skill-local Api Key configuration, and remove local artifacts when retention is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-tender-reader)
- [百炼®标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [百炼®标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [智能解读与标书制作 API](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [知识库字段说明](references/knowledge-fields.md)
- [执行细节（操作手册）](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON summaries, HTML or Word reports, and generated .docx bid documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local report files and short-lived download links for generated bid documents.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
