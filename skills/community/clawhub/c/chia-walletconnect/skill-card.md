## Description:

Telegram Web App for Chia wallet verification via WalletConnect and Sage. Enables cryptographic proof of wallet ownership through signature verification using MintGarden API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect a Sage wallet in Telegram, sign a challenge, and verify Chia wallet ownership for gated groups, airdrop eligibility, authentication, DAO voting, or proof-of-holdings workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-to-Telegram binding may be unsafe if challenges are generated or accepted without server-side state, single-use nonces, and strict timestamp handling.

Mitigation: Generate and store challenges server-side, make nonces single-use, reject future or expired timestamps, and bind each challenge to the expected Telegram user before granting access.

Risk: Telegram identity can be spoofed or misbound if Web App initData is not verified.

Mitigation: Verify Telegram Web App initData on the server before accepting wallet signatures or linking a wallet address to a Telegram account.

Risk: Verification endpoints and status lookups can expose or modify sensitive verification state if unauthenticated.

Mitigation: Authenticate status and verification endpoints, add rate limits, restrict CORS to the deployed domain, and avoid using the skill for access control until these controls are in place.

Risk: Wallet addresses, signatures, public keys, and Telegram identifiers may create privacy exposure when logged or sent to external verification services.

Mitigation: Minimize sensitive logging, disclose that MintGarden receives verification material, and clearly tell users when their Telegram identity may be linked with wallet data.

Risk: Remote frontend dependencies or outdated packages can weaken the verification flow.

Mitigation: Bundle or integrity-pin remote scripts and update dependency issues before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/koba42corp/skills/chia-walletconnect)
- [MintGarden API](https://api.mintgarden.io/docs)
- [WalletConnect Documentation](https://docs.walletconnect.com/)
- [Telegram Web Apps](https://core.telegram.org/bots/webapps)
- [Sage Wallet](https://www.sagewallet.io/)
- [CHIP-0002](https://github.com/Chia-Network/chips/blob/main/CHIPs/chip-0002.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram Web App setup guidance, CLI commands, integration snippets, configuration examples, and verification workflow guidance.]

## Skill Version(s):

1.0.0 (source: package.json and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
