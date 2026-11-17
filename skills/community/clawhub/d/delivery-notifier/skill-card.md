## Description:

Fetches delivery notifications from Gmail, filters likely marketing messages, extracts delivery details, and sends WhatsApp alerts for personal deliveries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[o0o-sp](https://clawhub.ai/user/o0o-sp)

### License/Terms of Use:


## Use Case:

Developers or operators use this skill to monitor a configured Gmail inbox for delivery-related messages and notify a controlled WhatsApp recipient when a new personal delivery appears.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private Gmail inbox content while looking for delivery messages.

Mitigation: Use a dedicated or restricted Gmail account where possible and grant only the access needed for delivery notifications.

Risk: Delivery metadata may be sent to the fixed WhatsApp recipient configured in the artifact.

Mitigation: Change the WhatsApp target to a controlled recipient before running the skill.

Risk: The debug script may print fetched email content and related metadata.

Mitigation: Remove, restrict, or avoid running the debug script in normal use.

Risk: The local state file stores notification history used for deduplication.

Mitigation: Protect or relocate the state file and retain only the minimum data needed to prevent duplicates.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown/plain-text delivery alerts and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts include courier, tracking value when found, email subject, and a generated-by footer; local state is used to reduce duplicate notifications.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
