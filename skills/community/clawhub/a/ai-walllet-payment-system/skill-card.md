## Description: <br>
Manage Ethereum wallets with encrypted key storage, TOTP authentication, ETH transactions, audit logging, and rate limiting for AI-driven payment workflows. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders can use this skill as an experimental reference for creating Ethereum wallets, checking balances, and preparing ETH transfers with local key protection and human authentication controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle wallet recovery material and authentication secrets. <br>
Mitigation: Keep TOTP seeds, backup codes, private keys, and wallet exports out of chat and logs; store them only in a dedicated password manager or encrypted local vault. <br>
Risk: The skill can send irreversible ETH transactions. <br>
Mitigation: Use testnets or unfunded wallets by default, and require explicit human approval, recipient review, and amount limits before any transaction is broadcast. <br>
Risk: The artifact makes security claims that evidence says are not fully supported. <br>
Mitigation: Treat it as experimental wallet software and require independent security audit before using it with production funds or mainnet assets. <br>


## Reference(s): <br>
- [Web3.py Documentation](https://web3py.readthedocs.io/) <br>
- [Ethereum Developer Documentation](https://ethereum.org/en/developers/docs/) <br>
- [Argon2 Specification](https://github.com/P-H-C/phc-winner-argon2) <br>
- [TOTP RFC 6238](https://tools.ietf.org/html/rfc6238) <br>
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) <br>
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet setup steps, environment configuration, security guidance, and transaction workflow examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
