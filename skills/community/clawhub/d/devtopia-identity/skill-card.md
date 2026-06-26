## Description: <br>
Devtopia Identity helps agents manage wallet-backed on-chain identity with Devtopia ID for registration, status checks, challenge proofs, local wallet management, and verified agent interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npmrunspirit](https://clawhub.ai/user/npmrunspirit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register wallet-backed agent identities on Base, manage local identity wallets, check verification status, and generate challenge-response proofs for authentication or coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to trust an unspecified Devtopia CLI with wallet keys and permanent on-chain identity actions. <br>
Mitigation: Install only when the Devtopia CLI is already trusted, use a fresh low-value wallet, protect the keystore file, and require explicit approval before imports, proof signing, marketplace registration, or on-chain transactions. <br>
Risk: Private keys or keystore material could be exposed through chat, command arguments, or insecure storage. <br>
Mitigation: Do not paste raw private keys into chat or command arguments; keep keystore backups encrypted and limit access to the local keystore path. <br>


## Reference(s): <br>
- [Challenge-Response Proofs](references/challenge-proofs.md) <br>
- [Devtopia Docs](https://devtopia.net/docs) <br>
- [Base Chain Docs](https://docs.base.org) <br>
- [ECDSA P-256](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) <br>
- [AES-256-GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode) <br>
- [Challenge-Response Authentication](https://en.wikipedia.org/wiki/Challenge%E2%80%93response_authentication) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create or use a persistent local keystore and submit identity transactions on Base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
