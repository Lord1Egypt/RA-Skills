## Description:

Ethermail helps agents access Web3 email through EtherMail with WalletConnect for wallet-address inboxes, Web3 notifications, and decentralized agent communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use Ethermail to access EtherMail accounts tied to EVM wallet addresses, extract WalletConnect login URIs, and read or send Web3 email through browser or Telegram workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet authentication may be routed through raw private-key signing.

Mitigation: Use a dedicated low-value wallet, avoid giving raw private keys to third-party scripts, and prefer a pinned, reviewed connector or hardware or isolated signer.

Risk: WalletConnect signing requests could be unsafe if accepted without review.

Mitigation: Verify each WalletConnect request before signing and use only reviewed WalletConnect tooling.

Risk: The extraction script accepts a URL and uses browser automation.

Mitigation: Do not run the extraction script against arbitrary URLs, and review browser automation behavior before installation or use.

## Reference(s):

- [ClawHub Ethermail Skill](https://clawhub.ai/daaab/skills/ethermail)
- [EtherMail Website](https://ethermail.io)
- [EtherMail Wallet Login](https://ethermail.io/accounts/login)
- [EtherMail Telegram Mini App](https://t.me/ethermailappbot/app?startapp=afid_6986e9a5c5a97b905a78c390)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline JavaScript and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WalletConnect URI extraction steps and browser automation guidance.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
