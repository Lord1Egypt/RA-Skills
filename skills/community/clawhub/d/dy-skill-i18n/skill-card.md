## Description:

Helps agents internationalize frontend UI copy by finding hardcoded static text, reusing or adding locale entries, replacing strings with project-specific i18n calls, and checking translation completeness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyaoqi](https://clawhub.ai/user/anyaoqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to convert frontend projects to internationalized UI copy while preserving existing project structure, locale-file conventions, and i18n call patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to modify frontend source files and locale files.

Mitigation: Review generated diffs before committing and run the target project's lint, tests, or UI validation workflow where available.

Risk: Translation changes can introduce inaccurate, inconsistent, or layout-breaking UI copy.

Mitigation: Check terminology consistency, supported-language key parity, spelling, grammar, and UI fit after edits.

Risk: Translated HTML rendered with v-html can create XSS exposure if content is not trusted.

Mitigation: Prefer normal text rendering; only use HTML rendering for trusted or sanitized content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyaoqi/skills/dy-skill-i18n)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands]

**Output Format:** [Markdown guidance with inline code examples and project file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should follow the target project's existing internationalization structure, naming conventions, and validation workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
