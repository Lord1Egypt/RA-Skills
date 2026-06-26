## Description: <br>
Manages an agent's context memory by checking session usage on wakeup, saving complete conversations when thresholds are reached, extracting structured memories, and running daily memory reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[csl3170](https://clawhub.ai/user/csl3170) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve long-running work by saving full conversations, extracting project memory, tracking user preferences and todos, and reviewing stored memory on a daily schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist complete chat histories and memory files that may contain sensitive conversations, project details, preferences, todos, or secrets accidentally shared in chat. <br>
Mitigation: Install only when durable local memory is intended, restrict access to the workspace, and periodically review or delete memory/chat, memory/projects, memory/archive, and MEMORY.md. <br>
Risk: The daily review flow uses fixed temporary report and log files that may expose memory metadata or drive later agent actions. <br>
Mitigation: Restrict access to /tmp/cmm_review_report.json and /tmp/cmm_review.log, consider disabling or editing the cron job, and review report contents before acting on them. <br>


## Reference(s): <br>
- [Model Context Windows](references/model-contexts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON review reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory files, MEMORY.md, crontab entries, and /tmp review report/log files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
