## Description: <br>
Elcano Superpowers guides agents through a structured brainstorm, plan, execute, review, and ship workflow for larger coding changes using sub-agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elcanoclaw](https://clawhub.ai/user/elcanoclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to manage larger feature work, refactors, and multi-file changes with approved designs, TDD-oriented plans, sub-agent execution, review, and shipping steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow includes shipping actions such as git push and PM2 restarts without a clear final approval step. <br>
Mitigation: Require explicit approval before commits, pushes, PM2 restarts, notifications, screenshots, or git checkout. <br>
Risk: Sub-agent workflows can expose more project context than needed, including sensitive code or shared branch state. <br>
Mitigation: Limit sub-agent context to the files needed for the task and review the skill before use in projects with shared branches, production PM2 processes, or sensitive code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elcanoclaw/elcano-superpowers) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown instructions with inline command examples and task templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workflow gates, plan templates, review checklists, and shipping actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
