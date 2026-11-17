## Description:

Ghost Eye lets a pure-text LLM analyze images through an OpenAI-compatible vision model, returning OCR text and a visual summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunter-crk](https://clawhub.ai/user/hunter-crk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert incoming images, screenshots, photos, or scanned documents into text that a text-only LLM can reason over. It supports automatic image preprocessing or explicit tool-call use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbound images can be sent automatically to a third-party vision API.

Mitigation: Use explicit tool-call mode for sensitive work and configure an approved OpenAI-compatible vision endpoint before deployment.

Risk: OCR text and visual summaries are stored in plaintext cache files by default.

Mitigation: Disable caching or regularly clear the cache when images may contain personal, business, credential, or regulated data.

Risk: Using image URLs can introduce uncontrolled network egress.

Mitigation: Prefer local image paths and use image URLs only when outbound network access is constrained and approved.

## Reference(s):

- [OpenClaw multimodal preprocessing configuration](references/multimodal-config.md)
- [ClawHub Ghost Eye skill page](https://clawhub.ai/hunter-crk/skills/ghost-eye)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON object with success, content, and metadata fields; content contains OCR text and a visual summary in plain text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEXN2_API_KEY; image analysis results may be cached as JSON files for up to 7 days by default.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
