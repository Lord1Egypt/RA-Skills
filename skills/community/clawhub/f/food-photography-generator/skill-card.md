## Description:

AI food photography generator for restaurants, recipe bloggers, cookbook authors, food brands, and Instagram creators that creates food marketing and editorial images with cinematic lighting and styling through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, restaurants, cookbook authors, food brands, and marketing teams use this skill to turn text prompts into food photography image URLs for menus, recipe cards, blogs, branding, and culinary editorial content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens are supplied on the command line and may be exposed through shell history, process listings, or logs.

Mitigation: Use a minimally privileged token, avoid shared or logged shells, and rotate the token if it may have been exposed.

Risk: Prompts and reference image identifiers are sent to an external image-generation provider.

Mitigation: Do not submit confidential recipes, customer data, proprietary campaign details, or other sensitive content unless external processing is approved.

Risk: The documented install path is broad and mutable.

Mitigation: Install only after review, and prefer a pinned, reviewed version or checksum when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/food-photography-generator)
- [Neta API token page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token supplied with --token; supports square, portrait, landscape, and tall image sizes plus optional reference image UUIDs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
