## Description:

Write AI-citable content in proven formats including FAQ pages, definition articles ("What is X?"), comparison guides (A vs B), how-to guides, and original data/statistics roundups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:


## Use Case:

External content teams and marketers use this skill to draft AI-citable content structures such as FAQ pages, definition articles, comparison guides, how-to guides, and statistics roundups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included Python generator is incomplete for FAQ, comparison, how-to, and statistics formats.

Mitigation: Use the documented Markdown structures for those formats or review generated output before publishing.

Risk: Using --output may overwrite the file path provided by the user.

Mitigation: Write to a new or disposable path, or confirm the target file can be replaced before running the generator.

## Reference(s):

- [AI Vocabulary Blacklist](references/ai-vocabulary.md)
- [AI Citation Content Writer on ClawHub](https://clawhub.ai/geoly-geo/skills/geo-citation-writer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with content templates, inline shell commands, and writing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled generator currently implements the definition template and may overwrite the path provided with --output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
