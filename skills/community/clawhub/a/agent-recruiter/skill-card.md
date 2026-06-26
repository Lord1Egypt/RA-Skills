## Description: <br>
Agent Recruiter creates, configures, and manages OpenClaw agents, including workspace files, credential-profile copies, Feishu routing bindings, and gateway restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JunChen19](https://clawhub.ai/user/JunChen19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create or customize persistent OpenClaw agents, bind them to Feishu groups, and generate their workspace identity and behavior files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently create OpenClaw agents, edit live routing, and restart Gateway. <br>
Mitigation: Back up ~/.openclaw/openclaw.json, review the planned agent and binding entries, and restart Gateway only after confirming the change. <br>
Risk: The skill can copy credential-profile configuration into a new agent. <br>
Mitigation: Inspect auth-profiles.json before and after copying, and limit the new agent to only the profiles required for its role. <br>
Risk: Generated SOUL.md, identity, memory, and group-binding behavior can affect what the new agent sends and retains. <br>
Mitigation: Review generated behavior files, verify the Feishu group ID, and avoid enabling group posting or memory logging until retention and message scope are understood. <br>


## Reference(s): <br>
- [agency-agents](https://github.com/msitarzewski/agency-agents) <br>
- [Agent Recruiter ClawHub listing](https://clawhub.ai/JunChen19/agent-recruiter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent OpenClaw agent files, copy credential profiles, update routing configuration, and restart Gateway.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
