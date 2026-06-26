## Description: <br>
Reasoning hygiene protocol for OpenClaw agents - keep context sharp by collapsing exploration into decisions, enforcing file budgets, and pruning ghost context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppiankov](https://clawhub.ai/user/ppiankov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep OpenClaw workspace context concise, prune stale memory, and establish persistent context hygiene rules for agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the pruning guidance too broadly could remove user-authored, audit-relevant, or still-useful context. <br>
Mitigation: Review proposed deletions and preserve anything user-authored, audit-relevant, or not clearly temporary. <br>
Risk: The timezone setup example may be copied without matching the user's actual location. <br>
Mitigation: Replace the example timezone with the user's real timezone before relying on date-sensitive reminders or reports. <br>
Risk: Adding the startup instruction to AGENTS.md makes this protocol persistent across future sessions. <br>
Mitigation: Add the AGENTS.md startup instruction only when ongoing context hygiene behavior is desired. <br>


## Reference(s): <br>
- [Context Hygiene on ClawHub](https://clawhub.ai/ppiankov/context-hygiene) <br>
- [Agent-Native CLI Convention](https://ancc.dev) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with short code blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide edits to workspace context files such as MEMORY.md, CONTEXT.md, USER.md, and AGENTS.md.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
