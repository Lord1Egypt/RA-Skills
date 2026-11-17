## Description:

食品与餐饮合规专家 routes pasted food and catering tables to one of six local checks and returns row-level, reproducible conclusions or missing-input notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Food production, catering, canteen, lab, finance, and compliance staff use this skill to check pasted table records for BOM variance, procurement and sample-retention records, factory inspection records, additive usage, fresh-loss variance, and sample custody issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's Chinese compliance output is advisory and may not satisfy legal, regulatory, food-safety, or audit review requirements.

Mitigation: Use it as a table-checking aid and have qualified compliance, food-safety, legal, or audit reviewers validate decisions before relying on the result.

Risk: The local runner creates a usage-count file in the user's home directory.

Mitigation: Inform users before execution and run in an appropriate local environment if home-directory writes are restricted.

Risk: Incomplete or ambiguous table headers can lead to no conclusion or only a subset of checks being executed.

Mitigation: Provide table headers with data rows, review missing-column and unexecuted-check messages, and rerun with complete inputs or a specific sub-skill when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-food-catering-pub)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text by default, or JSON when the runner is invoked with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs identify the selected sub-skill and include row-level findings when the supplied table has sufficient columns.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
