## Description: <br>
BanditDB is an in-memory decision database for AI agents that learns from outcomes to tune notification timing, model routing, and prompt selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simeonlukov](https://clawhub.ai/user/simeonlukov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use BanditDB to add outcome-based decision learning to agents for choices such as notification timing, tool routing, model selection, and response style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External BanditDB binaries, Docker images, or SDKs may change outside the skill artifact. <br>
Mitigation: Verify the external release source and pin versions before installation. <br>
Risk: Context vectors and reward data can encode sensitive user or workflow behavior. <br>
Mitigation: Use minimal non-sensitive features, obtain user consent when appropriate, and define retention and deletion practices. <br>
Risk: Learned rewards can steer agents toward unsuitable behavior if used for manipulation or high-risk decisions. <br>
Mitigation: Keep BanditDB out of high-risk decision workflows and review reward definitions for user-aligned outcomes. <br>


## Reference(s): <br>
- [BanditDB API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with API endpoint examples and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local service setup guidance, MCP tool registration notes, and reward-loop API usage.] <br>

## Skill Version(s): <br>
0.1.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
