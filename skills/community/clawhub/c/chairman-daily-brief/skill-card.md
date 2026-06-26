## Description: <br>
Generates morning and evening executive market briefings for listed-company chairmen, covering price movements, policy updates, competitor intelligence, capital-market sentiment, and regulatory announcement alerts using QVeris data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buxibuxi](https://clawhub.ai/user/buxibuxi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External executives and their support teams use this skill to generate daily pre-market and post-market briefings for monitored public companies, competitors, policies, announcements, and market sentiment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store holdings and competitor watchlists locally. <br>
Mitigation: Review local watchlist contents before use and avoid storing sensitive holdings or competitor monitoring data in shared environments. <br>
Risk: Generated market, quote, or policy information may include simulated data or otherwise appear more authoritative than the available source evidence supports. <br>
Mitigation: Verify important financial, policy, and strategic claims against live labeled data sources before making financial or strategic decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buxibuxi/chairman-daily-brief) <br>
- [QVeris homepage](https://qveris.ai) <br>
- [Tool chain routing reference](references/tool-chains.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing reports with supporting shell commands and JSON watchlist configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Morning and evening report modes can target a single company, competitors, or a saved watchlist.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
