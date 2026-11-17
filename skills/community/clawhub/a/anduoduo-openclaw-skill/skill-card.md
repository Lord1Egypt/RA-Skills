## Description:

面向安多多平台 OpenClaw API 的数据分析与查数技能，用于云资产风险、风险聚合、风险资产盘点、整体风险情况、高风险分布、规则下钻、合规摘要、合规报告、查数报告和 HTML 报告生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anduoduo](https://clawhub.ai/user/anduoduo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and cloud operations teams use this skill to query Anduoduo OpenClaw API data for cloud asset risk analysis, rule drilldowns, compliance summaries, and report generation. It helps turn OpenClaw API documentation into guided API calls, concise findings, and sanitized HTML or file-based reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive cloud security data and generated report delivery.

Mitigation: Review before installing; use a least-privilege Anduoduo API key, confirm API calls and report exports, and sanitize API-derived fields before sharing reports.

Risk: API credentials could be exposed through prompts, logs, files, or non-official destinations.

Mitigation: Use credentials only for requests to the official Anduoduo API domain, avoid printing keys, and do not persist keys in plaintext files.

Risk: Generated reports can contain real account names, instance names, environment identifiers, download links, or remote JavaScript.

Mitigation: Share only reviewed final reports through private, approved, encrypted, short-lived storage, and avoid remote JavaScript in reports intended for distribution.

Risk: Broad page queries, unstable pagination assumptions, and direct cloudAccountId filtering can produce misleading analysis.

Mitigation: Start with probes and aggregation, use small-page detail queries, prefer verified filters such as ruleId, severities, cloudInstanceId, and instanceHashId, and document uncertainty when account-level filters are requested.

Risk: Cloud-account onboarding through this skill can expand access or mutate platform configuration.

Mitigation: Avoid cloud-account onboarding through this skill unless separately reviewed and explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anduoduo/skills/anduoduo-openclaw-skill)
- [Anduoduo platform](https://www.anduoduo.cloud/)
- [Anduoduo help document](https://lv8u92t29eh.feishu.cn/docx/AnJVdze5Co0ZrhxFKMicfrDBnPd)
- [OpenClaw API reference](references/anduoduo_api_final.md)
- [API understanding and query playbook](references/api_understanding_and_query_playbook.md)
- [Default risk query SOP](sops/default_risk_query.md)
- [Rule drilldown SOP](sops/rule_drilldown.md)
- [Compliance summary and report SOP](sops/compliance_summary_and_report.md)
- [Best practices](references/best_practices.md)
- [Pitfalls](references/pitfalls.md)
- [Verification status](references/verification_status.md)
- [Report guidelines](references/report_guidelines.md)
- [Delivery strategy](references/delivery_strategy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with inline API call guidance and generated HTML, CSV, JSON, DOCX, or ZIP files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Anduoduo API key through ANDUODUO_API_KEY or explicit session-only user input; generated reports should be sanitized before delivery.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
