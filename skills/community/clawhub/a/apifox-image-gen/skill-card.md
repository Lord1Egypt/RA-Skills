## Description:

Generates images through the Apifox jyapi.AI-WX.CN image API using gpt-image-1.5 or grok-4-1-image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darker314159](https://clawhub.ai/user/darker314159)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can ask an agent to generate image files from text prompts with selectable model, size, quantity, and output path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts are sent to the jyapi.AI-WX.CN service.

Mitigation: Avoid sensitive, confidential, personal, or regulated prompts unless the service has been approved for that data.

Risk: The artifact bundles a shared API key.

Mitigation: Prefer a revised version that reads credentials from user-controlled secrets and rotates or removes the bundled key.

Risk: API-controlled image URLs can be downloaded and written to a caller-provided path.

Mitigation: Use disposable output directories, restrict allowed download hosts, validate image content and size, and prevent overwriting arbitrary files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darker314159/skills/apifox-image-gen)
- [Publisher profile](https://clawhub.ai/user/darker314159)
- [jyapi.AI-WX.CN API host](https://jyapi.AI-WX.CN)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [Generated image files with console status text and optional shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves generated images to /tmp by default or to a caller-provided output path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
