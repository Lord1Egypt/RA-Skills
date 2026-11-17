## Description:

Turns a user-provided fund quarterly report highlight sheet and authorized stills into separate short talking clips that speak only supplied report facts and manager commentary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Wealth advisors and fund marketers use this skill to plan and produce one short talking clip per authorized still from a supplied quarterly report highlight sheet, with separate approval for paid generation stages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Beatra receives fund-report inputs and still images under broad shared account authorization.

Mitigation: Install only if you trust Beatra with these inputs and review the requested permissions before approving access.

Risk: A shared local device token grants account access across Beatra skills.

Mitigation: Keep the device token private and review account access before connecting the device.

Risk: Automatic updates can replace reviewed code without separate confirmation.

Mitigation: Turn automatic updates off using the documented command when a pinned, reviewed version is required.

Risk: Generated financial claims or likeness and voice use could exceed the supplied facts or permissions.

Mitigation: Use only authorized images, voices, and report materials; review each clip against the supplied highlight sheet before sharing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/fund-report-talking)
- [Quarterly report talking workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Media artifacts]

**Output Format:** [Labeled Markdown plan and separate audio and video artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 2–8 separate 2–15-second clips; no stitching.]

## Skill Version(s):

0.1.9 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
