## Description:

横纵研究工作台 guides Chinese-language deep research by combining a vertical timeline, a horizontal comparison set, and crossing insights into a structured report or optional PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research a product, company, concept, technology, market, or person through a dual-axis method. It helps produce Chinese-language Markdown research reports that separate facts, inferences, and unknowns, with optional PDF export for formal delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional PDF export can be risky when processing untrusted Markdown reports.

Mitigation: Use trusted Markdown only for PDF export, or run conversion in a constrained directory or sandbox when processing user-supplied reports.

Risk: Dependency installation advice includes --break-system-packages, which can affect the system Python environment.

Mitigation: Install Markdown and WeasyPrint dependencies in a virtual environment and avoid --break-system-packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cellinlab/skills/cell-horizontal-vertical-analysis)
- [Workflow](references/workflow.md)
- [Source Strategy](references/source-strategy.md)
- [Analysis Lenses](references/analysis-lenses.md)
- [Report Contract](references/report-contract.md)
- [Research Schema](references/research-schema.json)
- [Research Report Template](assets/research-report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, code, shell commands, configuration]

**Output Format:** [Chinese-language Markdown report, optional PDF or HTML export, and structured research notes when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default report depth is standard; quick and deep modes are also documented.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
