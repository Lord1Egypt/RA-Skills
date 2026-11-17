## Description:

Converts supported local files into Markdown through a Docker-only CLI that selects a fixed-version prebuilt Aliyun CR image by host architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert supported local documents and images into Markdown for downstream analysis or processing while preserving logs and metadata from the Dockerized CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a third-party Docker image from the configured registry.

Mitigation: Install only when the image source is trusted, and review or pin the exact container digest before use.

Risk: Local VL configuration and .env values can be passed into the container.

Mitigation: Keep unrelated secrets out of the skill's .env file and prefer short-lived VL credentials.

Risk: IMAGE_NAME or registry overrides can redirect execution to a different container image.

Mitigation: Avoid image or registry overrides unless the replacement image is fully trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kadbbz/skills/convert-document-to-markdown)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown or structured JSON containing markdown, logs, and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Docker-only file command; supported inputs include PDF, Office Open XML, common image, text, JSON, XML, and Markdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
