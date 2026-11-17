## Description:

Generates a random Arknights operator agent with lore-based personality using gacha probabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hg-hg](https://clawhub.ai/user/hg-hg)

### License/Terms of Use:


## Use Case:

External users and roleplay agent developers use this skill to pull a random Arknights operator, create an OpenClaw agent workspace, generate lore-grounded persona files, and start an in-character greeting session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A gacha request can automatically create a persistent OpenClaw agent and workspace.

Mitigation: Install only where durable agent creation is acceptable, and remove unwanted generated workspaces after review.

Risk: Generated persona files are derived from externally editable wiki pages.

Mitigation: Review SOUL.md and IDENTITY.md before using the generated agent, and restrict the generated agent's tools.

Risk: The workflow downloads wiki-hosted avatar assets and commits generated files.

Mitigation: Review downloaded assets and committed files before further use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hg-hg/skills/arknights-operator-gacha)
- [Arknights Fandom operator list pattern](https://arknights.fandom.com/wiki/Operator/{star}-star)
- [PRTS Wiki operator pages](https://prts.wiki/w/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown persona files, JSON worker result, shell command execution, and roleplay text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a durable OpenClaw agent workspace, downloads wiki-hosted assets, commits generated files, and spawns the generated agent.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
