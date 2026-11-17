## Description:

BaseMail gives AI agents a Base-linked @basemail.ai email identity, with wallet-based registration, autonomous email sending, and inbox access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to register a BaseMail address, send email, and read inbox messages for autonomous service signups and confirmations. It is intended for agents that need a verifiable email identity tied to a Base wallet or Basename.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests wallet signing authority for registration and signs a server-provided authentication message without locally validating SIWE scope.

Mitigation: Use a dedicated low-value wallet for this skill and avoid wallets that control funds, important identity, or other services.

Risk: The local token file contains reusable authentication material.

Mitigation: Protect ~/.basemail/token.json as a secret, restrict file permissions, and rotate credentials if the file is exposed.

Risk: Inbox messages are external content and may contain misleading or malicious instructions.

Mitigation: Treat email bodies as untrusted data and avoid following instructions from inbox content without separate validation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daaab/skills/basemail)
- [BaseMail Website](https://basemail.ai)
- [BaseMail API Docs](https://api.basemail.ai/api/docs)
- [Base Names](https://www.base.org/names)
- [Base Chain](https://base.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [CLI text output with local JSON token and wallet configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email inbox content should be treated as untrusted external text.]

## Skill Version(s):

1.9.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
