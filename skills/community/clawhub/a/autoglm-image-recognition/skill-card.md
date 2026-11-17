## Description:

Use the AutoGLM Image Recognition API to analyze and describe image content, including object or scene recognition, OCR-like text extraction, and general image description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khurramjamil12](https://clawhub.ai/user/khurramjamil12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit public image URLs, or local images after upload, to AutoGLM for visual description, object and scene recognition, and OCR-like text extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files are uploaded to a public third-party URL before recognition.

Mitigation: Use only non-sensitive images and avoid documents, credentials, private screenshots, regulated data, or arbitrary local files unless the workflow adds confirmation, image validation, size limits, and private URL handling.

Risk: The skill uses local authentication without enough safeguards or scoping.

Mitigation: Review token handling before broad use and ensure credentials are scoped to the intended AutoGLM operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/khurramjamil12/skills/autoglm-image-recognition)
- [AutoGLM image recognition API endpoint](https://autoglm-api.autoglm.ai/agentdr/v1/assistant/skills/image-recognition)
- [AutoGLM upload-mix API endpoint](https://autoglm-api.autoglm.ai/agentdr/v1/assistant/upload-mix)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls]

**Output Format:** [Markdown guidance with shell commands and JSON API responses containing recognition text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recognition results are presented from the API response text; local files must first be uploaded to obtain a public image URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
