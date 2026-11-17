## Description:

Generates professional headshot image URLs from text prompts through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create professional headshot images from prompts and receive a direct image URL. It supports portrait, landscape, square, and tall outputs, with optional reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference IDs, and a Neta/TalesOfAI API token are sent to the external image generation service.

Mitigation: Use a low-privilege, revocable token and avoid sensitive personal details or unauthorized reference images in prompts.

Risk: A token passed on the command line may be exposed through shell history or process logs.

Mitigation: Rotate the token if exposure is suspected and prefer short-lived or low-privilege credentials.

Risk: Floating install references may not resolve to the reviewed release.

Mitigation: Verify the publisher and install from a pinned commit or trusted ClawHub package.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/ai-headshot-skill)
- [Neta AI API Access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints a single generated image URL to stdout on success.]

## Skill Version(s):

2.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
