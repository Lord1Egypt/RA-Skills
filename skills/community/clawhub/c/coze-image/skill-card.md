## Description:

Generate images using Coze AI platform with text-to-image generation and automatic Base64 encoding for inline preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pgyppp](https://clawhub.ai/user/pgyppp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to call a Coze image project from text prompts and receive generated images as inline Base64 data URIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted endpoint configuration can let untrusted callers direct requests to unexpected services.

Mitigation: Restrict who can pass api_url, prefer an approved IMAGE_API_URL, and add endpoint allowlisting before broader deployment.

Risk: Coze API tokens and prompts may be exposed through unsafe runtime configuration or sensitive prompt content.

Mitigation: Use a least-privilege token, keep tokens in environment configuration, and avoid submitting sensitive prompts.

Risk: Generated image URLs are fetched automatically, which can increase exposure to untrusted remote content.

Mitigation: Run the skill in an isolated environment and add image-download size and content limits before allowing untrusted use.

Risk: Implicit invocation and automatic updates can run or change the skill with limited user review.

Mitigation: Require confirmation for invocation where possible, pin dependencies, and consider disabling auto-update.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pgyppp/skills/coze-image)
- [Publisher profile](https://clawhub.ai/user/pgyppp)
- [Payload shape reference](references/payload-shape.md)
- [Skill metadata repository](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; runtime responses are JSON objects containing an image data URI or structured error fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful responses include image, mime_type, filename, and source_url; debug mode can include api_url, project_id, and session_id.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
