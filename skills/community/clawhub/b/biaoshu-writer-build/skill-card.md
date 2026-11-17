## Description:

分析招标文件、生成投标文件，并审查投标文件的合规性和相似性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

投标团队和采购专业人员可使用此技能解读招标要求、制作投标文件、检查合规风险，并比较投标文件的相似性。文件由第三方云服务处理。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bid documents and account data are sent to a third-party cloud service, and the security review flags incomplete disclosure of collection and retention.

Mitigation: Review the vendor's data-handling terms and obtain approval before submitting sensitive documents or account information.

Risk: API keys and SMS codes may be exposed if entered into ordinary chat.

Mitigation: Use a dedicated secret input flow or the vendor website; avoid pasting production credentials or SMS codes into chat unless it is an approved secure channel.

Risk: Automatic trial registration collects device characteristics without clearly disclosed consent.

Mitigation: Require explicit informed consent before trial registration and clarify what device and registration data the vendor collects and retains.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/liu-jiapeng/skills/biaoshu-writer-build)
- [API overview](artifact/references/api.md)
- [Usage guide](artifact/references/usage.md)
- [Bid workflow API](artifact/references/api-bid-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Text or Markdown summaries; DOCX bid documents and HTML or Word reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document generation, review, and similarity checks may consume account word credits.]

## Skill Version(s):

2.0.6 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
