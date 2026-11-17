## Description:

生成A股综合分析报告（深交所、上交所、北交所），包含K线技术指标图表、同行业对比、基本面分析、主营业务构成、技术面评分、催化剂与风险、短线和中线买卖建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bwgao](https://clawhub.ai/user/bwgao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill through an agent to turn an A-share stock name or code into a structured market analysis workflow and generated local report. The workflow resolves stock codes, gathers market and fundamentals data, creates charts, and drafts a report following the bundled template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include untrusted market or news text without sufficient escaping.

Mitigation: Treat generated reports as untrusted HTML, review them before opening or sharing, and add output escaping plus a restrictive content security policy before broader use.

Risk: The data pipeline uses plaintext market-data endpoints and external provider requests.

Mitigation: Run the skill in an isolated virtual environment or container, prefer HTTPS-capable data sources where available, and avoid exposing sensitive network or credential context.

Risk: Optional TUSHARE_TOKEN-backed requests and stock queries are sent to external providers.

Mitigation: Use a least-privilege token, avoid embedding secrets in prompts or reports, and disclose external data-provider access to users.

## Reference(s):

- [Peer Selection Rules](references/peer_selection_rules.md)
- [Report Template](references/report_template.md)
- [Technical Scoring](references/technical_scoring.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus generated JSON data, PNG charts, and standalone HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is scoped to A-share equities and may contact external market-data providers, including optional TUSHARE_TOKEN-backed requests.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
