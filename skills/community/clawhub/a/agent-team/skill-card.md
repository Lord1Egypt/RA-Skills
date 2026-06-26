## Description: <br>
Agent Team manages a configurable team of specialized child agents for listing, inspecting, spawning task sessions, and interactive chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and advanced agent users use Agent Team to manage local persona profiles, inspect configured agents, and launch specialized child-agent sessions for tasks or chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated child-agent sessions may continue running after launch. <br>
Mitigation: Monitor spawned sessions and stop them when the delegated task no longer needs to run. <br>
Risk: Local SOUL.md and config.json persona files may be sent to model providers during child-agent use. <br>
Mitigation: Use only trusted agent profiles and review persona files before spawning or chatting with an agent. <br>
Risk: The helper script includes confusing API credential handling. <br>
Mitigation: Keep real API keys in environment variables and do not place real keys directly in greetings.py. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangzhiyu/agent-team) <br>
- [Publisher profile](https://clawhub.ai/user/jiangzhiyu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text and child-agent responses, often Markdown or code depending on the delegated task.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn ongoing child-agent sessions and use local SOUL.md/config.json persona files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
