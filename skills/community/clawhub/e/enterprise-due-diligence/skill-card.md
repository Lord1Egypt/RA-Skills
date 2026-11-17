## Description:

对目标企业开展法律、财务和业务维度尽职调查，整合公开工商数据与用户提供材料，生成结构化 Word 尽调报告和风险检查清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[merlinbeard000](https://clawhub.ai/user/merlinbeard000)

### License/Terms of Use:

MIT-0

## Use Case:

Investment, M&A, procurement, and partnership teams use this skill to perform preliminary or full enterprise due diligence before a transaction or collaboration. It helps an agent gather public company information, combine user-provided materials, classify risks, and generate review-ready reports and checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names and due diligence materials may be shared with configured public-data providers or processed by the agent.

Mitigation: Redact confidential or regulated information where possible and provide only materials needed for the requested report.

Risk: API keys for company-data providers are required for some connector-backed lookups.

Mitigation: Store keys in environment variables, keep them out of prompts and generated files, and rotate them if exposed.

Risk: Public registry, litigation, finance, or media data may be incomplete, stale, or inconsistent across sources.

Mitigation: Cross-check key fields across multiple sources, preserve timestamps and source labels, and mark unresolved fields as pending verification.

Risk: Generated reports can influence investment, M&A, supplier, or partnership decisions.

Mitigation: Treat outputs as due diligence support rather than investment advice, and confirm material findings against official records and first-party documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/merlinbeard000/skills/enterprise-due-diligence)
- [Report template](references/report_template.md)
- [Checklist template](references/checklist_template.md)
- [Risk classification framework](references/risk_classification.md)
- [Data quality rules](references/data_quality.md)
- [MCP connectors reference](references/mcp_connectors.md)
- [Qichacha Open API](https://open.api.qichacha.com)
- [Tianyancha MCP endpoint](https://mcp.tianyancha.com/v1)
- [Qixin MCP endpoint](https://mcp.qixin.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated Word document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces due diligence reports and checklists from public company data and user-provided materials; flags unavailable or unverified data for follow-up.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
