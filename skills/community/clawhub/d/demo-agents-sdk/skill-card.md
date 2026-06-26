## Description: <br>
Complete Polygon agent toolkit for session-based smart contract wallets, token operations, ERC-8004 on-chain identity and reputation, and x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesLawton](https://clawhub.ai/user/JamesLawton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up Polygon Agent Kit wallets, configure session permissions, register agents on-chain, and prepare token operation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real wallet authority and can prepare commands that broadcast transactions. <br>
Mitigation: Use a new low-value wallet, set narrow session spending limits, and manually review every command that uses --broadcast. <br>
Risk: The release relies on unpinned external code and an auto-downloaded tunnel binary. <br>
Mitigation: Review the external Polygon Agent Kit repository and the cloudflared download source before installing or running the tunnel flow. <br>
Risk: Wallet approval URLs, private keys, and temporary session files may expose sensitive wallet material if retained or shared incorrectly. <br>
Mitigation: Keep private keys and approval URLs out of logs and chats, avoid sensitive environments for the tunnel flow, and remove any /tmp session files after use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JamesLawton/demo-agents-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples and configuration tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup flow, environment variables, transaction command examples, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
