## Description: <br>
One-step Safe rebalancer using on-chain 31Third policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Phips0812](https://clawhub.ai/user/Phips0812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to verify a 31Third Safe policy deployment and execute a one-step Safe rebalance from on-chain AssetUniverse, StaticAllocation, SlippagePolicy, and PriceOracle state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and broadcast live trades from a Safe through an executor private key, which can incur gas costs and move assets. <br>
Mitigation: Use a dedicated executor wallet with minimal permissions, never use the Safe owner key, verify deployed policies and slippage limits first, and require explicit human approval before each live rebalance. <br>
Risk: Incorrect or stale deployment configuration can cause failed or unintended rebalance execution. <br>
Mitigation: Run verify_deployment_config against the deployment troubleshooting summary and on-chain module state before enabling rebalance_now. <br>


## Reference(s): <br>
- [31Third Homepage](https://31third.com) <br>
- [31Third Safe Policy Deployer](https://app.31third.com/safe-policy-deployer) <br>
- [ClawHub Skill Page](https://clawhub.ai/Phips0812/31third-safe-rebalancer-simple) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [JSON tool results and Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [rebalance_now returns execution status, drift data, effective slippage values, and a transaction hash when executed; verify_deployment_config returns deployment checks, mismatches, warnings, and a summary message.] <br>

## Skill Version(s): <br>
0.2.0 (source: package.json, skill.yaml, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
