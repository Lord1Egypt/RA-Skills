## Description:

Generates and validates recursive, multi-modal creative narratives using a five-layer specification system inspired by Godel, Escher, and Bach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiyangzen](https://clawhub.ai/user/weiyangzen)

### License/Terms of Use:

MIT

## Use Case:

Creative practitioners, developers, and agents use this skill to design stories, films, games, music, or visual narratives with recursive structure and cross-modal consistency checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project initialization helpers create local folders and README files in the current workspace.

Mitigation: Run initialization only in the workspace where new creative project files should be created.

Risk: Creative consistency checks may produce subjective guidance that does not match a project's artistic intent.

Mitigation: Review generated specifications and consistency guidance before using them in production creative work.

## Reference(s):

- [GEB Aesthetics on ClawHub](https://clawhub.ai/weiyangzen/skills/geb-aesthetics)
- [Skill Specification](SKILL.md)
- [GEB Philosophy](docs/PHILOSOPHY.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project folders when initialization helpers are run.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
