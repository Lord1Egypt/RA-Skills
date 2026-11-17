## Description:

Ai Literacy Expert V4.3 helps teachers and learners create AI-literacy lessons, p5.js interactive courseware and games, and guided lesson-prep packages with Excel, Word, PPT, PDF, and zip outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gqliang2026](https://clawhub.ai/user/gqliang2026)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, students, and education-content developers use this skill to explain AI concepts, design course modules, build browser-based interactive teaching assets, and generate structured lesson-prep document packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production logging guidance may capture user input or behavior without sufficient privacy controls.

Mitigation: Require opt-in or clearly disclosed telemetry, remove raw user input from logs, and define retention, deletion, and access-control rules before deployment.

Risk: The validation workflow references an unpinned package-execution command.

Mitigation: Replace `npx -y acorn` with a pinned package version or a built-in validation method before use in managed environments.

Risk: Educational and generated code outputs may be incorrect or unsuitable for a specific school, training, or enterprise context.

Mitigation: Review lesson content, generated HTML, and downloadable document packages before classroom or enterprise deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gqliang2026/skills/ai-literacy-expert-v4)
- [Commercial production standards](references/commercial-production-standards.md)
- [Interactive lesson builder guide](references/interactive-lesson-builder-guide.md)
- [Lesson-prep workflow](references/lesson-prep-workflow.md)
- [p5.js courseware guide](references/p5js-courseware-guide.md)
- [p5.js game design guide](references/p5js-game-design-guide.md)
- [Course asset index](references/kb-asset-index.md)
- [Module A cognition reference](references/module-a-cognition.md)
- [Module B tools reference](references/module-b-tools.md)
- [Module C methodology reference](references/module-c-methodology.md)
- [Module D practice reference](references/module-d-practice.md)
- [Module E professional reference](references/module-e-professional.md)
- [Professional orientation lecture script](references/lecture-script-professional-orientation.md)
- [p5.js task template](references/p5js-task-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with generated single-file HTML, p5.js code, and lesson-package instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser-based courseware, game, and lesson-prep artifacts; generated outputs should be reviewed before classroom or enterprise deployment.]

## Skill Version(s):

4.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
