## Description: <br>
BaseMail gives AI agents a verifiable onchain email identity on Base, using SIWE wallet authentication to register, send email, and read inbox confirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an AI agent a BaseMail address tied to a Base wallet, then register for services, send messages, and receive email confirmations through the BaseMail API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires wallet-signing authority and access to a BaseMail mailbox. <br>
Mitigation: Use a dedicated low-value wallet, review the requested operations before running scripts, and avoid using a wallet that controls valuable assets. <br>
Risk: Wallet setup and unlock flows can expose mnemonics, private keys, or wallet passwords in terminal output. <br>
Mitigation: Prefer BASEMAIL_PRIVATE_KEY over managed wallet generation, avoid running setup in logged terminals or CI, and treat displayed mnemonics or echoed passwords as highly sensitive. <br>
Risk: Cached BaseMail tokens can grant mailbox access after registration. <br>
Mitigation: Protect BASEMAIL_TOKEN and ~/.basemail/token.json as secrets, restrict local file permissions, and remove cached tokens when access is no longer needed. <br>


## Reference(s): <br>
- [BaseMail ClawHub Release](https://clawhub.ai/daaab/basemail) <br>
- [BaseMail Website](https://basemail.ai) <br>
- [BaseMail API Documentation](https://api.basemail.ai/api/docs) <br>
- [Base Names](https://www.base.org/names) <br>
- [Base Chain](https://base.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local BaseMail wallet, token, and audit files under ~/.basemail when the user runs the provided scripts.] <br>

## Skill Version(s): <br>
1.8.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
