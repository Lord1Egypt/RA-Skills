## Description:

CLIProxy Media analyzes images and PDFs through a configurable CLIProxy-compatible Anthropic Messages endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bencoremans](https://clawhub.ai/user/bencoremans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to analyze, describe, compare, or extract information from image files, image URLs, and PDFs through a trusted CLIProxy-compatible endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local images, PDFs, and prompts can be sent to any configured endpoint.

Mitigation: Use only a trusted CLIProxy endpoint, preferably localhost or trusted HTTPS, and review use before sending private photos, scans, contracts, medical records, or financial PDFs.

Risk: The skill broadly routes media analysis through CLIProxy without clear consent safeguards.

Mitigation: Confirm endpoint choice and data handling before invoking the skill, and avoid broad automatic use when a built-in or first-party media tool would keep data in a safer path.

## Reference(s):

- [CLIProxy Media on ClawHub](https://clawhub.ai/bencoremans/skills/cliproxy-media)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown responses, often with shell commands and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional streaming output, endpoint/model overrides, system prompts, and configurable maximum tokens.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
