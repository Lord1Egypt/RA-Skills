## Description:

Generates draw.io diagrams with type-specific templates and a mandatory visual QA loop for flowcharts, ERDs, architecture diagrams, sequence diagrams, and class diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spotlight-revenue](https://clawhub.ai/user/spotlight-revenue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and technical teams use this skill to create or update draw.io diagrams for workflows, database schemas, system architecture, sequences, and UML class models, then export reviewed image or editable file formats for sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create local diagram files and exported images under a diagrams folder.

Mitigation: Review output paths and generated files before sharing, committing, or running the skill in sensitive repositories or shared folders.

Risk: The skill may run local draw.io or xvfb-run export tools.

Mitigation: Use trusted local installations and run exports with only the workspace permissions needed for the diagram task.

Risk: draw.io layouts use hardcoded positions, so generated diagrams can contain overlap, clipping, or misleading routing if not reviewed.

Mitigation: Complete the documented visual QA loop, inspect affected sections at full size, and re-export after fixes before delivery.

## Reference(s):

- [Box Style Standards](references/box-style-standards.md)
- [Visual Review Protocol](references/visual-review-protocol.md)
- [Diagram Workflow SOP](references/workflow-sop.md)
- [Flowchart / Process Flow / SOP Reference](references/diagram-types/flowchart.md)
- [ERD / Database Diagram Reference](references/diagram-types/erd.md)
- [UML Class Diagram Reference](references/diagram-types/class.md)
- [Sequence Diagram Reference](references/diagram-types/sequence.md)
- [Architecture / System Diagram Reference](references/diagram-types/layout.md)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [draw.io XML files, exported diagram assets, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local diagram assets under a diagrams folder and may export PNG, SVG, or PDF when draw.io is installed.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
