## Description: <br>
Add self-sustaining autonomous loop capability to an OpenClaw agent. The agent keeps working after each reply until a stop file is placed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasye378](https://clawhub.ai/user/lucasye378) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to keep an OpenClaw agent working across repeated task cycles, especially for long-running agents, autonomous-mode conversion, or debugging a loop that stopped unexpectedly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended looping can keep an agent operating longer than intended. <br>
Mitigation: Install only when unattended operation is intentional, set runtime or iteration limits, monitor initial runs, and know how to place the stop file or disable the plugin before starting it. <br>
Risk: Autonomous sessions may execute project startup scripts or other workspace commands without further prompts. <br>
Mitigation: Review and trust project scripts such as init.sh before enabling the loop for that workspace. <br>
Risk: Enabling another reply-trigger loop for the same agent can send duplicate follow-up messages. <br>
Mitigation: Do not enable this skill and agent-reply-trigger for the same agentId. <br>


## Reference(s): <br>
- [Autonomous Loop ClawHub Release](https://clawhub.ai/lucasye378/autonomous-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configurable delay and per-agent follow-up messages; writes OpenClaw loop logs.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
