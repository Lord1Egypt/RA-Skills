## Description:

Generates album cover images from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate album cover artwork from a text prompt, optionally selecting image size and using a reference image UUID for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens can be exposed when placed directly on the command line or when users install from an unpinned source.

Mitigation: Use NETA_TOKEN or a secret manager for the token, and prefer the ClawHub install path or a pinned verified source.

Risk: Prompts and reference image identifiers are sent to an external image generation API.

Mitigation: Avoid submitting sensitive personal data or confidential creative prompts unless the external service's handling of that data is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/skills/album-cover-skill)
- [Neta AI API Access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text image URL printed to stdout, with errors printed to stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token through NETA_TOKEN or --token; supports square, portrait, landscape, and tall output sizes.]

## Skill Version(s):

1.5.7 (source: server evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
