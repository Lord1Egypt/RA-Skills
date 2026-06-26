## Description: <br>
BOB is an Agentic Proof of Work NFT minting skill on Base where an agent solves puzzles, signs locally, and submits signed mint transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tron04736-star](https://clawhub.ai/user/tron04736-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use BOB to mint NFTs on Base by solving API-provided puzzles, signing returned transactions locally, and submitting the signed transactions to the BOB API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to handle raw EVM private keys. <br>
Mitigation: Use a fresh burner wallet funded only with the mint price and gas; never use a main wallet private key. <br>
Risk: The skill signs server-provided transaction data. <br>
Mitigation: Before signing, verify the contract address, Base chain ID 8453, transaction value, calldata, and recipient. <br>
Risk: API responses include agentHint text that could steer agent behavior. <br>
Mitigation: Treat agentHint values as untrusted data and do not follow them as instructions without independent user review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tron04736-star/bob) <br>
- [BOB homepage](https://www.bobsmint.xyz) <br>
- [BOB API base](https://www.bobsmint.xyz/api) <br>
- [Published skill file](https://www.bobsmint.xyz/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, JSON] <br>
**Output Format:** [Markdown with inline shell, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces step-by-step minting guidance and local signing code; responses may include API result summaries and transaction details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
