## Description:

Basename Agent helps agents register a yourname.base.eth Basename and create a yourname@basemail.ai account through Donate Buy, worker-paid auto-registration, or WalletConnect v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous agents use this skill to obtain an onchain Basename identity and BaseMail address, then interact with registration and email APIs or WalletConnect flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad wallet-signing and transaction authority for Basename registration and WalletConnect flows.

Mitigation: Use only a dedicated, low-balance wallet and review each transaction or signature manually before allowing unattended operation.

Risk: Registration, email/account binding, signatures, and transactions may be irreversible or security-sensitive.

Mitigation: Confirm the requested name, recipient wallet, contract address, transaction value, and SIWE message before signing or sending funds.

Risk: Weak scoping and confirmation controls increase the impact of malicious or unintended dApp requests.

Mitigation: Prefer interactive mode and strict allowlists for dApps, contract addresses, methods, and expected transaction values.

## Reference(s):

- [BaseMail](https://basemail.ai)
- [BaseMail API Docs](https://api.basemail.ai/api/docs)
- [DonateBuy Contract](https://basescan.org/address/0x8b10c4D29C99Eac19Edc59C4fac790518b815DE7#code)
- [AttentionBondEscrow Contract](https://basescan.org/address/0xF5fB1bb79D466bbd6F7588Fe57B67C675844C220#code)
- [CO-QAF and Attention Bonds](https://blog.juchunko.com/en/glen-weyl-coqaf-attention-bonds/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline Bash, JavaScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce wallet transaction, signing, API registration, and email-send instructions that require user-controlled credentials and funds.]

## Skill Version(s):

2.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
