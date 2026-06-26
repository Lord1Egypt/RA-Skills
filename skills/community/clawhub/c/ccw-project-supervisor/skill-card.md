## Description: <br>
Supervises OpenClaude and Claude Code Workflow project execution by selecting the correct planning, issue, queueing, or execution-review step and checking scope, dependencies, and backlog quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Majmunu](https://clawhub.ai/user/Majmunu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to supervise CCW project delivery, choose the right workflow command, and review plans or queues for dependency order, scope control, and execution readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend CCW prompts or /issue/execute steps that may not match the user's actual repository state or intended scope. <br>
Mitigation: Review generated prompts and execution recommendations before running them, and confirm they align with the current project scope, repository state, and validated issue queue. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Majmunu/ccw-project-supervisor) <br>
- [Engineering Order Reference](references/engineering-order.md) <br>
- [Phase Checklists](references/phase-checklists.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Text] <br>
**Output Format:** [Markdown with copy-ready command and prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include validation notes, exit criteria, and next-step recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
