## Description: <br>
Fetches real-time and historical Chinese A-share market data, including quotes, financial reports, capital flows, and fundamental indicators using AkShare. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GBABYZS](https://clawhub.ai/user/GBABYZS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial-analysis agents use this skill to fetch Chinese A-share quotes, historical prices, financial statements, capital-flow data, and fundamental indicators for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The declared Python implementation file is missing from the artifact. <br>
Mitigation: Confirm the source and contents of skill_main.py before installing or executing the skill. <br>
Risk: Financial data may be delayed, rate limited, or unsuitable as the only basis for financial decisions. <br>
Mitigation: Validate outputs against authoritative data sources, throttle requests, and use caching where repeated queries are expected. <br>
Risk: The skill depends on external Python packages and upstream market-data services. <br>
Mitigation: Install in an isolated Python environment and review or pin AkShare-related dependencies before use. <br>


## Reference(s): <br>
- [Finance Data Fetcher on ClawHub](https://clawhub.ai/GBABYZS/finance-data-fetcher) <br>
- [GBABYZS publisher profile](https://clawhub.ai/user/GBABYZS) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, API Calls] <br>
**Output Format:** [Python function results containing market quotes, financial reports, capital-flow data, and fundamental indicators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on AkShare and upstream financial data APIs; real-time quotes may be delayed and APIs may be rate limited.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
