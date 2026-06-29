## Description: <br>
Monitor current Ethereum gas prices (Slow/Standard/Fast/Instant tiers) with Gwei values and estimated confirmation times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to check current Ethereum gas prices, assess network congestion, and configure simple threshold alerts before transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live network requests to public Ethereum gas APIs. <br>
Mitigation: Run it only where outbound network access to the disclosed endpoints is acceptable, and use endpoint allowlisting in locked-down environments. <br>
Risk: Automation that depends on alert results may behave incorrectly if the alert threshold or exit-code behavior is misunderstood. <br>
Mitigation: Test the alert threshold and exit-code behavior before relying on the skill in cron jobs or transaction workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fuzzyb33s/skills/gas-tracker) <br>
- [Ethereum PublicNode RPC](https://ethereum.publicnode.com) <br>
- [Blockscout Gas Oracle API](https://api.blockscout.com/api/v1/gasOracle) <br>
- [EthGas Info API](https://ethgas.info/api/ethgas) <br>
- [EthGas Watch API](https://api.ethgas.watch/api/gas) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [CLI text report or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports Slow, Standard, Fast, and Instant gas tiers with Gwei values, estimated confirmation times, source, block number, timestamp, base fee, status, and alert messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
