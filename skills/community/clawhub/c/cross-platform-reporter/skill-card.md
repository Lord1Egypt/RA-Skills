## Description:

Cross Platform Reporter collects operations metrics from Xialiao, AIWay, MEYO, Tieba, and DingTalk to generate structured weekly reports and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bdz2007-antgroup](https://clawhub.ai/user/bdz2007-antgroup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to consolidate multi-platform engagement metrics, produce weekly reporting, and summarize trends for content and community operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled collection across multiple platforms may gather account or channel data beyond the intended scope.

Mitigation: Use the skill only with accounts and channels the user controls, and define the collection scope before enabling scheduled runs.

Risk: Local state storage in accounts-state.json may retain operational account metrics without clear retention controls.

Mitigation: Confirm the storage location, access controls, and retention period for accounts-state.json before deployment.

Risk: Automatic MEYO publication may expose reports before review.

Mitigation: Require manual review and approval before MEYO publication until opt-in, retention, and disable controls are documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bdz2007-antgroup/skills/cross-platform-reporter)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports with JSON state file references and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured weekly report sections, trend analysis, and proposed publication steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
