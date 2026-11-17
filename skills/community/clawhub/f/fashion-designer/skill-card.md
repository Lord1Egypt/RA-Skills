## Description:

This skill provides outfit advice and shopping suggestions for clothing, shoes, accessories, and bags based on the user's profile, current needs, and style feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasontujun](https://clawhub.ai/user/jasontujun)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get personalized outfit, accessory, shoe, and bag recommendations from shopping sources based on their profile, stated need, and feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store lasting local profile information including gender, age range, body type, style preferences, and feedback.

Mitigation: Ask before saving profile details, keep only information needed for recommendations, and support review, correction, and deletion.

Risk: The skill may put personal profile and preference information into Feishu documents.

Mitigation: Confirm the user is comfortable with Feishu sharing, limit document contents to necessary recommendation context, and avoid sensitive details.

Risk: The skill gives image-download instructions that may fetch unvalidated external image URLs.

Mitigation: Validate image URLs before download, restrict downloads to expected image content, use temporary files, and delete downloaded files after upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasontujun/skills/fashion-designer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown recommendations with product links, price ranges, styling tips, and optional Feishu document content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include up to three outfit options and up to three product images per outfit when image handling succeeds.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
