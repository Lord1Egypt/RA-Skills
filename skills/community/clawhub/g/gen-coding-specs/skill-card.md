## Description:

Generates project-specific coding standards from bundled templates and writes Markdown specifications under docs/coding-specs for use by gen-code and related skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lf951515851](https://clawhub.ai/user/lf951515851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to generate a consistent set of project coding-specification documents covering architecture, APIs, data models, Vue, testing, security, performance, documentation, code review, and version control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated coding standards may include security guidance that is too generic or contains weak encryption examples.

Mitigation: Review generated security guidance before adoption and replace encryption examples with project-approved cryptography patterns.

Risk: Generated version-control guidance includes rollback commands that can discard local work if used incorrectly.

Mitigation: Require human review before following destructive rollback guidance and prefer non-destructive recovery commands unless explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lf951515851/skills/gen-coding-specs)
- [Skill definition](artifact/SKILL.md)
- [Generation workflow prompt](artifact/prompt.md)
- [Template overview](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Shell commands]

**Output Format:** [Markdown files under docs/coding-specs with concise status guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated specifications should be reviewed before adoption; existing files may be overwritten when regeneration is confirmed or forced.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
