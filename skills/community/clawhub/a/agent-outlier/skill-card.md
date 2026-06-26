## Description: <br>
Agent Outlier helps an agent check arena status, view rounds, claim winnings, and interact with an onchain reflexive beauty contest game on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[potdealer](https://clawhub.ai/user/potdealer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to inspect Agent Outlier rounds and have an agent operate a dedicated wallet for commits, reveals, finalization, and claims in the Base mainnet game. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for a private key to sign on-chain game transactions. <br>
Mitigation: Use a dedicated low-balance wallet, never a primary wallet private key, and review the SDK before funding the wallet. <br>
Risk: The skill can participate in a real-money on-chain game with entry fees and gas costs. <br>
Mitigation: Confirm the tier, round, entry fee, and gas cost before play; use the free training tier or lowest-cost tier when testing. <br>
Risk: The artifact includes a continuous-play example that could create repeated spending. <br>
Mitigation: Avoid continuous play unless explicit round, time, and spend limits are set before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/potdealer/agent-outlier) <br>
- [Agent Outlier Game](https://exoagent.xyz/outlier) <br>
- [Exoskeletons](https://exoagent.xyz) <br>
- [V1 Contract on Basescan](https://basescan.org/address/0x8F7403D5809Dd7245dF268ab9D596B3299A84B5C) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, and PRIVATE_KEY; wallet actions may sign Base mainnet transactions.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
