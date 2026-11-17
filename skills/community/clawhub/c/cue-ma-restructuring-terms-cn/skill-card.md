## Description:

将一份 A 股并购重组披露文件整理为八项带原文引句和出处锚点的条款卡，并标出未检索内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

分析师及其他阅读 A 股公司披露文件的人可用它从重大资产重组报告书、预案等文件中提取八类交易条款，保留逐字引句和定位锚点，并列出未检索项目；估值、交易成败和股价判断交由人工。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using optional online services with confidential filings or mishandling the API key could expose sensitive information or credentials.

Mitigation: Use public, unannotated filings with online services; keep confidential documents local unless external processing is authorized and retention terms are understood. Verify the HTTPS destination before sending the key, and never paste it into chat.

Risk: Extracted terms may be incomplete or inaccurate compared with the original filing.

Mitigation: Check each extracted term and source anchor against the original filing.

## Reference(s):

- [M&A terms reference](references/ma-terms.md)
- [Cue data MCP configuration](https://cuecue.cn/hub/mcp)
- [Cue attachment and PDF reader configuration](https://cuecue.cn/hub/omni-reader)
- [Cue live service catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown clause card with eight quoted items, source anchors, comparison, missing-data list, and human-review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One card per supplied filing; unavailable clauses are identified explicitly, and investment or approval judgments remain for human review.]

## Skill Version(s):

0.1.0 (source: release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
