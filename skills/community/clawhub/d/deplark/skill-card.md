## Description:

Deploy static websites and Node.js apps to Deplark for fast access from mainland China using Codex or Claude Code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larksq](https://clawhub.ai/user/larksq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to publish static websites and Node.js apps on Deplark for users in mainland China, reusing an account connection across projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious: its partial scan covered 66.7% of components and noted credential-storage access plus environment and network capabilities without a declared tool scope; it reported no clear malicious intent.

Mitigation: Before installation, review how the skill uses credentials and confirm its local environment and network access fit your needs; treat the verdict as based on incomplete evidence.

Risk: After account consent, the macOS client uses Deplark-specific Keychain items, and the account connection can be reused across projects.

Mitigation: Review the account and requested permissions before consenting, and keep API keys out of chat, repositories, URLs, command arguments, and logs.

## Reference(s):

- [Deplark](https://deplark.com)
- [ClawHub release page](https://clawhub.ai/larksq/skills/deplark)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, JSON]

**Output Format:** [Shell commands and JSON command responses, including a deployment URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May build and publish a selected project after the user requests deployment and authorizes the account connection.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
