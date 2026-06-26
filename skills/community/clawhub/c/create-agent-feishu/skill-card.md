## Description: <br>
Creates a new OpenClaw agent by guiding workspace directory setup, memory files, openclaw.json configuration, Feishu channel setup, and channel binding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyachao](https://clawhub.ai/user/caoyachao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create and configure new OpenClaw agents, including workspace files, memory structure, Feishu bot credentials, channel policies, and bindings for routing messages to the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wildcard subagent permissions may allow the new agent to spawn or discover more agents than intended. <br>
Mitigation: Prefer an explicit allowAgents whitelist for production or sensitive deployments. <br>
Risk: Incorrect openclaw.json edits or gateway restarts may disrupt message routing. <br>
Mitigation: Back up and validate openclaw.json before restarting the OpenClaw gateway. <br>
Risk: Feishu app secrets may be exposed through logs, source control, or copied configuration snippets. <br>
Mitigation: Store Feishu credentials in protected configuration, keep them out of logs and repositories, and rotate exposed secrets. <br>
Risk: Memory, diary, and user profile files may accumulate unnecessary sensitive personal data. <br>
Mitigation: Minimize stored personal data and review workspace memory files before sharing, syncing, or publishing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/caoyachao/create-agent-feishu) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to OpenClaw workspace files and openclaw.json; review generated configuration and commands before execution.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
