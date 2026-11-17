## Description:

Feishu Batch Task Creator helps an agent create multiple Feishu tasks from templates, CSV-style inputs, and repeated task patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramlee77](https://clawhub.ai/user/ramlee77)

### License/Terms of Use:

MIT-0

## Use Case:

External users and team operators use this skill to have an agent prepare and create Feishu tasks in batches, including templated tasks, assignee fields, due dates, and recurring task parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk task creation can create many incorrect Feishu records if the target Bitable, assignees, due dates, or record count are wrong.

Mitigation: Confirm the target Bitable, assignees, due dates, and record count before executing batch creation.

Risk: Instructions include completing existing tasks, which could mark the wrong task as complete.

Mitigation: Review task identifiers and completion requests before applying updates to existing tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ramlee77/skills/feishu-batch-task)
- [Publisher profile](https://clawhub.ai/user/ramlee77)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with JSON task and Bitable parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu task fields, Bitable record payloads, assignee IDs, timestamps, and recurring-task rules.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
