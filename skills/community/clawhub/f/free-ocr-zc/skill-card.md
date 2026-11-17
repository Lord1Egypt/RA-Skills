## Description:

Extracts text from image URLs or local image files through OpenRouter using a configurable OCR model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can invoke this skill to run OCR on image URLs or local image files and receive extracted text, with optional prompt customization for the OCR request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local images and image URLs can be sent to OpenRouter or another configured provider.

Mitigation: Use only images approved for that provider, and avoid sensitive documents unless the data handling has been reviewed.

Risk: The API key is used when making remote OCR requests.

Mitigation: Keep the key scoped and limited, store it outside source control, and rotate it if exposure is suspected.

Risk: A configurable OCR_BASE_URL can redirect requests and credentials to an unexpected endpoint.

Mitigation: Do not allow untrusted users or wrappers to set OCR_BASE_URL, and review the configured endpoint before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/skills/free-ocr-zc)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Plain text OCR output with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenRouter API key and may use a configurable OCR model and base URL.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
