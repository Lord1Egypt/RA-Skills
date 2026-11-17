## Description:

D&D 5e toolkit for players and DMs. Roll dice, look up spells and monsters, generate characters, create encounters, and spawn NPCs. Uses the official D&D 5e SRD API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:


## Use Case:

External players, dungeon masters, and agents use this skill to roll dice, look up SRD spells and monsters, and generate characters, encounters, and NPCs for D&D 5e play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spell, monster, character, and encounter commands make outbound requests to the public D&D 5e API.

Mitigation: Run the skill only in environments where public API access is acceptable and expect network failures to affect those commands.

Risk: Very large dice expressions can cause local resource exhaustion until input limits are added.

Mitigation: Avoid requesting extremely large dice rolls and prefer normal tabletop dice expressions.

## Reference(s):

- [D&D 5e API](https://www.dnd5eapi.co/)
- [D&D 5e API endpoint](https://www.dnd5eapi.co/api)
- [ClawHub skill page](https://clawhub.ai/capt-marbles/skills/dnd)
- [Publisher profile](https://clawhub.ai/user/capt-marbles)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands fetch public SRD data from the D&D 5e API; dice, character, encounter, and NPC outputs are randomized.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
