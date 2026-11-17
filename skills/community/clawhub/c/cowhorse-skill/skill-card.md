## Description:

A skill that actively extracts and quantifies workflow requirements from users through structured Q&A about inputs, outputs, and objectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spa3k](https://clawhub.ai/user/spa3k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow authors use this skill to turn repeated AI-supported tasks into reusable agent skills by clarifying goals, input and output specifications, process steps, constraints, and validation needs before building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent agent skills and scripts that may encode incorrect requirements or unsafe automation behavior.

Mitigation: Review generated SKILL.md files, scripts, and package contents before deployment, and scan generated artifacts before reuse.

Risk: Workflow discovery may capture credentials, private paths, schemas, business details, or other sensitive information in generated files or memory logs.

Mitigation: Keep generated files in a scoped workspace and avoid storing sensitive workflow details unless persistence is explicitly intended.

## Reference(s):

- [Workflow Patterns Reference](references/workflow_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands, Python helper output, and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent skill files, scripts, references, assets, packaging steps, and memory updates when the user confirms requirements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
