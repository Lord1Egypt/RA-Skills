## Description:

AI fantasy map generator for worldbuilders, tabletop RPG campaigns, and game designers that creates fantasy world maps, dungeon maps, kingdom maps, and lore art through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, tabletop RPG players, worldbuilders, and game designers use this skill to generate fantasy map image URLs from text prompts with optional size and style-reference controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and token-authenticated requests are sent to the Neta/Tales of AI API.

Mitigation: Use the skill only with prompts appropriate for that external service, and avoid secrets or confidential creative material.

Risk: The documented --token flag can expose an API token through command history, process listings, or logs.

Mitigation: Prefer a low-scope or disposable token and avoid pasting long-lived credentials into shared shells or logged environments.

Risk: The documented npx install command is unpinned, so future upstream changes could affect installed behavior.

Mitigation: Review the skill before installing and pin or verify the intended release where the installation environment supports it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/fantasy-map-generator)
- [Neta API access page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text image URL, with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports optional size and reference image UUID arguments.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
