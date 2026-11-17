## Description:

快标书标书智能写作 helps agents process tender and bid files through the 百炼®标书 service for structured interpretation, bid document generation, compliance review, and duplicate or similarity checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to upload or reference tender and bid documents, then receive bid interpretation, generated bid documents, compliance review findings, and duplicate/similarity risk checks for bidding workflows. The workflow is oriented to Chinese procurement terminology and requires a user-managed 百炼®标书 API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents are sent to biaoshu.zhiliaobiaoxun.com under the user's API-key account.

Mitigation: Use only after the user confirms they are comfortable uploading those documents to the service.

Risk: The API key is stored in the skill directory and controls access to the user's account.

Mitigation: Keep the credential file local, restrict its permissions, and do not paste or expose the key in chat or links.

Risk: Reports or downloaded documents may overwrite unrelated local files if output paths are chosen carelessly.

Mitigation: Choose explicit output paths in the intended skill output directory and review paths before writing files.

Risk: The authoritative security verdict is suspicious because of reduced operational transparency and overbroad local file-write paths.

Mitigation: Review the skill before installing and monitor its file-write behavior during use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-radar)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼®标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [百炼®标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [智能解读与标书制作 API](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [知识库字段说明](references/knowledge-fields.md)
- [执行细节（操作手册）](references/usage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text responses with generated DOCX files, HTML or Word reports, JSON summaries, and short-lived download links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided tender or bid documents and a user-managed API key; generated documents and reports may be written to local output paths.]

## Skill Version(s):

1.0.15 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
