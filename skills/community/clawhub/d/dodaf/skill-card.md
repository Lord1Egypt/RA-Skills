## Description:

Create, verify, and document DoDAF 2.0/2.1 architecture models through a guided workflow that generates views, diagrams, checks, and consolidated reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsuhsuehi](https://clawhub.ai/user/hsuhsuehi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and defense engineering teams use this skill to scaffold DoDAF 2.0/2.1 architecture descriptions, collect stakeholder inputs, generate view products, and assemble review-ready reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic web research could expose or incorporate sensitive defense context when user input is insufficient.

Mitigation: Use only in a dedicated, non-sensitive workspace unless external searches are approved, and avoid classified or sensitive inputs.

Risk: The generated verification report may be mistaken for formal DoDAF compliance or defense architecture assurance.

Mitigation: Treat generated checks as scaffolding and require independent DoDAF or domain expert review before operational reliance.

Risk: Report generation writes project artifacts to user-selected locations and can invoke optional local conversion tools.

Mitigation: Review output directories and optional tool availability before execution.

## Reference(s):

- [DoDAF 2.0/2.1 Viewpoints Reference](references/dodaf-views.md)
- [draw.io Desktop](https://github.com/jgraph/drawio-desktop)
- [Pandoc Installation](https://pandoc.org/installing.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, draw.io diagram files, CSV matrices, and optional PDF, DOCX, or HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates project files under a user-selected output directory; PDF, DOCX, HTML, and diagram image export depend on optional local tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
