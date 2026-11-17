## Description:

Extends one or more images through the Flyelep AI Tool API to fill canvas edges at a requested aspect ratio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other image creators can use this skill to extend source images to a chosen aspect ratio, individually or in batches, and share the returned image links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends local images to a third-party service, and the returned links may be publicly accessible.

Mitigation: Before uploading, ensure the user is comfortable sending the selected images to Flyelep; avoid uploading sensitive images.

Risk: The claimed 24-hour expiry for uploaded image links is not verified.

Mitigation: Treat returned links as potentially accessible beyond 24 hours and avoid relying on expiry to protect sensitive images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyelepai/skills/flyelep-intelligent-extension)
- [Flyelep intelligent extension API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/intelligentExtension)
- [Flyelep image upload API](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)
- [Flyelep Open Platform](https://www.flyelep.cn/controlboard)

## Skill Output:

**Output Type(s):** [Image URLs, API response data]

**Output Format:** [JSON response data containing generated image URLs and a task ID]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns successful image URLs in input order; a batch may return fewer URLs than inputs when individual images fail.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
