## Description: <br>
Implement quantum-resistant encryption using the CIFER SDK (cifer-sdk npm package). Covers SDK initialization, wallet setup, secret creation, text encryption/decryption, and file encryption/decryption on any supported chain (Ethereum, Sepolia, Ternoa). Use when the user mentions CIFER, cifer-sdk, quantum-resistant encryption, ML-KEM, secret creation, or encrypted payloads/files with blockchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TIP-citron](https://clawhub.ai/user/TIP-citron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to integrate the CIFER SDK for wallet-backed secret creation, text encryption/decryption, and file encryption/decryption across supported Ethereum, Sepolia, and Ternoa chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys or signing credentials could be exposed while following integration examples. <br>
Mitigation: Use test or low-balance wallets, keep private keys out of chat, logs, client code, and source control, and prefer server-side signing where appropriate. <br>
Risk: Creating secrets or sending transactions can incur blockchain fees on the selected chain. <br>
Mitigation: Confirm the chain, balance, and fee details before sending transactions, and query the secret creation fee before execution. <br>
Risk: File encryption and decryption depend on the configured CIFER blackbox remote service and local output paths. <br>
Mitigation: Avoid uploading confidential files unless the remote service is trusted, and choose safe local output paths for downloaded encrypted or decrypted files. <br>


## Reference(s): <br>
- [CIFER SDK API reference](reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/TIP-citron/cifer-security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include wallet, chain, RPC, blackbox service, file path, and encryption job settings.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
