## Description:

Guides customers through xdccy.com account setup and batch parcel tracking, then summarizes results and exports reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdccycom](https://clawhub.ai/user/xdccycom)

### License/Terms of Use:

MIT-0

## Use Case:

Customers and their assistants use this skill to register or access an xdccy.com account, check multiple parcel tracking numbers, review delivery statistics, and export reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account passwords and stores reusable API and session credentials in a plaintext local file.

Mitigation: Use a dedicated account and password; keep ~/.workbuddy/xdcc-credentials.env private, never paste its contents into chat, and rotate or delete keys or tokens if exposed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xdccycom/skills/batch-query)
- [Parcel tracking API reference](references/api_reference.md)
- [Customer onboarding guide](references/onboarding_guide.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Files]

**Output Format:** [In-chat guidance and tracking summaries; JSON, CSV, or TXT reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch delivery-status and timing statistics; exports can be opened or processed separately.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; bundled skill frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
