## Description: <br>
Estimates first-year value for one major-US credit card by combining welcome bonus value, annual earn, statement credits, and annual fee, with optional user-provided spending details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahongc](https://clawhub.ai/user/jiahongc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this agent skill to estimate the first-year value of a specific major-US credit card, including welcome bonus, annual earn, statement credits, annual fee, and confidence notes from issuer-first research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credit-card offers, fees, point valuations, and statement credits can change or conflict across sources. <br>
Mitigation: Use issuer-first research, cite fetched sources, flag uncertain claims, and treat the result as an estimate rather than financial advice. <br>
Risk: User prompts may include unnecessary personal financial details. <br>
Mitigation: Use spending categories and approximate amounts only; avoid account numbers and other sensitive personal financial information. <br>
Risk: Optional Brave Search use requires a search API key when configured. <br>
Mitigation: Provide BRAVE_API_KEY only in trusted environments and fall back to built-in web search when the key or curl is unavailable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jiahongc/card-value) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Condensed Markdown report with spend profile, welcome bonus, annual earn, credits, net first-year value, confidence notes, and sources.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses current web lookups; optional Brave Search API key and curl support may be used when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
