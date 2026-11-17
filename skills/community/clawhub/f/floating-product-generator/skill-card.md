## Description:

Generate cinematic floating product shots, levitating product photography, and hovering e-commerce images with dramatic studio lighting for e-commerce, advertising, luxury brand marketing, creator content, and commercial product photography via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate floating product photography from text prompts for commerce listings, ads, brand marketing, and creator content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires users to pass a Neta API token on the command line.

Mitigation: Use a low-privilege, revocable token and avoid exposing tokens in shell history, logs, or shared terminals.

Risk: Prompts and optional reference identifiers are sent to an external image generation service.

Mitigation: Avoid submitting sensitive product plans, personal data, confidential images, or regulated content unless the service terms and data handling are approved.

Risk: The install command may resolve mutable package content if not pinned or reviewed.

Mitigation: Install through a trusted, pinned, or reviewed channel before use in controlled environments.

## Reference(s):

- [Floating Product Generator on ClawHub](https://clawhub.ai/blammectrappora/skills/floating-product-generator)
- [Neta API access](https://www.neta.art/open/)
- [Neta image API endpoint](https://api.talesofai.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and supports square, portrait, landscape, and tall image sizes plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
