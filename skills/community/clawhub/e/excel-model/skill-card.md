## Description:

Build a real, formula-driven Excel (.xlsx) model, not a static table, for financial models, budgets, forecasts, scenario planners, and other editable workbooks with live formulas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to design and generate editable Excel workbook models with centralized assumptions, calculation sheets, live formulas, formatting, and a short model README.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a code-execution environment to create Excel files.

Mitigation: Review generated scripts before running them and execute them only in an appropriate code-execution environment.

Risk: The referenced helper script is missing from the artifact, so functionality may depend on the agent generating its own openpyxl script.

Mitigation: Verify the generated workbook opens correctly and contains live formulas; use a markdown model specification when code execution is unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/excel-model)
- [Excel Model Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/excel-model.html)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Markdown, Guidance]

**Output Format:** [Excel .xlsx workbook plus Markdown README and generated Python/openpyxl script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a code-execution environment; if code execution is unavailable, the skill falls back to a markdown model specification.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
