## Description:

Exact Discord recipient routing for trusted team collaboration: resolve one canonical roster entry, send to its immutable Discord ID, and verify the delivery target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

### License/Terms of Use:

MIT-0

## Use Case:

Agents in trusted team Discord workflows use this procedure to resolve an explicitly named recipient from the active approved roster, send to the corresponding immutable Discord user ID, and verify that the delivery response reports the same target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A stale roster or unauthorized message request could lead to a relay being routed to an unintended recipient.

Mitigation: Keep requester admission under host controls and use only the active approved roster, requiring one exact active match and its immutable Discord user ID.

Risk: Recipient IDs and delivery records can expose personal or operational information, and a send could be overstated if the receipt does not confirm its target.

Mitigation: Protect delivery records, retain only non-content evidence, and claim a relay as sent only when the response confirms the expected target; otherwise report that confirmation is unavailable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/daniel-refahi-ikara/skills/discord-recipient-safety)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Procedural instructions and delivery status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recipient-specific routing guidance; delivery records contain non-content evidence only.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
