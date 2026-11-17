## Description:

将年报附注中的长期股权投资披露整理为逐条可追溯到原句与来源锚点的台账，并按披露分别登记分类、核算方法、收益、分红、减值与处置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

供阅读中国企业年报的投资者、分析人员与财务研究人员使用，将长期股权投资附注整理成带原句、页表锚点和来源链接的七节 Markdown 台账。技能只登记披露内容，不评价投资价值或给出买卖建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is suspicious and partial; its summary cites MCP service discovery, credentialed requests, and external document parsing, so the scan evidence is incomplete.

Mitigation: Use only documents you are permitted to share with the connected service, inspect the live MCP catalog and tool list before connecting, and provide CUE_API_KEY only when the retrieval and parsing features are needed.

Risk: The skill leaves a persistent local usage marker under ~/.cue-usage on first run.

Mitigation: Review or remove the marker if you do not want to retain this local usage record.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-long-term-equity-investment-cn)
- [CUE MCP setup](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader setup](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Chinese Markdown with seven sections, quoted evidence, source anchors, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps disclosed figures separate, names missing information, and does not provide investment recommendations.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
