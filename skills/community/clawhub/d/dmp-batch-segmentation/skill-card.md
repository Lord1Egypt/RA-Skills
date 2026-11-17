## Description:

Helps DMP operators create and track batches of location-based and rule-combined audience segments through the 明日 DMP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

DMP operators and marketing teams use this skill to split large location lists or combinations of tags and existing audiences into manageable segmentation jobs, then track their progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DMP account credentials are stored locally and grant account access.

Mitigation: Use a secure secret store rather than pasting long-lived AK/SK into chat; grant only the access needed.

Risk: A bundled monitor can run persistently and includes a preloaded monitoring task.

Mitigation: Review and disable the monitor unless needed, and remove the preloaded task before use.

Risk: Optional chat or email webhooks can transmit task metadata externally.

Mitigation: Keep notifications off unless needed; review recipients and the task data shared.

Risk: The workflow can install additional skills.

Mitigation: Review each dependency and approve its installation separately.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mingri26/skills/dmp-batch-segmentation)
- [Tag search and ambiguity handling](references/标签搜索歧义处理规则.md)
- [DMP authentication skill dependency](https://clawhub.ai/mingri26/mingdata-dmp-auth)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with task progress, setup instructions, and commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save project plans and task statuses as JSON files.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
