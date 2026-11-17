## Description:

Generate Word documents by filling templates with content based on reference materials, preserving original styles and supporting table-heavy templates such as project proposals, lesson plans, curriculum standards, course outlines, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users use this skill to fill structured .docx templates from reference materials while preserving template styles. It is intended for table-heavy documents such as proposals, lesson plans, curriculum standards, course outlines, reports, and other formatted Word outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documents may silently lose table content if unfilled table cells are cleared or if placeholders and static text are not declared correctly.

Mitigation: Use an explicit output path in a scratch or workspace directory, keep backups of source templates, and manually compare generated documents against the source template for missing table text.

Risk: The renderer can overwrite arbitrary writable output files when a careless output path is supplied.

Mitigation: Choose a new output filename for each run and avoid using important existing file paths until overwrite behavior is reviewed.

Risk: Generated documents may be unsuitable for legal, financial, or approval workflows without review.

Mitigation: Avoid high-impact use until the renderer only changes explicitly declared placeholders and refuses unsafe overwrites by default; require human review before relying on generated content.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/neuhanli/skills/docx-fill)
- [Fill Contract Schema](references/fill_contract_schema.md)
- [Structure Agent](references/structure_agent.md)
- [Content Agent](references/content_agent.md)
- [Conflict Checker](references/conflict_checker.md)
- [Evaluator](references/evaluator.md)
- [Evaluation Rules](references/evaluation_rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JSON intermediate artifacts, shell commands, and generated .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured fill contracts and generated content JSON before rendering a Word document; final output preserves the source template format where validation passes.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
