## Description: <br>
FXAI helps an agent create V5 tokens on BSC with optional USDT or BNB pools, upload token metadata, and prepare USDT or BNB buy and sell actions through BNB Chain MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NathanThoreaurl](https://clawhub.ai/user/NathanThoreaurl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and token operators use this skill to guide token creation and trading workflows on BNB Smart Chain. It is intended for users who can configure BNB Chain MCP and manage a wallet key for transaction signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help approve token spending and execute irreversible BSC transactions from a wallet configured in BNB Chain MCP. <br>
Mitigation: Use a dedicated low-balance wallet, avoid using a main wallet PRIVATE_KEY, verify the contract address and MCP package, and require explicit human confirmation before every approval, token creation, buy, or sell. <br>
Risk: The metadata upload helper reads a local image and publishes that file plus token metadata to the Flap upload API. <br>
Mitigation: Run the helper only with files and metadata intended for publication, and review image paths, descriptions, and links before upload. <br>


## Reference(s): <br>
- [FXAI contract ABI](references/contract-abi.md) <br>
- [BNB Chain MCP skills documentation](https://docs.bnbchain.org/showcase/mcp/skills/) <br>
- [Flap token launcher guide](https://docs.flap.sh/flap/developers/token-launcher-developers/launch-token-through-portal) <br>
- [Flap deployed contract addresses](https://docs.flap.sh/flap/developers/token-launcher-developers/deployed-contract-addresses) <br>
- [ClawHub skill page](https://clawhub.ai/NathanThoreaurl/fxai-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands, contract parameters, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include contract addresses, ABI references, MCP write_contract parameters, and token metadata upload commands.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
