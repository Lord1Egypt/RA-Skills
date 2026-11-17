## Description:

Generates multi-themed food collages for Viral Cakes, Street Food, Smoothie Bowls, Coffee Art, and Fusion Tacos, including circle-masked image layouts and curated item-pick prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[expysf98](https://clawhub.ai/user/expysf98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate themed food-pick collage assets from predefined categories and local item images. It is suited for social, menu, or visual prompt workflows that need 3x3 circular image layouts with dynamic pick titles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package ships an undeclared Cloudflare image-generation script with embedded credentials.

Mitigation: Remove or fully disclose the script, revoke and replace the exposed token, and require review before deployment.

Risk: The image-generation script uses unsafe shell execution with prompt input.

Mitigation: Replace shell=True command construction with a structured HTTP client or argument-vector subprocess call and validate user-supplied prompt and output path values.

Risk: The image-generation script writes API responses to a shared /tmp file.

Mitigation: Handle API responses in memory or use unique temporary files with restrictive permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/expysf98/skills/design-pick2)
- [Publisher profile](https://clawhub.ai/user/expysf98)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one 3x3 collage PNG per configured food theme when the expected source item images are present.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
