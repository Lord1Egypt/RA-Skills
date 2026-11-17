## Description:

Translate technical & legal documents while preserving original formatting, terminology consistency, and domain context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and documentation teams use this skill to translate technical, legal, marketing, and general documents while preserving structure, code blocks, links, tables, and terminology consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current CLI can falsely report successful translation or validation.

Mitigation: Review generated translations and consistency reports manually, and do not rely on PASS output for legal, technical, or publication workflows.

Risk: The current CLI has unsafe filename handling.

Mitigation: Avoid running it on files from untrusted sources until filename handling is fixed and retested.

Risk: Legal translations may be mistaken for certified legal translations.

Mitigation: Use the legal disclaimer from the skill materials and have legally binding translations reviewed by a qualified legal translator.

## Reference(s):

- [Domain Translation Modes](references/domain-modes.json)
- [Input Schema](schemas/input.schema.json)
- [Output Schema](schemas/output.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/document-translation-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON reports, and copied document files depending on the requested workflow step.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce bilingual or translated-only document views, terminology glossaries, consistency reports, and format-preservation checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
