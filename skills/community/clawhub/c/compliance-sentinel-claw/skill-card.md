## Description: <br>
合规哨兵监控虾 monitors suppliers and customers for business registration changes, litigation, dishonest-executor records, and related compliance risk signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance, procurement, legal, and operations teams use this skill to review partner onboarding risk, monitor supplier or customer changes, batch-scan company lists, and produce risk summaries or monthly monitoring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles partner company names, unified social credit codes, Feishu compliance records, and commercial data-source credentials. <br>
Mitigation: Use least-privilege Feishu and commercial API credentials, restrict monitoring to authorized companies, and define who may view, retain, export, or delete compliance records. <br>
Risk: Free or public data sources may be delayed, rate limited, or incomplete, especially for judicial records and overseas companies. <br>
Mitigation: Confirm significant findings against authoritative sources, tune query frequency to data-source limits, and configure appropriate commercial or overseas data sources when higher coverage is required. <br>
Risk: Automated risk scores and alert templates can overstate or understate partner compliance risk. <br>
Mitigation: Require human review by the responsible compliance, procurement, or legal owner before pausing cooperation, payments, or contracts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/compliance-sentinel-claw) <br>
- [Risk rules](references/risk-rules.md) <br>
- [Data sources](references/data-sources.md) <br>
- [Notification templates](references/notification-templates.md) <br>
- [National Enterprise Credit Information Publicity System](https://www.gsxt.gov.cn/) <br>
- [China Judgments Online](https://wenshu.court.gov.cn/) <br>
- [Dishonest Judgment Debtors Query](https://zxgk.court.gov.cn/shixin/) <br>
- [Qichacha Open API](https://openapi.qcc.com/) <br>
- [Tianyancha Open API](https://open.tianyancha.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with optional JSON query output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include company risk levels, scores, source notes, Feishu notification content, CSV import summaries, and monthly report templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
