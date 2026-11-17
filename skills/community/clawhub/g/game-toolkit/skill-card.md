## Description:

Generates runnable browser game prototypes from a short game concept, including game logic, levels, controls, visual effects, and optional 2D or 3D rendering choices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and game teams use this skill to turn a concept or design brief into a playable HTML game prototype for rapid ideation, playtesting, and iteration. It is best suited for prototype generation and gameplay validation rather than decisions that require human judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release was flagged as suspicious because it requests command and file authority beyond the core game-generation task.

Mitigation: Install and run it only in a workspace where file writes and possible command execution are acceptable; review proposed commands and generated files before use.

Risk: The evidence notes external API or network behavior beyond a clearly scoped need.

Mitigation: Avoid providing secrets or sensitive project data, and confirm command and network boundaries with the publisher before using the skill in sensitive environments.

Risk: Generated game code may contain logic, performance, accessibility, or content issues that are not obvious from the prompt.

Mitigation: Review, test, and scan generated games before distribution or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/game-toolkit)
- [Node.js](https://nodejs.org/)
- [npm](https://www.npmjs.com/)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown and JSON describing runnable HTML, JavaScript, CSS, game metadata, controls, and generated feature details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a self-contained HTML browser game, prototype code, generated level data, visual or audio effect logic, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
