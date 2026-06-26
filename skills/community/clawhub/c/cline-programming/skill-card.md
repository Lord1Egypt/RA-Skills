## Description: <br>
Calls the Cline AI programming tool and provides a plan-check-act workflow for generating a coding plan, reviewing it, and executing implementation tasks with verbose progress output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[touchdeeper](https://clawhub.ai/user/touchdeeper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to structure Cline-assisted coding work into planning, plan review, and action steps. It provides command patterns for Cline configuration, credential setup, planning, and execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes Cline auto-approval through --yolo, allowing coding actions and generated code execution without manual confirmation. <br>
Mitigation: Use it in a disposable or version-controlled workspace, remove auto-approval flags for sensitive tasks, and review generated plans before allowing changes. <br>
Risk: Cline tasks may depend on API credentials, network access, and local workspace permissions. <br>
Mitigation: Limit credentials and workspace permissions to the minimum needed for the task, and avoid running the skill where secrets or production assets are exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/touchdeeper/cline-programming) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Cline CLI commands that can execute generated code when run by an agent.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
