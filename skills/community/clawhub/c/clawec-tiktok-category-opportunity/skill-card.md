## Description: <br>
Uses the ClawEC API to analyze TikTok category and keyword opportunities, including opportunity scores, creator-sales trends, recent sales metrics, and radar-score breakdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and analysts use this skill to evaluate TikTok category or keyword opportunities by market, compare returned keyword candidates, and summarize sales, trend, and radar-score signals in Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live analysis sends TikTok research keywords, selected market codes, and the ClawEC API token to ClawEC. <br>
Mitigation: Keep the token in CLAWEC_API_KEY, avoid hardcoding credentials, and do not submit confidential business secrets as keywords unless ClawEC's data handling is acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anyunzhong/clawec-tiktok-category-opportunity) <br>
- [ClawEC API base](https://www.clawec.com/api) <br>
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub) <br>
- [Response schema](artifact/references/response-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables, trend summaries, radar-score interpretation, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs Chinese opportunity-analysis reports from ClawEC API responses; requires a CLAWEC_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
