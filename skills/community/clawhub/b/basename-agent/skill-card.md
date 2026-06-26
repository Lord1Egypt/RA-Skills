## Description: <br>
Basename Agent helps AI agents register a Basename on Base and obtain a BaseMail email address through Donate Buy, free auto-registration, or WalletConnect v2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check, register, and configure onchain Basenames and related BaseMail email access. It provides command examples, JavaScript helpers, and WalletConnect flows for Base mainnet identity registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad private-key-backed wallet signing power beyond simple Basename and email registration. <br>
Mitigation: Use a dedicated low-balance wallet, review every signing or transaction request, and avoid using the generic WalletConnect helper for arbitrary dApps. <br>
Risk: The configured PRIVATE_KEY has full spending authority for its wallet. <br>
Mitigation: Store the key only in environment variables, never pass it on the command line, and prefer mandatory confirmations before signing. <br>
Risk: BaseMail API flows may send wallet, token, signature, or registration data to external services. <br>
Mitigation: Review the publisher's API documentation and confirm exactly what data and tokens are transmitted before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/daaab/basename-agent) <br>
- [BaseMail](https://basemail.ai) <br>
- [BaseMail API documentation](https://api.basemail.ai/api/docs) <br>
- [DonateBuy contract on BaseScan](https://basescan.org/address/0x8b10c4D29C99Eac19Edc59C4fac790518b815DE7#code) <br>
- [CO-QAF and Attention Bonds](https://blog.juchunko.com/en/glen-weyl-coqaf-attention-bonds/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash, JavaScript, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction, signing, WalletConnect, and API-call instructions that require a funded wallet and sensitive credential handling.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
