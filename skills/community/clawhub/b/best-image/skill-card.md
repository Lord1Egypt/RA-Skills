## Description:

Best quality AI image generation (~$0.12-0.20/image). Text-to-image, image-to-image, and image editing via the EvoLink API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pharmacist9527](https://clawhub.ai/user/pharmacist9527)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate new images, transform image references, and edit images through EvoLink from natural-language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generation settings, and reference image URLs are sent to EvoLink using the user's API key.

Mitigation: Use this skill only with prompts and reference image URLs that are appropriate to share with EvoLink.

Risk: Image generation may create API charges, especially at higher quality settings.

Mitigation: Confirm the intended quality setting and API budget before running generation, and reserve 4K output for cases where the added cost is acceptable.

Risk: Generated image URLs expire after about 24 hours.

Mitigation: Download generated results promptly and rely on the locally saved image file for persistence.

## Reference(s):

- [Best Image on ClawHub](https://clawhub.ai/pharmacist9527/skills/best-image)
- [EvoLink](https://evolink.ai)
- [curl heredoc fallback](references/curl_heredoc.md)
- [PowerShell fallback](references/powershell.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Local image file with MEDIA path output, plus command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved locally; result URLs expire after about 24 hours.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
