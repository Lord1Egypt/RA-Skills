## Description:

Sends SMS notifications to the user's Free Mobile phone number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dclauzel](https://clawhub.ai/user/dclauzel)

### License/Terms of Use:

FPC (Fais pas chier), https://clauzel.eu/FPC/

## Use Case:

Agents and users use this skill to send short operational alerts or reminders to the configured Free Mobile subscriber phone number. It requires a Free Mobile SMS notification user ID and API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMS content and API credentials may be exposed through the URL-query request method.

Mitigation: Review before installing and prefer changing the implementation to POST before using it with real credentials.

Risk: The skill can send SMS messages without documented confirmation guidance.

Mitigation: Require explicit confirmation before each send.

Risk: SMS messages may carry sensitive content to an external mobile provider.

Mitigation: Avoid sending secrets in SMS messages and use only an account where this API-key access is acceptable.

## Reference(s):

- [Free Mobile SMS reference](references/REFERENCE.md)
- [Free Mobile SMS notification documentation](https://mobile.free.fr/account/mes-options/notifications-sms)
- [ClawHub skill page](https://clawhub.ai/dclauzel/skills/freemobile-sms)
- [Project homepage](https://github.com/dClauzel/freemobile-sms)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [SMS messages are limited to 160 characters by the script.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
