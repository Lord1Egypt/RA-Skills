## Description: <br>
Set up and start mining AGENT tokens on Base L2 using apow-cli. Easy Mode uses x402 for RPC, LLM, and GPU grinding with no config beyond wallet funding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentoshi](https://clawhub.ai/user/agentoshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure apow-cli, fund a fresh Base wallet, mint a Mining Rig NFT, and start or monitor AGENT token mining. It supports Easy Mode x402 setup and advanced manual configuration with RPC, LLM, wallet, and grinder options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to create or export wallet private keys and operate a funded crypto wallet. <br>
Mitigation: Use a fresh, low-balance hot wallet only; avoid main wallets and require explicit approval before any key export or wallet-funded action. <br>
Risk: The skill can initiate paid x402 services, bridge or swap flows, minting, and mining loops that spend ETH or USDC. <br>
Mitigation: Require explicit approval before bridge, swap, mint, mining loop, or paid x402 operations, and keep balances limited to the intended experiment. <br>
Risk: The skill may handle plaintext wallet import helpers or scan local wallet files during dashboard setup. <br>
Mitigation: Prefer encrypted keystore backups, avoid plaintext private-key storage when possible, and approve dashboard scans only for intended directories. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/agentoshi/apow-mining) <br>
- [APoW CLI](https://github.com/Agentoshi/apow-cli) <br>
- [APoW Core](https://github.com/Agentoshi/apow-core) <br>
- [APoW Grind](https://github.com/Agentoshi/apow-grind) <br>
- [x402 payment protocol](https://www.x402.org/) <br>
- [Squid Router](https://squidrouter.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands and environment variable snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user-facing funding handoff guidance and local configuration snippets.] <br>

## Skill Version(s): <br>
0.4.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
