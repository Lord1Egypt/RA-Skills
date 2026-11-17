## Description:

Defines a Feishu bot identity messaging protocol for double-message robot mentions, sender attribution, user-identity replies, group user mapping, and ID refresh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyfate](https://clawhub.ai/user/skyfate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents working in controlled Feishu workspaces use this skill to route bot-to-bot mentions and replies while preserving an explicit sender identity protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated user identity and text-based sender markers can misroute or impersonate replies.

Mitigation: Install only in Feishu workspaces where strict allowlists, explicit authorization for delegated sends, immutable sender-ID validation, loop prevention, and auditing are enforced.

Risk: Display names or bracket markers may be mistaken for proof of sender identity.

Mitigation: Validate sender identity from trusted Feishu IDs and do not rely on display names or message markers alone.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skyfate/skills/feishu-robot-protocol)
- [Publisher profile](https://clawhub.ai/user/skyfate)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with Feishu message templates and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes protocol rules for double messages, sender markers, user ID mapping, and ID refresh.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
