## Description:

Recognizes and translates text in images through the Flyelep AI Tool API, then returns the translated image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can translate poster or product-image text into a supported target language and receive a URL for the translated image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images sent for translation may be stored on third-party public storage, and unsigned links may be accessible to anyone who has them; the stated 24-hour expiry is unverified.

Mitigation: Get the user's consent before uploading local images, avoid sending sensitive images unless the user accepts this exposure, and treat returned links as public rather than relying on their stated expiry.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/flyelepai/skills/flyelep-image-translate)
- [Flyelep image translation API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate)
- [Flyelep image upload API](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)
- [Flyelep API key application portal](https://www.flyelep.cn/controlboard)

## Skill Output:

**Output Type(s):** [Text, URLs]

**Output Format:** [Text containing translated image URL(s)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch requests support up to 20 image-language combinations; the skill returns URLs rather than image contents.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
