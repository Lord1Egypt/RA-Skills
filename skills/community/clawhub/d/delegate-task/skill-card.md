## Description: <br>
Delegate tasks to OpenSpace, a full-stack autonomous worker for coding, DevOps, web research, and desktop automation, backed by an MCP tool and skill library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tcbywing](https://clawhub.ai/user/tcbywing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to delegate tasks that require OpenSpace's tool access, skill search, orchestration, or skill repair and upload workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated tasks may send task details, code, infrastructure context, web context, or desktop context to an external OpenSpace service. <br>
Mitigation: Require explicit approval before delegation and avoid sharing sensitive repositories, credentials, or private operational details unless the user intentionally approves that exposure. <br>
Risk: Auto-imported, evolved, fixed, or uploaded skills can affect future agent behavior and may spread unsafe changes if reviewed poorly. <br>
Mitigation: Disable automatic cloud imports where possible, inspect evolved or fixed skills before use, and review any public upload decision before sharing it. <br>
Risk: The server security verdict flags broad cloud delegation, auto-import, and upload authority as suspicious because the artifact has limited approval and data-safety guardrails. <br>
Mitigation: Treat OpenSpace calls as privileged actions, keep user confirmation in the loop, and review generated or modified files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tcbywing/delegate-task) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with MCP tool call examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return delegated task results, skill search results, evolved skill metadata, or upload decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
