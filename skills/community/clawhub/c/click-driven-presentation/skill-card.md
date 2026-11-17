## Description:

Turns an existing narration script into a click-driven, full-screen Vite and React web presentation that the speaker advances one beat at a time and records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and content creators use this skill to convert an existing narration script into a talk-driven web presentation with one focused idea per click. It is useful for recording dynamic presentations or presenting them live without locking pacing into a rendered video timeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold creates and modifies files in a local presentation project directory.

Mitigation: Use a fresh target directory and avoid --force unless overwriting existing files is intentional.

Risk: The scaffold may run npm install for the generated Vite, React, and TypeScript project.

Mitigation: Use --no-install to inspect the scaffold first, then install dependencies only if the project contents are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/click-driven-presentation)
- [README](artifact/README.md)
- [Scene Craft](artifact/references/SCENE-CRAFT.md)
- [Steps Spec](artifact/references/STEPS-SPEC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript, React, CSS, configuration files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local Vite + React + TypeScript presentation project with click and keyboard step navigation, token-based theming, and per-scene steps data.]

## Skill Version(s):

0.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
