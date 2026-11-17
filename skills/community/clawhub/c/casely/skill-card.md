## Description:

Casely is an intelligent QA assistant that turns project requirements and example test cases into style-consistent test plans, Markdown test cases, and Excel exports for test management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnwayneeee](https://clawhub.ai/user/johnwayneeee)

### License/Terms of Use:

MIT

## Use Case:

QA engineers, test automation engineers, and development teams use Casely to parse requirement documents, learn the team's existing test case structure, generate atomic test cases, and export them as Excel files for test management systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow may create project files and modify the repository Python environment.

Mitigation: Run setup in an isolated workspace and review or pin dependencies before using /init.

Risk: The skill reads requirement and example documents that may contain sensitive product or customer information.

Mitigation: Use sanitized inputs where possible and confirm the workspace and generated outputs follow the team's data handling policy.

Risk: Generated Excel exports may carry values that spreadsheet tools can interpret as formulas.

Mitigation: Treat XLSX exports as untrusted until values beginning with formula-triggering characters are escaped before sharing or import.

## Reference(s):

- [Parser Usage Guide](references/parser_usage.md)
- [Export Guide](references/export_guide.md)
- [Test Style Analysis Methodology](references/style_analysis_prompts.md)
- [ClawHub Skill Page](https://clawhub.ai/johnwayneeee/skills/casely)
- [Repository](https://github.com/JohnWayneeee/casely-qa-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with generated Markdown test case files and XLSX exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates project folders, parsed Markdown files, a test style guide, a test plan, per-case Markdown files, and one Excel workbook per generated test case.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
