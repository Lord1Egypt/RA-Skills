## Description: <br>
Helps agents build and run complete OKX DEX Aggregator swap flows, including swap calldata retrieval, transaction signing support, ERC-20 approval handling, and signed transaction broadcast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AaronLLee](https://clawhub.ai/user/AaronLLee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to generate code and guidance for token-to-token swaps through the OKX DEX Aggregator API, including approval, signing, MEV protection, and broadcast steps. It is intended for workflows where users explicitly want help preparing real on-chain swap transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help use wallet and API secrets to approve, sign, and submit real on-chain swap transactions without a required confirmation checkpoint. <br>
Mitigation: Prefer an external wallet or hardware signer, use least-privilege OKX API credentials, require manual confirmation before every approval, signing, and broadcast step, approve exact amounts when possible, and revoke unused allowances after swaps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AaronLLee/easy-swap) <br>
- [OKX DEX Aggregator Swap API](https://web3.okx.com/api/v6/dex/aggregator/swap) <br>
- [OKX DEX Broadcast Transaction API](https://web3.okx.com/api/v6/dex/pre-transaction/broadcast-transaction) <br>
- [OKX Web3 API base](https://web3.okx.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code examples, API parameters, configuration guidance, and shell commands where needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Python or Node.js examples for OKX API signing, swap calldata retrieval, approval handling, transaction broadcast, and verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
