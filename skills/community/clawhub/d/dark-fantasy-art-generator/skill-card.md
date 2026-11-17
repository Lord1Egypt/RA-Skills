## Description:

Generates dark fantasy, grimdark, and gothic horror image URLs from text prompts via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate dark fantasy, grimdark, and gothic horror artwork from short text prompts for creative projects such as tabletop campaigns, album covers, game concepts, and novel covers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference IDs, and the API token are sent to the external Neta/api.talesofai.com service.

Mitigation: Avoid submitting sensitive prompts or reference identifiers, and use tokens with the minimum needed scope and lifetime.

Risk: The npx installer path is not pinned in the provided usage examples.

Mitigation: Prefer the ClawHub install path, or verify and pin the package before installing with npx.

Risk: Passing a long-lived API token directly on the command line can expose it through shell history or process listings.

Mitigation: Use shell expansion or another safer credential handling method instead of typing raw long-lived tokens into commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/dark-fantasy-art-generator)
- [Neta AI token access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; accepts optional size and reference image UUID parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
