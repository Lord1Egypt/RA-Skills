## Description:

Generates Barbie-style AI portrait image URLs from text descriptions using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn text prompts into Barbie-style AI portrait image URLs for social, branded, or creative visual workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional reference image identifiers are sent to an external image-generation service.

Mitigation: Avoid confidential, sensitive personal, or proprietary content in prompts and reference identifiers unless the service terms and data handling are acceptable.

Risk: The Neta API token is a reusable secret required for generation.

Mitigation: Pass the token through an environment variable or secret manager and avoid exposing it in shell history, logs, screenshots, or shared command transcripts.

Risk: Generated outputs may be unsuitable for a specific brand, audience, or rights context.

Mitigation: Review generated image URLs and resulting images before publishing or using them in customer-facing materials.

Risk: The artifact is installed and run from a third-party publisher account.

Mitigation: Install only from the verified ClawHub publisher profile or another trusted, pinned source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/barbie-style-generator)
- [Neta API token page](https://www.neta.art/open/)
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image)
- [Neta artifact polling endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid})

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text image URL with progress messages on stderr and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall image sizes plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
