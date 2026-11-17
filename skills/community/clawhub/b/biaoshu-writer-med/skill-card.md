## Description:

帮助投标团队解读招标文件、生成投标文件，并审查合规及多份投标文件的相似风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

投标团队和代理机构可用它解读招标要求、起草投标文件，并在提交前检查合规问题和不同投标文件之间的相似风险。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender documents, generated results, and account-related data are processed by the vendor cloud service.

Mitigation: Upload only documents authorized for vendor processing; review confidentiality and retention requirements first.

Risk: Account setup and data-collection disclosures conflict with what the skill actually collects and stores; automatic trial enrollment may collect device-identifying data.

Mitigation: Avoid automatic trial enrollment without explicit consent to device-identifying data collection.

Risk: API keys and SMS codes used for account access may be exposed through chat or local storage.

Mitigation: Use dedicated secret storage rather than sharing credentials in chat, and keep the service URL fixed to the documented vendor endpoint.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/biaoshu-writer-med)
- [百炼®标书平台](https://biaoshu.zhiliaobiaoxun.com/?ch=s95)
- [使用指南](artifact/references/usage.md)
- [开放 API 指南](artifact/references/api.md)
- [标书查重接口](artifact/references/api-duplicate.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown guidance and reports in JSON, HTML, Word, or DOCX format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents and reports may be saved locally or provided through time-limited download links.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
