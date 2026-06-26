## Description: <br>
Read-only Api3 feed discovery, readiness, coverage, and purchase-planning skill for downstream agent projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daav3](https://clawhub.ai/user/daav3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover or verify API3 decentralized data feeds, inspect readiness and runway state, and prepare reviewable activation or contract-call plans without giving the skill signer authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated calldata, browser plans, contract addresses, values, or pricing outputs could be wrong for the intended chain or stale by the time they are used. <br>
Mitigation: Verify every generated detail against trusted API3 sources and the intended chain before passing it to a wallet, browser flow, or separate executor. <br>
Risk: Users may confuse planning output with authority to execute or with completed funding. <br>
Mitigation: Treat plans and calldata as review material only, and require a fresh post-action check before claiming that a feed was funded or activated. <br>
Risk: Supplying private keys or seed phrases would create unnecessary credential exposure for a read-only planning tool. <br>
Mitigation: Do not provide signer material; use a separate wallet or executor for any transaction after human review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daav3/api3-feed-manager-readonly) <br>
- [Publisher Profile](https://clawhub.ai/user/daav3) <br>
- [Project Homepage](https://github.com/daav3/agentic-lending-project) <br>
- [API3 Market](https://market.api3.org) <br>
- [API3 Market Pricing Data](https://api3dao.github.io/data-feeds/market/dapi-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON or CSV CLI output with reviewable transaction call details, calldata, browser plans, and diagnostics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output; the skill does not accept signer material or submit transactions.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
