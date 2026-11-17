## Description:

投标文件智能生成 helps agents analyze tender documents, generate bid document .docx files, review bid compliance, and compare bid files for similarity using the 百炼®标书 cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External bid teams and procurement-support users use this skill to process legally held tender and bid files for bid interpretation, document generation, compliance review, and similarity checks. It is intended for workflows where users can upload sensitive bidding documents to the 百炼®标书 service under their own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid files, generated results, and account activity are processed server-side under the user's API key.

Mitigation: Use the skill only for documents the user is allowed to upload, and confirm consent before first upload.

Risk: The security summary reports under-disclosed persistent local state.

Mitigation: Review local configuration and generated metadata before installation or redistribution, and keep API keys out of chat and release packages.

Risk: The security guidance reports unsafe report path handling that could write outside the intended output boundary.

Mitigation: Do not expose report filename or output path options to untrusted input; constrain report output to a reviewed local directory until path handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-bid-gen)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼®标书 platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [Open API overview](references/api.md)
- [Authentication, tasks, and word entitlements](references/api-auth.md)
- [Bid interpretation and generation workflow](references/api-bid-workflow.md)
- [Bid compliance review API](references/api-compliance.md)
- [Bid duplicate checking API](references/api-duplicate.md)
- [Knowledge base fields](references/knowledge-fields.md)
- [Usage and operating manual](references/usage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Text and Markdown responses, JSON results, generated .docx bid documents, HTML/Word reports, download links, and local file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-managed 百炼®标书 API key; uploads user-provided tender and bid files to the cloud service; generated reports use zh-CN bidding labels; bid generation, review, and duplicate checks may consume account word balance.]

## Skill Version(s):

3.1.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
