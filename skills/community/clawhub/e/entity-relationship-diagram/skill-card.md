## Description:

Turns described domains into ready-to-render Mermaid entity-relationship diagrams with entities, relationships, cardinality, key attributes, and design notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data modelers, and database designers use this skill to turn a described domain into a Mermaid ER diagram for schema design, table relationship review, and data-model communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated diagrams may contain inaccurate entities, relationships, cardinalities, or attribute choices when the source domain details are incomplete.

Mitigation: Review the diagram against domain requirements before using it for schema implementation or migration planning.

Risk: Mermaid ER output may fail to render if cardinality notation, entity blocks, or spaced relationship labels are malformed.

Mitigation: Check that the Mermaid block renders and that relationship labels with spaces are quoted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/entity-relationship-diagram)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/entity-relationship-diagram.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with a Mermaid erDiagram code block and concise design notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Mermaid output should use explicit crow's-foot cardinality, PK/FK markers, and focused attributes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
