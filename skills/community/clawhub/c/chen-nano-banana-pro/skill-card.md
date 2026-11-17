## Description:

Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Supports text-to-image, edits, and 1K/2K/4K resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill through an agent to generate or edit PNG images with Google Gemini 3 Pro Image, selecting 1K, 2K, or 4K output resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images may be sent to Google's Gemini API.

Mitigation: Use only non-sensitive prompts and images unless the user is comfortable sending that content to the third-party API.

Risk: Gemini API keys can be exposed if pasted into chat or passed on the command line.

Mitigation: Prefer GEMINI_API_KEY from a protected environment variable or secret manager, and rotate any key that was shared insecurely.

Risk: The uv workflow installs dependencies without pinned versions.

Mitigation: Review and pin dependencies before running the workflow in controlled or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/skills/chen-nano-banana-pro)
- [Publisher profile](https://clawhub.ai/user/cs995279497-byte)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands and generated PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates PNG image files at the requested filename or path.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
