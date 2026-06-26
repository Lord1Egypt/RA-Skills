## Description: <br>
Perform institutional-grade analysis of any US-listed stock using real-time and fundamental data from the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to research US-listed equities, compare valuation and financial-health signals, and generate structured buy, hold, avoid, or sell research reports. Outputs should be treated as analytical research rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key. <br>
Mitigation: Use a dedicated key with appropriate quota or billing controls, and rotate or revoke it if exposure is suspected. <br>
Risk: Ticker requests and related query context are sent to Finskills. <br>
Mitigation: Review Finskills privacy and retention terms before using the skill for confidential investment research. <br>
Risk: Generated ratings and price targets may be mistaken for financial advice. <br>
Mitigation: Treat reports as research output, review assumptions and source data, and avoid using the skill to make unsupervised trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/finskills-us-stock-analyzer) <br>
- [Source homepage](https://github.com/finskills/us-stock-analyzer) <br>
- [Finskills API](https://finskills.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Structured Markdown investment research report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and a US-listed ticker; report completeness depends on requested depth and available Finskills API data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
