## Description:

Generates barcode images as base64 content by type and parameters, or recognizes barcode content from an image URL or base64 image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate EAN, Code128, Code39, UPC, ISBN, and other barcode images, or to read barcode type and number from submitted barcode images through JisuAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Barcode image content and API key values are sent to a third-party API provider.

Mitigation: Use a restricted and revocable JISU_API_KEY, and avoid submitting sensitive barcode images or private/internal image URLs.

Risk: API keys and barcode data are sent in request query parameters where provider or proxy logs may retain them.

Mitigation: Route only acceptable data through the skill and rotate the API key if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/barcode2)
- [JisuAPI Barcode Generation and Recognition API](https://www.jisuapi.com/api/barcode/)
- [JisuAPI](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands; runtime script output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
