## Description:

AliasKit gives an agent a persistent digital identity with email, phone, virtual payment card, TOTP codes, and messaging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nalin-atmakur](https://clawhub.ai/user/nalin-atmakur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use AliasKit to let an agent fill identity fields, complete signups, receive email/SMS verification, handle 2FA, send messages, and assist with online purchases where approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses sensitive identity credentials and payment-related keys in identity.json.

Mitigation: Restrict identity.json file permissions, keep it out of version control, and rotate any AliasKit API key that may have been exposed.

Risk: The skill supports high-impact actions such as purchases, card reveal, outbound messages, inbox deletion, and 2FA use.

Mitigation: Require explicit user approval before those actions and review the requested recipient, service, amount, or code use before execution.

Risk: Setup can load an existing identity ID and bind it to the local agent state.

Mitigation: Run setup only with trusted identity IDs and confirm the resulting identity details before using them in workflows.

Risk: The skill connects the agent to real inbox, SMS, identity, 2FA, and payment workflows.

Mitigation: Install it only for agents intended to handle those workflows and review the skill carefully before deployment.

## Reference(s):

- [AliasKit SDK Method Reference](references/sdk-methods.md)
- [AliasKit Documentation](https://www.aliaskit.com/docs)
- [AliasKit Skill on ClawHub](https://clawhub.ai/nalin-atmakur/skills/aliaskit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with TypeScript examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local identity.json file containing sensitive credentials and identity state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
