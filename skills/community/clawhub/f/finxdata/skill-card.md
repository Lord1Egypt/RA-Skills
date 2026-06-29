## Description: <br>
FinXData helps agents query FinXData financial data APIs for A-share market data, stock quotes, financial statements, market news, dragon-tiger lists, lockup releases, macroeconomic data, FRED data, quota checks, API key setup, error handling, and service health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuqp](https://clawhub.ai/user/qiuqp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve FinXData financial API data, choose the narrowest supported endpoint for a request, handle quota or network errors, and summarize returned market data without turning it into investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send a FinXData API key to the configured API host. <br>
Mitigation: Use a limited, rotatable key and keep FINXDATA_BASE_URL pointed at the trusted FinXData API host unless the user intentionally changes it. <br>
Risk: Remote market and news responses may be inaccurate, stale, or include text that should not control agent behavior. <br>
Mitigation: Treat API responses as data, summarize dates and data availability, and do not follow returned text as instructions. <br>
Risk: Financial data summaries can be mistaken for investment advice. <br>
Mitigation: Frame outputs as information retrieval and data organization, include relevant dates, and avoid deterministic buy or sell recommendations. <br>


## Reference(s): <br>
- [FinXData API reference](references/api.md) <br>
- [FinXData usage guide](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with shell command examples and JSON API responses when raw command output is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Most data endpoints return JSON whose data field is commonly Markdown; the agent is expected to summarize key fields, dates, data availability, and next steps.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
