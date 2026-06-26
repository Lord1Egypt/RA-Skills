## Description: <br>
Use this skill when the user needs to design, critique, redesign, audit, generate, code, or explain quantitative graphics: charts, dashboards, tables, maps, scientific/statistical figures, visual evidence, or chart specifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to choose, critique, redesign, audit, generate, and explain quantitative displays such as charts, dashboards, tables, maps, and statistical figures. It emphasizes truthful quantitative reasoning, appropriate display selection, accessibility, and concrete improvements to comparison and interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled scripts inspect user-supplied data files for visualization recommendations, audits, contrast checks, or SVG generation. <br>
Mitigation: Run them only on files the user intends the agent to inspect, and avoid supplying sensitive datasets unless that exposure is acceptable. <br>
Risk: Generated chart audits, redesign guidance, SVGs, or handoff notes may be incorrect or incomplete for publication or decision use. <br>
Mitigation: Review outputs for units, denominators, source context, uncertainty, accessibility, and scale choices before using them in reports or publications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/display-quantitative-information) <br>
- [Principles](references/principles.md) <br>
- [Display Selection](references/display-selection.md) <br>
- [Integrity Audit](references/integrity-audit.md) <br>
- [Redesign Workflow](references/redesign-workflow.md) <br>
- [Chart Specification](references/chart-spec.md) <br>
- [Accessibility and Output](references/accessibility-and-output.md) <br>
- [Language and Variation](references/language-and-variation.md) <br>
- [Rubric](references/rubric.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON chart specifications, Python or shell commands, and SVG/chart handoff files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use optional local Python utilities for CSV inspection, display suggestions, integrity audits, lie-factor checks, contrast checks, SVG rendering, and critique-language review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
