## Description: <br>
Multi-agent task orchestration skill that coordinates review, execution, and audit loops with manual subtasks for simple work and reviewer-generated subtasks for complex work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run recurring multi-agent task workflows that break goals into subtasks, coordinate execution, apply review and audit gates, and package completed results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring unattended multi-agent execution may continue acting on task files without close operator attention. <br>
Mitigation: Install only when that behavior is intended, run it in an isolated workspace with a low-privilege coordinator agent, and remove heartbeat or cron jobs when the work is done. <br>
Risk: Generated task JSON and role prompts may cause agents to act on incorrect or unintended instructions. <br>
Mitigation: Manually review task JSON and generated prompts before letting reviewer, executor, or auditor agents proceed. <br>
Risk: Workspace credentials or production resources could be exposed to spawned agents during automated execution. <br>
Mitigation: Do not provide production credentials, and limit the workspace and agent permissions used for this skill. <br>


## Reference(s): <br>
- [Auto Evolution Skill Page](https://clawhub.ai/cjboy007/auto-evolution) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [task-example.json](references/task-example.json) <br>
- [Task JSON Schema](config/task-schema.json) <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON files] <br>
**Output Format:** [Markdown guidance with shell command snippets, JSON task files, and generated role prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one task or role handoff at a time for coordinator, reviewer, executor, auditor, monitor, and packaging workflows.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
