## Description: <br>
Sign and verify HTTP requests with Ethereum wallets using ERC-8128. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacopo-eth](https://clawhub.ai/user/jacopo-eth) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add wallet-signed HTTP authentication to APIs, agent workflows, and clients that need ERC-8128 request signing or verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys can be exposed if raw keys are passed on the command line, stored in shell history, or left in unencrypted files. <br>
Mitigation: Prefer encrypted keystores or dedicated low-value signing keys, and avoid passing raw private keys directly on the command line. <br>
Risk: Signed requests can authorize the wrong destination or payload if users sign without checking the request details. <br>
Mitigation: Verify the destination and payload before sending signed requests, keep signature TTLs short, and use nonce-based replay protection where appropriate. <br>
Risk: Installing from an unexpected package source can introduce untrusted signing or verification code. <br>
Mitigation: Install only from the expected @slicekit package source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacopo-eth/erc8128) <br>
- [ERC-8128 documentation](https://erc8128.slice.so) <br>
- [Quick Start](https://erc8128.slice.so/getting-started/quick-start) <br>
- [Request Binding](https://erc8128.slice.so/concepts/request-binding) <br>
- [Verifying Requests](https://erc8128.slice.so/guides/verifying-requests) <br>
- [CLI Guide](https://erc8128.slice.so/guides/cli) <br>
- [ERC-8128 Spec](https://github.com/slice-so/ERCs/blob/d9c6f41183008285a0e9f1af1d2aeac72e7a8fdc/ERCS/erc-8128.md) <br>
- [CLI Reference](references/cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes signing and verification patterns for the @slicekit/erc8128 library and erc8128 CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
