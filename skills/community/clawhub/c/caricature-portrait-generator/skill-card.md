## Description:

Generate AI caricature portraits with exaggerated features from text descriptions, returning a direct image URL through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate caricature, cartoon, comic, or funny face portrait image URLs from descriptive prompts for gifts, social media, invitations, and personalized art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an API token and sends it to api.talesofai.com, which the security evidence says is not clearly disclosed in the main skill instructions.

Mitigation: Review before installing and use only a narrowly scoped, revocable Neta token.

Risk: Prompts and reference image IDs may be sent to the external image generation service.

Mitigation: Avoid sensitive personal data, confidential prompts, and reference IDs that should not be shared with the service.

Risk: The security guidance recommends install-source review for this low-trust release.

Mitigation: Prefer a pinned or checksum-verified install source before deployment.

## Reference(s):

- [Neta AI API token setup](https://www.neta.art/open/)
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/caricature-portrait-generator)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands]

**Output Format:** [Plain text image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference UUID inputs affect the generated image request.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
