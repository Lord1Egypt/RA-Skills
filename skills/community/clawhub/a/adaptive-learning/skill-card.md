## Description:

Create adaptive learning flashcard apps from course materials using FSRS and Bayesian Knowledge Tracing for intelligent review scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weishuz](https://clawhub.ai/user/weishuz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and learners use this skill to turn course URLs, PDFs, or local folders into self-contained browser flashcard apps for spaced repetition, adaptive quizzes, and review planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted question JSON and course IDs can become executable browser content or unsafe output paths.

Mitigation: Use trusted course materials, validate course IDs and output paths before running the bundler, and review generated files before opening them.

Risk: Generated apps may run in a browser context that has sensitive same-origin data.

Mitigation: Open generated apps in an isolated browser profile or origin and avoid mixing them with sensitive local or same-origin browser data.

Risk: The framework loads KaTeX from a public CDN by default.

Mitigation: Vendor KaTeX locally or add subresource integrity and network-consent review before broader deployment.

## Reference(s):

- [Adaptive Learning ClawHub release](https://clawhub.ai/weishuz/skills/adaptive-learning)
- [FSRS algorithm reference](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm#fsrs-5)
- [KaTeX 0.16.9 CDN asset](https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON question banks, shell commands, and generated HTML/CSS/JavaScript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-contained browser study apps that store progress in localStorage and may load KaTeX assets from a CDN unless vendored locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
