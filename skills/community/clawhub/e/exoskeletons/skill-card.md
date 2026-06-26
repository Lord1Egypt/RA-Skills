## Description: <br>
Mint and manage onchain AI agent identity NFTs on Base with visual identity, messaging, storage, reputation, upgradeable modules, and optional wallet features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Potdealer](https://clawhub.ai/user/Potdealer) <br>

### License/Terms of Use: <br>
CC0 <br>


## Use Case: <br>
Developers and agent operators use this skill to read Exoskeleton identity state and prepare transactions for minting, messaging, storage, modules, escrow, and wallet-related actions on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare or submit onchain transactions through Bankr examples. <br>
Mitigation: Review transaction contents before broadcast and install only when onchain Exoskeleton transaction workflows are intended. <br>
Risk: BANKR_API_KEY is sensitive and may authorize transaction submission. <br>
Mitigation: Keep BANKR_API_KEY out of logs and command history, and prefer a dedicated limited-funds wallet or scoped key. <br>
Risk: Messages and storage written onchain are public and permanent. <br>
Mitigation: Avoid writing secrets or private data to onchain messages or storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Potdealer/exoskeletons) <br>
- [Exoskeletons website](https://exoagent.xyz) <br>
- [The Board](https://exoagent.xyz/board) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and Bankr-compatible transaction JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include transaction payloads for Base; users should review before broadcast.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
