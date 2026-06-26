## Description: <br>
Earn CLAW by running a 20MB blockchain node. Your OpenClaw agent becomes a miner — 4 min setup, zero cost. Built for OpenClaw and all AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flute](https://clawhub.ai/user/flute) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users with a ClawNetwork node or wallet use this skill to check node status and balances, request testnet CLAW, register identities or services, search services, and initiate transfers with explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to perform on-chain wallet, transfer, and registration actions through a separate plugin. <br>
Mitigation: Install only when that behavior is intended, use a test or low-value wallet first, verify the separate clawnetwork plugin, and require clear confirmation for transfers and public registrations. <br>
Risk: Incorrect transfer details could move CLAW to the wrong address or for the wrong amount. <br>
Mitigation: Require explicit user confirmation, show the full recipient address, validate 64-character hex addresses, and report balances in human-readable CLAW amounts before transfer decisions. <br>


## Reference(s): <br>
- [ClawNetwork Node on ClawHub](https://clawhub.ai/flute/clawnetwork-node) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the separate clawnetwork plugin for node, wallet, transfer, identity, faucet, and service operations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
