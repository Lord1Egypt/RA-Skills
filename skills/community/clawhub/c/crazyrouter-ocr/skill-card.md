## Description:

Image-to-text and OCR via Crazyrouter API using vision models to extract text, describe images, and analyze screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujfcn](https://clawhub.ai/user/xujfcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send selected local images or screenshots to Crazyrouter vision models for OCR, visual description, and screenshot analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, prompts, and derived OCR or analysis content are sent to Crazyrouter and potentially its model providers.

Mitigation: Use the skill only for images that are acceptable to send to that service; avoid secrets, credentials, IDs, medical or financial records, and private screenshots.

Risk: CRAZYROUTER_BASE_URL can redirect requests, including the API key and full image data, to an alternate endpoint.

Mitigation: Leave CRAZYROUTER_BASE_URL unset unless the endpoint is fully trusted and expected for this use.

## Reference(s):

- [Crazyrouter](https://crazyrouter.com)
- [ClawHub skill page](https://clawhub.ai/xujfcn/skills/crazyrouter-ocr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text or Markdown returned on stdout or written to a user-specified output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY; supports user-selected image path, prompt, model, and optional output file.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
