## Description:

Uses the DMXAPI platform and multimodal vision models for image description, OCR, chart analysis, object detection, scene understanding, and related image-recognition tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onee-io](https://clawhub.ai/user/onee-io)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and run DMXAPI CLI image-understanding workflows for local or remote images. It supports tasks such as OCR, document extraction, chart interpretation, object identification, and scene analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are sent to DMXAPI for processing, which can expose sensitive visual content.

Mitigation: Do not upload identity documents, contracts, medical, financial, confidential screenshots, or other sensitive images unless authorized and comfortable sending them to DMXAPI.

Risk: The skill depends on an installed third-party CLI and configured API key.

Mitigation: Install dmxapi-cli from a trusted source, preferably pinned or isolated to a project, and review generated commands before execution.

## Reference(s):

- [DMXAPI Console](https://www.dmxapi.cn/)
- [ClawHub skill page](https://clawhub.ai/onee-io/skills/dmxapi-image-recognition)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional text, table, or JSON results from image-recognition tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20+, dmxapi-cli, a configured DMXAPI API key, and image input as a local path or remote URL.]

## Skill Version(s):

1.0.0 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
