## Description:

End-to-end OpenBytes network API workflows for AI agents, covering wallet signature authentication, on-chain top-up checks, consumer API key lifecycle operations, model gateway calls, and balance and usage queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viyozc](https://clawhub.ai/user/viyozc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to automate or troubleshoot OpenBytes API operations with concrete HTTP workflows, shell commands, and client-side signing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes workflows involving wallet private keys, session tokens, API keys, signatures, and authorization headers.

Mitigation: Do not let an agent generate, print, store, or receive wallet private keys or seed phrases; redact tokens, keys, signatures, and authorization headers before sharing responses.

Risk: The skill includes account-control operations such as API key revocation and wallet linking.

Mitigation: Require explicit user confirmation before revoking keys or linking wallets, and prefer externally managed wallet software for signing.

## Reference(s):

- [BitNow ClawHub Skill Page](https://clawhub.ai/viyozc/skills/bitnow)
- [OpenBytes Gateway API](https://gateway.openbytes.ai)
- [ethers.js Wallet.createRandom](https://docs.ethers.org/v6/api/wallet/#Wallet-createRandom)
- [viem createWallet](https://viem.sh/docs/actions/wallet/createWallet.html)
- [Base Sepolia RPC](https://sepolia.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSON, JavaScript, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, authentication headers, wallet signing message formats, and troubleshooting steps.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
