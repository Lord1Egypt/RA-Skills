## Description: <br>
Provides agent guidance for recovering from tool, command, dependency, permission, looping, backend fallback, degraded-service, and long-conversation truncation failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelfeng](https://clawhub.ai/user/michaelfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to help an AI assistant recover from failed tool calls, repeated mistakes, missing commands or dependencies, permission issues, model fallback events, degraded services, and truncated long conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may tell an agent to install missing dependencies automatically before retrying work. <br>
Mitigation: Require the agent to ask before adding dependencies, prefer isolated environments such as a project virtual environment or container, and review package names and versions before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michaelfeng/clawbrain-pro-retry) <br>
- [ClawBrain dashboard](https://clawbrain.dev/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Shell commands] <br>
**Output Format:** [Markdown guidance with inline command examples and status explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose alternate commands, dependency-install steps, fallback explanations, and user-facing recovery status.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
