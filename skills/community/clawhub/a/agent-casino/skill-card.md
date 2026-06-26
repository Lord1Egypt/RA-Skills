## Description: <br>
On-chain Rock-Paper-Scissors on Base Mainnet with real USDC, using a commit-reveal mechanism, 80/20 anti-bankruptcy payout, and zero rake. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemodigital](https://clawhub.ai/user/lemodigital) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agents use this skill to inspect, create, join, reveal, and settle on-chain Rock-Paper-Scissors games with real USDC on Base Mainnet. It is intended for users who deliberately want an agent workflow around a real-money blockchain game and can review wallet transactions before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports a real-money USDC game and asks agents to work with wallet transactions on Base Mainnet. <br>
Mitigation: Install only when this behavior is intentional; use a dedicated low-balance wallet and accept that signed blockchain transactions are irreversible. <br>
Risk: The remote casino API prepares transaction data that an agent or user may sign. <br>
Mitigation: Manually verify every transaction destination, calldata, approval, and amount before signing, and avoid broad approvals. <br>
Risk: The workflow depends on game-secret salt values and a remote API that must be trusted with transaction preparation and game-secret information. <br>
Mitigation: Keep salt values secret until reveal, preserve them for the full game flow, and avoid using the skill if the remote service trust requirement is unacceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lemodigital/agent-casino) <br>
- [Agent Casino API](https://casino.lemomo.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON transaction data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces unsigned transaction targets and calldata that must be manually verified, signed, and broadcast with the user's own wallet.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
