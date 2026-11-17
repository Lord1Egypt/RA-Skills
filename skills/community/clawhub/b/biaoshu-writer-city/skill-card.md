## Description:

协助采购与投标人员解读招标文件、生成投标文件，并审查合规性与文件相似风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

采购和投标人员用它分析招标要求、制作投标书，并检查废标风险、合规问题及多份投标文件的相似性。文件交由第三方云服务处理，生成、审查和查重可能消耗账户可用字数。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential tender and bid files are processed by the vendor cloud service.

Mitigation: Confirm the vendor's cloud processing and data-retention terms meet procurement confidentiality requirements before uploading sensitive files.

Risk: Automatic trial setup sends device-identifying fields.

Mitigation: Use an existing API key instead of automatic trial registration if device identification is not acceptable.

Risk: The API key is stored locally in the skill directory.

Mitigation: Protect the local credential file and avoid sharing the key in output or URLs.

Risk: Remote file inputs can include internal-only URLs.

Mitigation: Provide only trusted, publicly intended file URLs or upload approved local files instead.

Risk: Generation, review, and similarity checks may consume account credits.

Mitigation: Check the account's available balance and expected consumption before submitting paid work.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/biaoshu-writer-city)
- [API reference](references/api.md)
- [Usage guide](references/usage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Text or Markdown summaries; HTML or Word reports and DOCX bid documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bid documents may be delivered through expiring download links or saved locally on request.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
