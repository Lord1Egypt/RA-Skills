## Description:

Builds a two-tier sunset workflow that re-engages dormant contacts after a configurable inactivity window and suppresses contacts that do not re-engage within the follow-up window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operations and CRM teams use this skill to configure a HubSpot workflow that attempts re-engagement before suppressing inactive contacts from marketing email. The workflow is intended to protect deliverability while preserving a chance to reactivate dormant contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overbroad enrollment filters or suppression criteria could affect contacts that should remain marketable.

Mitigation: Confirm filters on a small segment, review the non-marketing action with the email reach owner, and keep a clear reversal process for affected contacts.

Risk: AI-assisted HubSpot workflow generation may create OR-based triggers or omit unsupported conditions, enrolling contacts incorrectly.

Mitigation: Manually verify and correct the enrollment trigger, unknown-status checks, re-enrollment settings, and workflow goals before activation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomgranot/skills/engagement-suppression-workflow)

## Skill Output:

**Output Type(s):** [Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with step-by-step workflow configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes manual setup steps, optional AI-assisted build guidance, verification checks, rollback steps, and tuning guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
