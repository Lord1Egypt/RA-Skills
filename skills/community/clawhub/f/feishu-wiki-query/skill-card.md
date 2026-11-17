## Description:

Feishu Wiki Query helps an agent retrieve Feishu wiki content, including text, images, whiteboards, and spreadsheets, from configured knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwsong](https://clawhub.ai/user/fwsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Feishu knowledge bases, browse wiki directories, read documents, and return sourced answers from Feishu content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary reports exposed Feishu app credentials.

Mitigation: Revoke the exposed secret, rotate credentials, and clear packaged configuration before using the skill with real Feishu resources.

Risk: The release security guidance warns about image upload and message sending behavior.

Mitigation: Require clear user approval and verify intended recipients before uploading images or sending Feishu messages.

Risk: The release security summary notes broader spreadsheet permission guidance.

Mitigation: Use least-privilege Feishu spreadsheet permissions where possible, or document why broader access is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fwsong/skills/feishu-wiki-query)
- [Publisher Profile](https://clawhub.ai/user/fwsong)
- [Feishu Open Platform APIs](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline code blocks, command examples, and sourced Feishu knowledge base results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results are expected to include a visible Feishu knowledge base source label.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
