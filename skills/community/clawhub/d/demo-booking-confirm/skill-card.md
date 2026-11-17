## Description:

Creates labeled booking-confirmation voice lines and generates one spoken clip per notice for confirmed, rescheduled, and cancelled shop bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shop staff and sellers use this skill to draft labeled booking notices from confirmed facts and generate 8 to 20 matching voice clips for guests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra device token grants broader media-generation, wallet, task, upload, telemetry, uninstall, and update access than booking speech alone requires.

Mitigation: Install only if that access is acceptable; consider a dedicated Beatra account or environment.

Risk: Automatic package updates can change executable skill behavior without separate approval.

Mitigation: Consider disabling automatic updates and reviewing new releases before enabling them.

## Reference(s):

- [Booking Confirmation Voice Pack on ClawHub](https://clawhub.ai/beatra-ai/skills/demo-booking-confirm)
- [Booking confirmation workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Audio]

**Output Format:** [Labeled booking-notice list and individual voice clips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One spoken clip per labeled notice; typically 8 to 20 clips.]

## Skill Version(s):

0.2.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
