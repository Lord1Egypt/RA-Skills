## Description:

A Chinese-language compensation analysis skill for salary benchmarking, raise planning, pay equity analysis, compensation structure design, market percentile analysis, salary band design, and compensation competitiveness assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

HR and compensation practitioners use this skill to produce structured compensation analyses, including market benchmarking, raise allocation, internal pay equity review, and compensation structure recommendations. It is designed for Chief-mediated specialist use and can fall back to scoped direct use when called independently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is expected to handle sensitive HR salary and employee compensation data.

Mitigation: Provide only necessary fields, anonymize employee identifiers where possible, and treat compensation inputs and outputs as confidential.

Risk: Compensation recommendations can be misleading if market data, internal salary records, performance data, or job matching inputs are stale or incomplete.

Mitigation: Require users to label data sources, sample sizes, years, assumptions, and confidence levels before relying on recommendations.

Risk: The skill primarily produces Chinese-language compensation analysis, which may not match every user's preferred output language.

Mitigation: Confirm the desired output language when users do not want Chinese responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/diting-compensation-expert)
- [Output templates](references/output-templates.md)
- [Compensation analysis tools](references/tools.md)
- [Classic compensation books](references/classic-books.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown reports, tables, checklists, and occasional Python calculation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language compensation analysis with conclusions, risk notes, confidence statements, and data-source caveats]

## Skill Version(s):

2.1.2 (source: server release metadata; artifact frontmatter reports 2.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
