## Description:

明洞丹雅皮肤科 — 首尔明洞人气皮肤科，提供皮肤管理、激光、注射等医美项目。

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Dana to view DAN-A Clinic booking guidance, submit appointment requests through BeautsGO, open clinic or consultation pages, query prices, and get app download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking details may be sent to an external appointment API when a booking request with a parsed date is handled.

Mitigation: Require an explicit user confirmation step before submission and clearly disclose that booking details are sent to BeautsGO's appointment service.

Risk: Browser-opening behavior relies on shell-based commands.

Mitigation: Replace shell-based URL opening with a safer browser-launch mechanism and keep the BeautsGO URL allowlist enforced.

Risk: Bundled API tokens and APK download links create operational and integrity concerns.

Mitigation: Remove or rotate bundled tokens, load secrets from managed configuration, and provide integrity guidance such as checksums or trusted-store preference for APK downloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beautsgo/skills/dana-clinic-booking)
- [BeautsGO DAN-A Clinic Booking Page](https://i.beautsgo.com/cn/hospital/dan-a-clinic/skill)
- [BeautsGO DAN-A Clinic Page](https://i.beautsgo.com/cn/hospital/dan-a-clinic?from=skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted string responses with booking guidance, appointment status, price information, links, or error messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger HTTPS requests to external appointment and price APIs or attempt to open allowlisted BeautsGO URLs in the user's browser.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, skill.json, and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
