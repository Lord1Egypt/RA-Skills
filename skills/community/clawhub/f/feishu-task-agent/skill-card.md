## Description:

飞书任务智能体 routes Feishu task creation, unfinished-task polling, agent registration, and daily.json profile refresh requests into the appropriate workflow for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tengchengwei](https://clawhub.ai/user/tengchengwei)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and Feishu workspace operators use this skill to turn user requests into Feishu tasks, manage recurring task execution, register the Feishu task agent, and refresh a daily profile summary from local journal Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automation and workspace routing changes can affect future agent behavior or run recurring Feishu task jobs.

Mitigation: Review cron jobs, scheduled-message payloads, and AGENTS.md changes before enabling the skill, and use a constrained workspace for deployment.

Risk: Local date-named Markdown files can be summarized into daily.json and published to the Feishu task agent profile.

Mitigation: Keep only intended journal files under the app root and avoid sensitive date-named Markdown files in directories scanned by the profile workflow.

Risk: The skill can create and update Feishu tasks, comments, attachments, text deliveries, and task status fields.

Mitigation: Confirm the intended Feishu account, assignee, follower set, and application identity before allowing task creation or delivery updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tengchengwei/skills/feishu-task-agent)
- [Task decision rules](artifact/references/task-decision-rules.md)
- [Creator / Members Output Contract](artifact/references/task-output-contract.md)
- [daily.json data shape](artifact/references/profile-data-shape.md)
- [Profile discovery rules](artifact/references/profile-discovery-rules.md)
- [Profile schedule rules](artifact/references/profile-schedule-rules.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Configuration, Markdown, Files]

**Output Format:** [Markdown guidance with shell command examples, JSON contracts, and file output descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Feishu tasks, task comments, attachments, text deliveries, OpenClaw cron jobs, workspace routing text, and daily.json when executed in a Feishu/OpenClaw environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
