## Description: <br>
End-to-end OpenBytes network API workflows for AI agents covering wallet signature authentication, on-chain top-up monitoring, consumer API key lifecycle management, model gateway API calls, balance queries, and usage queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viyozc](https://clawhub.ai/user/viyozc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate and troubleshoot OpenBytes network operations through direct API interaction, including wallet-based authentication, API key management, deposits, balance checks, usage checks, and model gateway calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes wallet and credential workflows where private keys, API keys, session tokens, signatures, or Authorization headers could be exposed in generated commands or troubleshooting output. <br>
Mitigation: Do not let an agent generate, display, store, or paste wallet private keys or seed phrases; redact Authorization headers, API keys, session tokens, signatures, and secret fields before sharing responses. <br>
Risk: The skill guides on-chain deposits and wallet linking, where incorrect gateway, chain, token, or contract details could cause funds or account relationships to be misdirected. <br>
Mitigation: Manually verify the gateway, chain ID, token address, contract address, and wallet-linking message before approving deposits or linking wallets. <br>


## Reference(s): <br>
- [BitNow ClawHub Skill Page](https://clawhub.ai/viyozc/bitnow) <br>
- [OpenBytes Gateway API Base URL](https://gateway.openbytes.ai) <br>
- [ethers.js Wallet.createRandom Documentation](https://docs.ethers.org/v6/api/wallet/#Wallet-createRandom) <br>
- [viem createWallet Documentation](https://viem.sh/docs/actions/wallet/createWallet.html) <br>
- [Base Sepolia RPC Endpoint](https://sepolia.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell, JavaScript, TypeScript, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user-supplied placeholders for wallet addresses, tokens, API keys, timestamps, endpoint URLs, and transaction details.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
