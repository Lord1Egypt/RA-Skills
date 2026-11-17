## Description:

Funpay Assistant monitors FunPay chats, sends automated replies to common customer questions, and forwards unrecognized messages or login-consent alerts to the operator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirra87654321](https://clawhub.ai/user/mirra87654321)

### License/Terms of Use:


## Use Case:

Marketplace operators can use this skill to monitor FunPay customer chats, answer repeated availability or region-related questions, and surface conversations that need manual attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package ships an embedded FunPay account credential and private chat/order state.

Mitigation: Remove packaged credentials and state, rotate the exposed credential, and require installers to provide their own credential through a secure local configuration path.

Risk: The skill can automatically send messages to customers from the operator's FunPay account.

Mitigation: Disclose automated messaging behavior before use and require operator review for sensitive account-access replies.

## Reference(s):

- [Artifact skill documentation](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/mirra87654321/skills/funpay-assistant)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing setup and usage guidance for a FunPay chat-monitoring script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
