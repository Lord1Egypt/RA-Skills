## Description: <br>
Agent Advisor recommends Claude models from a task description or recent OpenClaw conversation history and reports an OpenClaw gateway security score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrKangZuBin](https://clawhub.ai/user/MrKangZuBin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Agent Advisor to choose an appropriate Claude model for a described or recent task and to understand basic OpenClaw gateway security posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto and full-without-task modes read recent local OpenClaw conversation history, which may include secrets, credentials, proprietary topics, or personal information. <br>
Mitigation: Use recommend with an explicit task description when prior sessions may contain sensitive information. <br>


## Reference(s): <br>
- [Agent Advisor on ClawHub](https://clawhub.ai/MrKangZuBin/agent-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Plain text console reports with model recommendations, security scores, and suggested configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw configuration and, in auto and full-without-task modes, recent local OpenClaw conversation history.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
