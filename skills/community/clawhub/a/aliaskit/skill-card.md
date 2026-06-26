## Description: <br>
Persistent digital identity for this agent, including email, phone, virtual payment card, and TOTP code workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nalin-atmakur](https://clawhub.ai/user/nalin-atmakur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use AliasKit to give an agent a persistent identity for signups, email and SMS verification, 2FA workflows, messaging, and controlled online purchase flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad persistent authority over identity, messaging, 2FA, and payment workflows. <br>
Mitigation: Require explicit approval before every signup, purchase, card reveal, message send, TOTP action, deletion, or card cancellation. <br>
Risk: identity.json can contain API keys, identity identifiers, email, phone, date of birth, and card decryption key material. <br>
Mitigation: Keep identity.json out of shared folders, backups, logs, and version control, and avoid printing sensitive contents in conversation output. <br>
Risk: The setup script installs aliaskit@latest, so dependency behavior can change between runs. <br>
Mitigation: Use a locked-down execution environment and pin the dependency version before operational use. <br>


## Reference(s): <br>
- [AliasKit SDK Method Reference](references/sdk-methods.md) <br>
- [AliasKit documentation](https://www.aliaskit.com/docs) <br>
- [AliasKit ClawHub release](https://clawhub.ai/nalin-atmakur/aliaskit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read a local identity.json containing AliasKit credentials and identity state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
