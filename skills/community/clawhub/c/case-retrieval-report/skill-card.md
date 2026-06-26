## Description: <br>
生成面向中国裁判文书类案检索的标准化报告，使用得理案例检索 API 执行检索、筛选、比对分析和裁判规则提炼。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal professionals and legal operations teams use this skill to prepare Chinese similar-case retrieval reports for court submission or internal litigation strategy. It collects matter facts, searches Delilegal case data, compares similar cases, and summarizes judicial views in a structured report. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive legal facts and API credentials to Delilegal. <br>
Mitigation: Use only information the user is permitted to share, redact party details where possible, and avoid entering production credentials until security review is complete. <br>
Risk: The artifact disables HTTPS certificate and hostname verification for the API request path. <br>
Mitigation: Do not use a real API key or confidential matter data until certificate verification is fixed and the connection can be trusted. <br>
Risk: Similar-case retrieval can produce incomplete or misleading legal conclusions if results are not checked against authoritative sources. <br>
Mitigation: Cross-check key cases through official sources and present both favorable and unfavorable cases before relying on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolalam/case-retrieval-report) <br>
- [Delilegal case retrieval API](https://platform.delilegal.com/api/v1/generice/case/list) <br>
- [API guide](references/api-guide.md) <br>
- [Report template](references/report-template.md) <br>
- [Legal basis](references/legal-basis.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional shell command invocations and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Delilegal API key; case reports should preserve data-source attribution and distinguish assumptions from verified case data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
