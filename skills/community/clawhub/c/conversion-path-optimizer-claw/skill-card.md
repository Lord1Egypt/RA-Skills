## Description:

转化路径优化虾 analyzes sales funnels, mines high-converting sales scripts, and gives optimization recommendations for sales teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Sales operations teams, revenue leaders, and developers use this skill to analyze CRM exports or conversation records, identify funnel drop-off points, recommend sales scripts, and design A/B tests for sales conversion improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM exports and conversation logs may contain customer names, phone numbers, or other sensitive business data.

Mitigation: Use only data the user is allowed to analyze and remove sensitive fields where possible before running the skill.

Risk: Generated reports or Feishu documents may disclose business data if exported without review.

Mitigation: Confirm with the user before exporting reports or creating shared documents that contain CRM-derived information.

Risk: The scripts require local Python dependencies for spreadsheet and CSV processing.

Mitigation: Install dependencies in a virtual environment before executing the bundled analysis scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/conversion-path-optimizer-claw)
- [Sales funnel modeling guide](references/funnel-modeling.md)
- [Sales script mining algorithms](references/script-mining.md)
- [Sales script evaluation framework](references/script-evaluation.md)
- [Industry sales script templates](references/industry-templates.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown reports with optional shell commands and generated report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce funnel reports, ranked script recommendations, structured playbooks, and user-requested exported reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
