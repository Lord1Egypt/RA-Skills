## Description:

Art Deco Generator creates 1920s-inspired Gatsby-style art deco posters, prints, wedding invitations, luxury branding, and illustrations from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate art deco images such as posters, invitations, branding concepts, wallpapers, and geometric vintage illustrations from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts, optional reference image UUIDs, and the Neta API token are sent to the TalesOfAI/Neta service.

Mitigation: Use only when sharing those inputs with the external image service is acceptable, and avoid including sensitive or private data in prompts or reference identifiers.

Risk: The token is passed on the command line and could be exposed in shared terminals, shell history, CI logs, or recordings.

Mitigation: Avoid using real tokens in shared or recorded environments, and rotate the token if it may have been exposed.

Risk: The skill depends on an external image generation API and installation source integrity.

Mitigation: Prefer a pinned or verified install path when available and review generated image outputs before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/art-deco-generator)
- [Neta API token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference image UUID parameters affect the generated image.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
