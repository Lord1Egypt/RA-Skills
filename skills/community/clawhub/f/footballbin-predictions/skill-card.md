## Description: <br>
Get AI-powered match predictions for Premier League and Champions League including scores, next goal, and corners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billychl1](https://clawhub.ai/user/billychl1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to fetch FootballBin match predictions for Premier League and Champions League matches, with optional matchweek and team filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Football query choices are sent to the FootballBin API. <br>
Mitigation: Use the skill only when sharing league, matchweek, and team filter choices with that API is acceptable. <br>
Risk: Prediction data can be incorrect or incomplete. <br>
Mitigation: Treat returned predictions as informational output and verify important decisions against authoritative football data sources. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/billychl1/footballbin-predictions) <br>
- [FootballBin iOS App](https://apps.apple.com/app/footballbin/id6757111871) <br>
- [FootballBin Android App](https://play.google.com/store/apps/details?id=com.achan.footballbinandroid) <br>
- [FootballBin MCP API Endpoint](https://api.footballbin.achaninc.net/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output, or raw JSON when jq is unavailable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; sends league, optional matchweek, and optional team filters to the FootballBin API.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
