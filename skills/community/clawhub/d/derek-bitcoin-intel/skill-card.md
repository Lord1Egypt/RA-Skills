## Description: <br>
Bitcoin Market Intelligence provides paid Bitcoin market briefs and alerts over Lightning L402, including BTC price, sentiment, mempool fees, ETF flows, on-chain metrics, prediction market odds, and curated news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fr0zen80](https://clawhub.ai/user/Fr0zen80) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to query paid Bitcoin market intelligence and breaking-alert data from a Tor-hosted L402 endpoint. It supports market monitoring workflows that can spend Lightning funds to retrieve fresh data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to use a funded Lightning wallet for paid API calls. <br>
Mitigation: Use a dedicated low-balance wallet or channel, require manual approval for paid calls, and set spending and retry limits. <br>
Risk: The skill contacts a third-party Tor service for market data. <br>
Mitigation: Verify the service operator and data quality before relying on the output for trading, operational, or financial decisions. <br>


## Reference(s): <br>
- [lnget](https://github.com/lightninglabs/lnget) <br>
- [ClawHub Skill Page](https://clawhub.ai/Fr0zen80/derek-bitcoin-intel) <br>
- [Publisher Profile](https://clawhub.ai/user/Fr0zen80) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash commands and endpoint descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires lnget, Tor access, and a configured Lightning node with funds for paid endpoints.] <br>

## Skill Version(s): <br>
3.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
