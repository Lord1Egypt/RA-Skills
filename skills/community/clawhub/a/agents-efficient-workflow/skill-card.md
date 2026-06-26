## Description: <br>
Coordinate multiple agents with direct agent-to-agent handoffs and durable local Markdown notes to reduce token waste and handoff loss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wewehg](https://clawhub.ai/user/wewehg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to split work across specific agents, preserve handoff state in local Markdown files, and let the next agent resume from a concise source of truth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local handoff notes can contain secrets or unnecessary private data if users include sensitive context. <br>
Mitigation: Write only the information needed for the next agent, avoid secrets, and delete old handoff files when they are no longer needed. <br>


## Reference(s): <br>
- [Handoff Template](references/handoff-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/wewehg/agents-efficient-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown guidance and handoff file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local handoff notes under ~/.openclaw/shared-handoffs/ when agents follow the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
