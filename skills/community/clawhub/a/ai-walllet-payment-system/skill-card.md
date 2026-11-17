## Description:

Manage Ethereum wallets with encrypted keys, TOTP 2FA, secure ETH transactions, audit logs, and rate limiting for AI-driven payment processing.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[cerbug45](https://clawhub.ai/user/cerbug45)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent builders can use this demonstration skill to prototype Ethereum wallet creation, encrypted key storage, TOTP-gated ETH transactions, and payment workflow integration in isolated or testnet environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real cryptocurrency wallets and transactions, so implementation mistakes or unsafe execution could lead to fund loss.

Mitigation: Do not use it for production, mainnet, or meaningful funds unless the transaction flow, key recovery design, dependency pins, and documentation are independently audited.

Risk: Generated wallets may become unrecoverable if MFA secrets, backup codes, passwords, or encrypted backups are lost or mishandled.

Mitigation: Test recovery paths with testnet-only funds and store MFA secrets, backup codes, and backup passwords in an offline or otherwise trusted secret-management system.

Risk: Security claims in the artifact exceed the implementation and may create false confidence around hardware security, recovery, and advanced cryptographic protections.

Mitigation: Treat unsupported security claims as unverified and review HSM behavior, dependency pins, recovery design, and documentation before any deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cerbug45/skills/ai-walllet-payment-system)
- [Web3.py documentation](https://web3py.readthedocs.io/)
- [Ethereum developer documentation](https://ethereum.org/en/developers/docs/)
- [Argon2 specification](https://github.com/P-H-C/phc-winner-argon2)
- [TOTP RFC 6238](https://tools.ietf.org/html/rfc6238)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, configuration examples, and Python dictionary results from wallet API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Python environment, configured Web3 provider, SQLCipher dependencies, and secure handling of wallet secrets before execution.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
