## Description:

Creates and manages online voting activities, including template search, participant and image management, and voting data reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caiguwang](https://clawhub.ai/user/caiguwang)

### License/Terms of Use:

MIT

## Use Case:

External organizers use this skill to create and manage online voting or evaluation campaigns, add participants, and review participation and vote results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad voting-related activation wording may invoke the skill when the user did not intend to manage a voting activity.

Mitigation: Use it when the request clearly concerns creating, managing, or reviewing a voting activity.

Risk: Image uploads send local files or retrieve remote images through the external Caiguang platform, and account operations use an access token.

Mitigation: Keep the token private and check the intended image and platform destination before uploading.

## Reference(s):

- [Source repository](https://github.com/caiguwang/caiguwang-creator)
- [ClawHub release](https://clawhub.ai/caiguwang/skills/caiguwang-creator)
- [Caiguang platform](https://www.chinacaigu.com)

## Skill Output:

**Output Type(s):** [Text, JSON, URLs, Guidance]

**Output Format:** [Concise text summaries and structured platform data, including activity links and vote statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include voting activity links, QR code image URLs, and activity or vote statistics.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
