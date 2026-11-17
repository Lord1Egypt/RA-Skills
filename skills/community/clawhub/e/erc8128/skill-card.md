## Description:

Sign and verify HTTP requests with Ethereum wallets using ERC-8128 for wallet-based API authentication, signed ERC-8128 endpoint requests, server-side request verification, and agent-to-server authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacopo-eth](https://clawhub.ai/user/jacopo-eth)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement wallet-signed HTTP authentication for APIs, agents, and servers that need ERC-8128 request signing, verification, replay protection, and request integrity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global npm installs or npx execution can run package code that has not been reviewed for the deployment.

Mitigation: Pin @slicekit/erc8128-cli to a reviewed version, install it project-locally with a lockfile, and run it with least privilege.

Risk: The workflow handles Ethereum signing keys, including raw private keys, key files, and ETH_PRIVATE_KEY.

Mitigation: Prefer encrypted keystores, hardware wallets, or a signing service; avoid raw private keys and ETH_PRIVATE_KEY for production use.

Risk: Signed requests sent to untrusted endpoints or written to careless output paths may expose sensitive request or response data.

Mitigation: Sign only requests to trusted HTTPS endpoints and choose output paths intentionally, especially when responses may contain sensitive data.

## Reference(s):

- [ERC-8128 documentation](https://erc8128.slice.so)
- [CLI reference](references/cli.md)
- [Quick Start](https://erc8128.slice.so/getting-started/quick-start)
- [Request Binding](https://erc8128.slice.so/concepts/request-binding)
- [Verifying Requests](https://erc8128.slice.so/guides/verifying-requests)
- [VerifyPolicy API Reference](https://erc8128.slice.so/api/types#verifypolicy)
- [VerifyFailReason API Reference](https://erc8128.slice.so/api/types#verifyfailreason)
- [ERC-8128 Specification](https://github.com/slice-so/ERCs/blob/d9c6f41183008285a0e9f1af1d2aeac72e7a8fdc/ERCS/erc-8128.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
