## Description: <br>
Automation Recipe Book helps agents create, validate, debug, share, and manage persistent automation recipes for personal, team, and enterprise workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and business teams use this skill to generate and operate automation recipes for recurring tasks, workflow orchestration, notifications, content operations, data processing, approvals, and reporting. It is intended for agents that can read, write, and run shell commands in supported agent environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags broad write and command authority for persistent workflow automation without enough scoping or review controls. <br>
Mitigation: Install only when persistent automation recipe management is intended, and review generated or imported recipes before enabling them. <br>
Risk: Generated or imported recipes may run commands, write files, send notifications, post content, or touch business systems. <br>
Mitigation: Apply least-privilege execution, inspect recipes that perform side effects, and test with dry runs or mock inputs before production use. <br>
Risk: Community recipes may introduce unintended behavior or unsafe integrations. <br>
Mitigation: Review community-sourced recipes and their required skills or external services before import or installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/automation-recipe-book) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, JSON, text, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate persistent automation recipe files, validation guidance, debugging instructions, and workflow configuration suggestions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
