## Description:

Generate full-body anime character images from text descriptions with customizable outfits, hairstyles, poses, image size, and optional style reference input through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate anime-style character illustrations for original characters, fan art, visual novels, profile avatars, and portraits from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accepts the Neta API token through command-line arguments, which can expose long-lived credentials in local shell history or process listings.

Mitigation: Use a short-lived or low-scope Neta token, avoid pasting long-lived tokens directly into commands, and rotate any token that may have been exposed.

Risk: The documented npx installer path is unpinned, so users may install a different future release than the one reviewed.

Mitigation: Prefer a pinned or ClawHub-managed install path and review the installed artifact before use.

Risk: Prompts and reference image UUIDs are sent to the Neta/TalesofAI service.

Mitigation: Do not submit sensitive prompts or private reference UUIDs unless sharing them with the service is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/skills/anime-character-generator)
- [Neta Token Setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text image URL with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and may use an optional reference image UUID for style inheritance.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
