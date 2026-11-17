## Description:

Generates cosplay reference sheets and costume design illustrations from character or outfit descriptions, returning a direct image URL through the Neta/TalesOfAI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate cosplay reference sheet image URLs from character or costume descriptions for build planning, commissions, convention prep, photoshoots, listings, and tutorials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation example uses an unpinned npx command.

Mitigation: Install through ClawHub's reviewed install path or pin the package version or commit before running it.

Risk: The skill asks users to pass a real API token on the command line.

Mitigation: Avoid placing long-lived production tokens directly in shell history; use a short-lived or scoped token and rotate it after use when possible.

Risk: Prompts and reference UUIDs are sent to the external Neta/TalesOfAI service.

Mitigation: Do not submit confidential, unreleased, or rights-sensitive character and costume details unless that external service is approved for the intended data.

## Reference(s):

- [Cosplay Reference Generator on ClawHub](https://clawhub.ai/blammectrappora/skills/cosplay-reference-generator)
- [Neta API token setup](https://www.neta.art/open/)
- [TalesOfAI image generation API](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text image URL with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; accepts optional size and reference UUID parameters; submits prompts to an external image generation service and polls for completion.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
