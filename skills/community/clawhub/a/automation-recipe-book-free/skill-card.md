## Description: <br>
Provides eight ready-to-use automation recipe templates for common workflows such as news summaries, email replies, price monitoring, content publishing, data backup, and scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, small teams, and productivity-focused users use this skill to start from YAML automation recipes, customize parameters, and guide an agent through repeatable scheduled or event-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automation recipes can send emails, publish public posts, or copy data on schedules without enough scoping or review guidance. <br>
Mitigation: Add explicit review steps, narrow recipients and platforms, test recipes in simulation, and confirm what data or content will be sent, posted, or copied before enabling them. <br>
Risk: Scheduled workflows may continue running after initial setup and create unintended repeated actions. <br>
Mitigation: Start with manual or one-time test runs, keep execution logs enabled, and document how to disable each recipe before scheduling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/automation-recipe-book-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML recipe templates and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recipe definitions with trigger, actions, and optional failure-handling fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
