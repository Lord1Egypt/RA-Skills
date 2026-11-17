## Description: <br>
Guides agents in using cron-style reminder workflows, including session-start checks, timezone handling, basic reminder patterns, and common scheduling pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create local reminder workflows, check due tasks at session start, and avoid common scheduling mistakes such as timezone drift, DST assumptions, month-end dates, and concurrent execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder examples can manage local reminder files and update them when an agent session starts. <br>
Mitigation: Review the storage path and generated reminder data before allowing the agent to run or modify local reminder files. <br>
Risk: Timezone guidance claims offset-aware storage, but the examples use naive Python datetimes. <br>
Mitigation: Adapt the examples to store explicit timezone offsets before relying on reminders for important deadlines, especially outside Asia/Shanghai. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and local command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples may create or update local reminder JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
