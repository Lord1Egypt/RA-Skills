## Description: <br>
飞书任务智能体 routes Feishu task creation, task polling, agent registration, and daily.json profile refresh workflows for an OpenClaw/Feishu workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tengchengwei](https://clawhub.ai/user/tengchengwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this agent to turn action items, deliverables, follow-ups, decomposition requests, and recurring requests into Feishu tasks, and to process eligible unfinished tasks from scheduled polling. It also supports explicit Feishu task-agent registration and refreshes daily.json from recent journal entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install persistent scheduled automation and broad workspace routing behavior. <br>
Mitigation: Review the cron jobs and AGENTS.md routing rule before registration, and keep registration limited to the explicit trigger described in the workflow. <br>
Risk: The skill can manage Feishu tasks and upload daily.json-derived profile content. <br>
Mitigation: Confirm the Feishu/OpenClaw account, task-tool permissions, and generated daily.json contents before allowing write actions. <br>


## Reference(s): <br>
- [Feishu Task Agent skill definition](SKILL.md) <br>
- [Task orchestration workflow](workflows/auto-task.md) <br>
- [Polled task execution workflow](workflows/polled-task-execution.md) <br>
- [Agent profile and daily.json workflow](workflows/agent-profile.md) <br>
- [Feishu task-agent registration workflow](workflows/reg.md) <br>
- [Task decision rules](references/task-decision-rules.md) <br>
- [Task output contract](references/task-output-contract.md) <br>
- [Profile data shape](references/profile-data-shape.md) <br>
- [ClawHub skill page](https://clawhub.ai/tengchengwei/feishu-task-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON contracts, and Feishu task update instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu tasks, comments, attachments, delivery links, cron jobs, AGENTS.md routing rules, and daily.json when invoked in a configured OpenClaw/Feishu environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
