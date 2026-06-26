## Description: <br>
Analyze historical impact of financial events on related assets. Kensho-style event-driven analysis. Use when: asking about asset reactions to events (oil surge, gold rise, rate hikes), historical precedent analysis, causal indicator relationships. Outputs Chinese reports and charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze how financial events have historically affected related assets, macro indicators, rates, monetary aggregates, and FX across multiple economies. It produces Chinese-language event analysis reports and charts for scenario comparison and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tushare token and may optionally use a FRED API key for financial data access. <br>
Mitigation: Provide credentials only through environment variables, confirm they are set without printing their values, and avoid pasting tokens into chat or logs. <br>
Risk: The skill fetches data from disclosed external financial data services. <br>
Mitigation: Confirm the intended data-service access is acceptable before installation and execution. <br>
Risk: Macro-economy coverage may be incomplete until the macro_indicators data-flow bug is fixed. <br>
Mitigation: Review outputs for missing macro indicators before relying on cross-economy conclusions. <br>
Risk: Font installation steps may require sudo privileges. <br>
Mitigation: Run sudo font-install commands only after explicit administrator review. <br>


## Reference(s): <br>
- [Indicator Mapping Reference](artifact/references/indicator_mapping.md) <br>
- [Chinese Report Template](artifact/references/report_template.md) <br>
- [Tushare Pro Registration](https://tushare.pro/register) <br>
- [FRED API Key Documentation](https://fred.stlouisfed.org/docs/api/api_key.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Chinese Markdown reports with JSON data files and PNG charts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local report artifacts under the workspace memory/reports directory and may display generated report text and charts in chat.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
