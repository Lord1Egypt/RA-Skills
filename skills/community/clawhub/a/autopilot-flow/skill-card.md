## Description: <br>
Autopilot Flow helps agents turn repeated work into automations through a six-step observe, abstract, design, implement, test, and optimize workflow with templates, error handling, monitoring, FAQ, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to identify repeated tasks, design repeatable automations, generate scripts or configurations, test with dry runs, and monitor ongoing reliability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages agents to build or enable automations proactively, including scripts, cron jobs, file moves, and email actions. <br>
Mitigation: Require the agent to describe affected files, accounts, schedules, external recipients, and production-data writes before execution, then approve cron jobs, watchers, email sends, and command execution explicitly. <br>
Risk: Automations may change real files, send messages, or write production data if tested directly against live systems. <br>
Mitigation: Use dry-run mode first, review generated outputs manually, and only enable live writes or external sends after the dry-run result is accepted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, YAML examples, and workflow templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose scripts, cron schedules, file watchers, notifications, and dry-run test plans for user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
