## Description:

AIPPT Generator helps agents collect structured business presentation requirements, draft decision-oriented Markdown slide decks with native chart data, and export editable PowerPoint files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent-chao-lang](https://clawhub.ai/user/vincent-chao-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external business users, and agents use this skill to turn business inputs into professional presentation drafts for executive updates, client proposals, quarterly reviews, project reports, training sessions, and custom content-to-slide workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated business presentations may include incorrect or unsupported claims if the input data is incomplete or unreviewed.

Mitigation: Review the generated Markdown and deck against source business data before using it for decisions or external communication.

Risk: The skill creates editable PowerPoint files on disk at the requested output path.

Mitigation: Choose the output path deliberately and avoid writing sensitive decks into shared or unintended locations.

Risk: The PowerPoint export depends on python-pptx when generating .pptx files.

Mitigation: Install in a virtual environment and pin or review python-pptx before using the skill for sensitive business work.

## Reference(s):

- [Scenario Diagnostics](references/scenarios.md)
- [Prompt Templates](references/prompt_templates.md)
- [Styling Guide](references/styling_guide.md)
- [Example Output](references/example_output.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown slide draft with chart data blocks, plus optional editable .pptx file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks and built-in labels may be Chinese unless prompts or script settings are adapted; the export script writes editable .pptx files to a user-selected path.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
