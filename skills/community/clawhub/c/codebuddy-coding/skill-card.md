## Description: <br>
CodeBuddy Coding lets an agent invoke the CodeBuddy CLI for code generation, refactoring, debugging, file operations, command execution, progress monitoring, and structured task results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13770626440](https://clawhub.ai/user/13770626440) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to delegate coding tasks to CodeBuddy CLI, track progress, and receive structured results about status, modified files, tool calls, reasoning, duration, and errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a CLI with broad coding authority and defaults to permission bypass. <br>
Mitigation: Use it only with a trusted CodeBuddy CLI in a version-controlled or disposable workspace, pass an explicit safe cwd, and avoid bypassPermissions unless deliberately needed. <br>
Risk: Task prompts may cause file changes or command execution in the selected workspace. <br>
Mitigation: Review task text before execution and do not pass untrusted instructions to the skill. <br>
Risk: Detached background execution can continue outside the immediate request flow. <br>
Mitigation: Monitor background processes or disable detached background execution when unattended changes are not acceptable. <br>


## Reference(s): <br>
- [CodeBuddy Coding on ClawHub](https://clawhub.ai/13770626440/codebuddy-coding) <br>
- [Publisher profile: 13770626440](https://clawhub.ai/user/13770626440) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance, JSON task results] <br>
**Output Format:** [JSON result objects and progress events, with optional text output from the underlying CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports status, filesModified, toolCalls, reasoning, duration, progress, and errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
