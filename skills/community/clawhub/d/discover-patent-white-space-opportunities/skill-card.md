## Description:

Guides Chinese-language patent-map analysis to identify candidate whitespace, assess problem value, diagnose key contradictions, and propose logically grounded resolution directions while requiring user confirmation at major decision points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External patent analysts, innovation teams, and IP strategy users use this skill to review patent maps or sparse technical areas, select candidate whitespace with checkpoints, evaluate problem value, and produce structured contradiction-resolution analysis. The workflow can generate a self-contained HTML report after the staged analysis is complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent whitespace analysis and generated HTML reports may contain confidential strategy or portfolio information.

Mitigation: Review where @session/reports/ is stored and avoid saving a report when working with confidential material unless the user explicitly wants that artifact.

Risk: The workflow depends on a PatSnap/Zhihuiya MCP account for patent data access; without that configuration, conclusions may be limited to the user's supplied materials.

Mitigation: Confirm the required MCP account authorization and data-access scope before relying on database-backed findings.

## Reference(s):

- [Candidate whitespace evaluation framework](references/evaluation-framework.md)
- [Output templates](references/output-templates.md)
- [Zhihuiya open platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Markdown analysis with structured tables and optional self-contained HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before deep analysis and before contradiction diagnosis; final report may be saved under @session/reports/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
