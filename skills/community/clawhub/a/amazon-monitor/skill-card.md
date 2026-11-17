## Description:

Amazon product monitoring skill for tracking owned products and competitors with price tracking, review analysis, competitor comparison, trend visualization, and operational recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[backtoyoung](https://clawhub.ai/user/backtoyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and operations teams use this skill to collect product and competitor metrics, schedule monitoring tasks, generate trend charts, and produce comparison reports for pricing and marketplace decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence rates the release suspicious because file-writing behavior is under-scoped and ASIN input can influence output paths.

Mitigation: Run the skill in a limited workspace or virtual environment, use only valid 10-character ASINs from trusted sources, and prefer a patched version that validates ASINs and writes only to a dedicated data directory.

Risk: The skill performs Amazon scraping and creates local files during monitoring and reporting.

Mitigation: Install only when that behavior is acceptable for the deployment environment, and review generated files before relying on the results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/backtoyoung/skills/amazon-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and generated local JSON, PNG, and text report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local product history, task configuration, trend chart, and competitor analysis files when its scripts are executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
