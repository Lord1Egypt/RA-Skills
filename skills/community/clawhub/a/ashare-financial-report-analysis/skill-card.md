## Description:

A股上市公司财报结构化拆解系统，基于16节固定模板，对季报和年报进行一手数据提取、自算核验和跨季度可比的结构化分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxyzcyxpp](https://clawhub.ai/user/chenxyzcyxpp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce structured A-share earnings-report analysis from a stock code and reporting period. It guides the agent through financial statement retrieval, fixed-section report drafting, calculation checks, source labeling, and risk review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat generated financial analysis as investment advice.

Mitigation: Present outputs as research support only and include the artifact's non-investment-advice disclaimer.

Risk: Financial values may be misleading if the agent fills gaps from memory or unverified sources.

Mitigation: Use actual Tushare, akshare, baostock, Eastmoney, or official disclosure data; when retrieval fails, mark the item as unavailable instead of inventing values.

Risk: A known Tushare free_cashflow field mismatch can produce incorrect cash-flow conclusions.

Mitigation: Compute free cash flow directly as operating cash flow minus capital expenditure and do not rely on the precomputed free_cashflow field.

Risk: API permission gaps or stale daily data can leave sections incomplete.

Mitigation: Use the documented fallback sources, retry prior trading dates where appropriate, and label sections that require manual or official-document review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenxyzcyxpp/skills/ashare-financial-report-analysis)
- [A-share earnings template](references/a-share-earnings-template.md)
- [Tengjing 2025 case study](references/case-study-tengjing-2025.md)
- [CNINFO announcements](http://www.cninfo.com.cn)
- [Eastmoney datacenter API](https://datacenter-web.eastmoney.com/api/data/v1/get)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured earnings-analysis report with tables, formulas, source notes, and risk flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are research support and should include data-source labels, N/A markers for missing data, and a non-investment-advice disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
