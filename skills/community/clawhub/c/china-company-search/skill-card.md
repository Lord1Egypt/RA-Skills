## Description: <br>
China company search and business registry skill by Fengniao (Riskbird) for KYB, supplier verification, company due diligence, corporate risk screening, and counterparty checks on Chinese companies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinshu001](https://clawhub.ai/user/xinshu001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External compliance, procurement, onboarding, and business teams use this skill to verify Chinese companies, screen suppliers and counterparties, and prepare due diligence summaries from Riskbird-backed registry and risk data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, person names, entids, and related lookup parameters are sent to Riskbird. <br>
Mitigation: Install and use the skill only for approved Riskbird-backed due diligence workflows, and avoid submitting sensitive inputs that are not approved for third-party processing. <br>
Risk: A private FN_API_KEY is passed to the Riskbird API as a URL parameter. <br>
Mitigation: Use a private key only where URL-parameter credential exposure is acceptable, and account for logs, proxies, and monitoring systems that may record request URLs. <br>
Risk: Auto-invocation may trigger for broad supplier, contract, or company-background prompts. <br>
Mitigation: Confirm the intended lookup scope and disambiguate ambiguous company or person names before calling Riskbird endpoints. <br>
Risk: The built-in public API key has a daily quota. <br>
Mitigation: Configure a private FN_API_KEY for reliable use, or retry after the public quota resets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xinshu001/china-company-search) <br>
- [Riskbird](https://www.riskbird.com/) <br>
- [Riskbird skills quota page](https://www.riskbird.com/skills) <br>
- [企业尽调报告生成指南](references/due_diligence_report.md) <br>
- [风鸟 API 字段定义 - 通用结构 & 工商维度](references/field_definitions_common_bizinfo.md) <br>
- [风鸟 API 字段定义 - 法律风险](references/field_definitions_legal.md) <br>
- [风鸟 API 字段定义 - 风险信息](references/field_definitions_risk.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [JSON API responses and Markdown summaries or due diligence reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Riskbird API key from FN_API_KEY or a built-in public key; public-key usage is quota-limited.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
