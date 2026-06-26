## Description: <br>
A financial comparable-company analysis skill for A-share listed companies that compares a target company with peers across operating, financial, valuation, and benchmark metrics and generates a themed Excel report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts, investment researchers, and agents use this skill to compare one identifiable A-share listed company against peer companies across operating, financial, and valuation dimensions. It is intended for screening, fundamental analysis, valuation comparison, and business-context explanation, with outputs treated as reference material rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires EM_API_KEY and sends company queries to Eastmoney's comparable-company API. <br>
Mitigation: Install only when use of that API is intended, keep EM_API_KEY out of code and logs, and avoid submitting sensitive analysis questions unless the data-sharing posture is acceptable. <br>
Risk: The data-fetch script can print full API response data during debug runs. <br>
Mitigation: Avoid running debug fetches in shared logs, notebooks, or terminals when analysis inputs or API responses are sensitive. <br>
Risk: Financial analysis outputs may be incomplete or unsuitable for unsupported companies, multi-entity inputs, or thin peer sets. <br>
Mitigation: Use only for single identifiable A-share listed companies, preserve API error messages, and do not fabricate conclusions when the API fails or comparable-company statistics are weak. <br>
Risk: The generated comparison and explanations could be mistaken for investment advice. <br>
Mitigation: Present results as reference material and require human review before investment, merger, or valuation decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/comparable-company-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/financial-ai-analyst) <br>
- [Eastmoney MXClaw registration](https://ai.eastmoney.com/mxClaw) <br>
- [Eastmoney comparable-company API endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/comparable-company-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown financial analysis plus a local .xlsx comparable-company report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY, sends single-company queries to Eastmoney, and writes Excel files under miaoxiang/comparable_company_analysis by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
