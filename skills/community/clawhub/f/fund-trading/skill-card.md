## Description: <br>
Fund Trading Clawhub provides simulated fund trading commands for account management, fund lookup, subscriptions, redemptions, holdings, and order queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weitom0902](https://clawhub.ai/user/weitom0902) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance-learning users use this skill to run virtual-money fund trading workflows while viewing real fund net values and market data. Typical tasks include registering a simulated account, querying funds and holdings, and issuing simulated subscribe, redeem, or cancel commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags ambiguity about whether trading actions can affect real money and which API endpoint the installed command will use. <br>
Mitigation: Install only after confirming the workflow is strictly virtual-money sandbox trading and verify the effective API endpoint before running subscribe, redeem, or cancel commands. <br>
Risk: The skill stores account configuration, client credentials, and access tokens locally and may print sensitive account details during registration. <br>
Mitigation: Treat local config and console output as sensitive, avoid committing or sharing them, and review terminal output before copying it into logs or tickets. <br>
Risk: Financial command names can create accidental high-impact actions if a user misunderstands the simulated trading boundary. <br>
Mitigation: Require explicit user approval before running subscribe, redeem, or cancel commands and keep the important virtual-money disclaimer visible in operator guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weitom0902/fund-trading) <br>
- [PyPI package](https://pypi.org/project/fund-trading-skill/) <br>
- [npm package](https://www.npmjs.com/package/fund-trading-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with CLI commands and terminal-style text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an API endpoint setting identified by OPENAPI_URL in ClawHub metadata; local account configuration and tokens should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
