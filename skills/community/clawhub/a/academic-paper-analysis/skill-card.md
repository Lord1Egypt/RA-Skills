## Description:

Provides structured, in-depth analysis of epidemiology, biostatistics, and public health academic papers, including term explanations, method interpretation, results analysis, and table layout extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chircken891](https://clawhub.ai/user/chircken891)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to analyze academic papers in epidemiology, biostatistics, and public health with detailed explanations of terminology, study design, statistical methods, results, limitations, and table structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to retain table-layout information from every analyzed paper in a hardcoded local database path without consent or retention controls.

Mitigation: Use only with papers whose table-layout retention is acceptable, and avoid confidential, unpublished, proprietary, or copyrighted papers unless persistence is removed or made explicit, optional, and deletable.

## Reference(s):

- [Academic Paper Analysis on ClawHub](https://clawhub.ai/chircken891/skills/academic-paper-analysis)
- [OpenClaw ClawHub](https://github.com/openclaw/clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown with structured analysis sections and bilingual excerpts when analyzing English papers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted table layout descriptions; artifact behavior indicates table-layout information is written to a hardcoded local database path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
