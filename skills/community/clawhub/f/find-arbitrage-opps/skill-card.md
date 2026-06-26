## Description: <br>
Find arbitrage opportunities across exchanges by comparing prices for fungible token pairs like BTC/WBTC and USDT/USDC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengtality](https://clawhub.ai/user/fengtality) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading automation operators use this skill to compare fungible token prices across Hummingbot-connected exchanges and identify potential buy-low, sell-high arbitrage opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The prerequisite step runs a remote shell script before use. <br>
Mitigation: Inspect the remote prerequisite script before running it and execute it only in a trusted environment. <br>
Risk: The script uses Hummingbot API credentials and documented defaults may be weak. <br>
Mitigation: Use a strong API password, keep the Hummingbot API bound to localhost or HTTPS on a trusted network, and run from a directory where the .env fallback cannot pick up unrelated secrets. <br>


## Reference(s): <br>
- [Find Arbitrage Opps on ClawHub](https://clawhub.ai/fengtality/find-arbitrage-opps) <br>
- [Hummingbot prerequisite script](https://raw.githubusercontent.com/hummingbot/skills/main/skills/lp-agent/scripts/check_prerequisites.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; script output is plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted Hummingbot API with configured exchange connectors; supports connector filters, minimum spread filtering, and optional JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
