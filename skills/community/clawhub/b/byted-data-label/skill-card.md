## Description:

Byted Data Label helps agents operate Seederive to run LLM-based batch analysis on text, speech, and image datasets, including sentiment analysis, tag classification, opinion extraction, translation, content scoring, and prompt optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to preview, create, manage, and improve Seederive data-labeling workflows for CSV, Excel, or platform datasets. It guides agents through credential setup, task creation, tag-base management, result preview, model changes, and prompt optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation rules may cause the skill to run for many data-labeling or analysis requests.

Mitigation: Confirm the user intends to use Seederive before running commands or sending data.

Risk: The skill sends Volcengine credentials and user data to a configurable remote endpoint.

Mitigation: Use narrowly scoped credentials, keep the default endpoint unless an approved endpoint is required, and avoid processing sensitive datasets without approval.

Risk: Delete, model-change, task-change, and bulk-upload commands can alter remote Seederive state.

Mitigation: Require explicit manual confirmation before executing destructive or high-impact operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-data-label)
- [Seederive task workflow reference](references/task.md)
- [Seederive tag-base workflow reference](references/tag-base.md)
- [Seederive optimization workflow reference](references/optimize.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, CSV]

**Output Format:** [Markdown guidance with bash commands and JSON or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON or CSV files used as inputs to Seederive commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
