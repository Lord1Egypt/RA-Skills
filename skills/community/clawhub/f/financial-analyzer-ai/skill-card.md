## Description: <br>
AI 财务报表分析 helps analyze financial statements across IFRS, US GAAP, and Chinese accounting standards, producing ratio calculations, scoring, DuPont analysis, risk alerts, and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial analysts can use this skill to request structured financial statement analysis for company reporting, investment review, credit assessment, internal audit, and peer benchmarking. It is intended to return financial ratios, a composite score, fraud-risk signals, and practical recommendations from supplied statement data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill directs sensitive financial data and payment confirmation through an unsecured HTTP gateway. <br>
Mitigation: Do not submit real financial statements, payment credentials, or confidential business data unless the publisher provides an HTTPS endpoint with clear ownership, authentication, and payment validation details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/financial-analyzer-ai) <br>
- [Publisher profile](https://clawhub.ai/user/ai-gaoqian) <br>
- [Financial analyzer reference data](artifact/references/financial-analyzer.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with example shell commands and structured JSON analysis responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The documented basic tier returns JSON financial analysis after payment confirmation; PDF output is described as future reserved behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
