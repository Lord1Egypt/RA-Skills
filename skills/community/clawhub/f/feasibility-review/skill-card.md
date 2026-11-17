## Description:

Feasibility Review helps agents review uploaded feasibility-study reports by checking document quality and substantive project evidence, then generating a structured project-approval review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Science and technology project managers and review teams use this skill to evaluate feasibility-study reports for document completeness, consistency with project guidance, technical routes, innovation claims, patent and paper evidence, policy fit, and final project-approval recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce incorrect or misleading review conclusions if generated analyses are not checked against the uploaded feasibility report and retrieved evidence.

Mitigation: Review the generated report, source citations, charts, and project-rating rationale before using it for approval decisions.

Risk: The optional exporter writes review.json to a caller-selected directory and can overwrite an existing file at that path.

Mitigation: Run scripts/export_json.py only with an output directory you control and preserve any existing review.json before exporting.

Risk: The workflow depends on PatSnap/MCP and policy-search access, so broad or reused credentials could expose unrelated data or capabilities.

Mitigation: Use credentials scoped to this review workflow and confirm the required MCP tools are configured before execution.

## Reference(s):

- [ClawHub skill page: feasibility-review](https://clawhub.ai/yuanzhian-patsnap/skills/feasibility-review)
- [State Council policy document library](https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Self-contained HTML report with embedded charts, optional JSON export data, and a concise local-path summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates review_pipeline.py during execution and may export review.json to a caller-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
