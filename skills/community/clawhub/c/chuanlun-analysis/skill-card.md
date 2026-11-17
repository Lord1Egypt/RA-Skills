## Description:

Uses ChanLun Theory to analyze stocks and generate technical analysis visualizations.

This skill is for research and development only.

## Publisher:

[silverfoxchina-gif](https://clawhub.ai/user/silverfoxchina-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to run ChanLun technical analysis on supported A-share, Hong Kong, and U.S. stocks, producing reports and charts for review. The analysis is educational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock names or codes submitted for analysis may be sent to external market-data services.

Mitigation: Use the skill with non-sensitive ticker queries, disclose external data access to users, and run it only when network access to the market-data services is acceptable.

Risk: Generated market reports can be mistaken for investment advice.

Mitigation: Present outputs as educational technical analysis, retain the not-investment-advice disclaimer, and require human review before any trading decision.

Risk: The skill installs and runs Python dependencies and writes local report/chart files.

Mitigation: Install dependencies in a dedicated virtual environment, avoid elevated privileges, and direct outputs to an expected workspace path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silverfoxchina-gif/skills/chuanlun-analysis)
- [Referenced original ClawHub ChanLun skill](https://clawhub.ai/laigen/chanlun-technical-analysis)
- [Indicator reference for stroke recognition](https://github.com/neuks/Indicator)
- [czsc_in_practise reference for segment recognition](https://github.com/jiapengwei/czsc_in_practise)
- [Tencent A-share K-line API endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get)
- [Tencent Hong Kong stock K-line API endpoint](https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get)
- [Tencent U.S. stock K-line API endpoint](https://web.ifzq.gtimg.cn/appstock/app/usfqkline/get)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON summaries, PNG charts, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local report and chart files; optional JSON can be printed to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
