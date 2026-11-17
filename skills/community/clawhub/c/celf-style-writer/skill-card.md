## Description:

Cell 风格写作 helps agents write, rewrite, enhance, or review Chinese content in Cell's friend-to-friend style while preserving truthful source meaning and avoiding academic or AI-template phrasing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to produce, reshape, or audit Chinese prose so it matches Cell's warm, concrete, lightly sharp writing style. It supports new drafts, rewrites, style enhancement, and style diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is tailored to a specific Chinese writing voice and may produce an unsuitable style for other languages or less personalized writing tasks.

Mitigation: Explicitly override the requested language, tone, or style when the Cell voice is not desired.

Risk: Generated prose could add unsupported personal details, quotes, data, or evidence if the source material is thin.

Mitigation: Require source-grounded details for personal experience and verifiable claims, and review final text against the artifact's truthfulness and no-fabrication rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cellinlab/skills/celf-style-writer)
- [Skill homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/celf-style-writer)
- [Content Method](references/content-method.md)
- [Personal Variables](references/personal-variables.md)
- [Quality Bar](references/quality-bar.md)
- [Style Skeleton](references/style-skeleton.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown Chinese prose with optional style review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; responses are writing, rewriting, enhancement, or review guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
