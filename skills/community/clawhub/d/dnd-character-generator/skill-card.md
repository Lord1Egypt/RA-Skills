## Description:

Generate cinematic D&D character portraits and tabletop RPG hero art from a text description using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate Dungeons & Dragons and tabletop RPG character art from text prompts, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A command-line parsing bug can accidentally send the user's API token as image prompt text.

Mitigation: Place the character description before --token, avoid token-only invocations until parsing is fixed, and use only a token acceptable for use with the Neta/Tales of AI service.

Risk: Unpinned npx installation can install a moving package version.

Mitigation: Prefer a pinned package version or a ClawHub-managed install path for repeatable installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/dnd-character-generator)
- [Publisher profile](https://clawhub.ai/user/omactiengartelle)
- [Neta API token page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with optional Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall image size options.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
