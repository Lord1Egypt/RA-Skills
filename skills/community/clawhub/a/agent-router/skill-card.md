## Description: <br>
Routes user commands to the most suitable sub-agent based on intent, coordinates task execution priority, and tracks overall task status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zs15600770520](https://clawhub.ai/user/zs15600770520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route user requests to the most suitable downstream agent or skill, coordinate priority when multiple skills trigger, and summarize subtask status into one response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing requests with sensitive information or consequential actions to untrusted downstream agents or skills can expose data or produce unsafe actions. <br>
Mitigation: Use trusted downstream agents or skills, and review routed tasks before consequential execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zs15600770520/agent-router) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Natural-language routing decisions and task status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only routing behavior; downstream outputs depend on the selected agents or skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
