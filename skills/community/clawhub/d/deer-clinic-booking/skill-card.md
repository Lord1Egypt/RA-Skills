## Description:

Deer helps users view booking guidance, submit appointment requests, contact online support, and query pricing for Lumiin Dermatology through BeautsGO.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get Lumiin Dermatology booking guidance, submit requested appointment details, contact support, and check treatment pricing through BeautsGO.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Appointment details may be sent to external BeautsGO/yestokr services without a clear confirmation step.

Mitigation: Require an explicit user confirmation before submitting contact or appointment details, and verify the clinic and platform identity before entering a phone number.

Risk: The security review flags API, credential, URL-opening, and language-loading issues that should be reviewed before use.

Mitigation: Review and fix those issues before deployment, then rescan the skill before enabling it for users.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beautsgo/skills/deer-clinic-booking)
- [BeautsGO Lumiin Dermatology booking page](https://i.beautsgo.com/cn/hospital/lumiin-dermatology/skill)
- [BeautsGO Lumiin Dermatology details page](https://i.beautsgo.com/cn/hospital/lumiin-dermatology?from=skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking submission status, pricing lookup results, support links, or app download links.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
