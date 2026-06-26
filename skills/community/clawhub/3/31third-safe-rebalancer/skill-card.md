## Description: <br>
Policy-aware Safe portfolio rebalancing assistant for 31Third ExecutorModule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Phips0812](https://clawhub.ai/user/Phips0812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Safe operators use this skill to monitor portfolio drift, generate policy-aware rebalance plans, validate trades, and execute approved batches through the 31Third ExecutorModule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real portfolio trades for the configured Safe. <br>
Mitigation: Install only for an intended Safe, use an executor wallet with limited authority, never provide the Safe owner private key, and run smoke, check-drift, and plan-only workflows before production execution. <br>
Risk: Portfolio planning data may be sent to 31Third. <br>
Mitigation: Review what portfolio data is shared with 31Third before enabling planning or automated rebalance workflows. <br>
Risk: Automatic rebalance execution may act without the level of human review expected for production treasury operations. <br>
Mitigation: Consider adding an operator confirmation step before enabling rebalance_now in production. <br>


## Reference(s): <br>
- [31Third homepage](https://31third.com) <br>
- [31Third Safe policy deployer](https://app.31third.com/safe-policy-deployer) <br>
- [ClawHub skill page](https://clawhub.ai/Phips0812/31third-safe-rebalancer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown guidance, CLI commands, and JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include rebalance plans, drift analysis, validation results, alert payloads, and transaction hashes.] <br>

## Skill Version(s): <br>
0.2.0 (source: package.json, skill.json, skill.yaml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
