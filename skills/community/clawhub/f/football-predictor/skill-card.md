## Description: <br>
Football Predictor analyzes football match data, odds, and team signals to generate outcome predictions, confidence scores, risk scores, and betting-style recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warrenop](https://clawhub.ai/user/warrenop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this agent to request football match predictions, daily recommendations, prediction statistics, and learning updates. It is intended for sports analysis workflows and should not be treated as a verified betting or financial decision system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence says the skill presents betting predictions from mostly random mock data. <br>
Mitigation: Do not use recommendations for real betting or financial decisions unless verified live data sources are added and mock mode is clearly labeled. <br>
Risk: Security evidence notes under-disclosed persistence, broad tools, scheduling behavior, and optional external sharing. <br>
Mitigation: Review tool permissions, document required environment variables, and provide explicit controls for memory, scheduling, and EvoMap sharing before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/warrenop/football-predictor) <br>
- [Data sources reference](references/data-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON objects and concise text recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prediction outputs include match, predicted result, confidence, odds, recommendation, risk score, and key factors; statistics and learning commands return summary objects.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
