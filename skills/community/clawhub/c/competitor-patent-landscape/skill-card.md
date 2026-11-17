## Description:

Given a competitor company and technology field, this skill retrieves patent information, identifies core and peripheral patent strategy, and produces HTML/PDF patent landscape reports with product visualization for IP and R&D teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Enterprise IP teams, R&D engineers, and strategy analysts use this skill to study competitor patent activity in a technology area, identify core and peripheral patent coverage, and generate evidence-backed landscape reports for planning and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may render untrusted patent or search data into HTML/PDF.

Mitigation: Review inputs before report generation, run the generator in an isolated environment, and prefer a version that escapes report fields and validates analysis.json.

Risk: PDF rendering can fetch or process external resources when converting HTML.

Mitigation: Disable or tightly restrict WeasyPrint resource fetching and avoid opening generated HTML from untrusted inputs.

Risk: Patent strategy conclusions can be incomplete or misleading if live patent data access is unavailable or search results are sparse.

Mitigation: Confirm PatSnap MCP/OpenAPI configuration before use and require evidence-backed conclusions with patent numbers and source notes.

## Reference(s):

- [Competitor patent landscape workflow guide](references/workflow_guide.md)
- [PatSnap open platform](https://open.zhihuiya.com/)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/competitor-patent-landscape)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML/PDF report files with supporting structured analysis data and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report generation depends on configured PatSnap MCP/OpenAPI access for live patent data; when PDF rendering support is unavailable, the script falls back to HTML.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
