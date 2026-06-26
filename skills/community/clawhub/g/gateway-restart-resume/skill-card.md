## Description: <br>
Guides OpenClaw agents through gateway restarts by requiring a durable callback, captured reply route, recovery checks, and a post-restart status reply. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udaymanish6](https://clawhub.ai/user/udaymanish6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an OpenClaw gateway-backed agent must restart, stop, reload, update, or repair a gateway without losing the user follow-up. It helps the agent capture minimal routing metadata, create a durable resume callback, verify recovery, and report status in the original conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A gateway restart can terminate the current agent turn before the user receives confirmation. <br>
Mitigation: Create a durable callback outside the current gateway turn before restarting, and refuse to restart if that callback cannot be created. <br>
Risk: Resume payloads could expose secrets or private message content if copied too broadly. <br>
Mitigation: Store only the minimal routing metadata needed for the reply, and omit raw messages, tokens, environment values, transcripts, and full configuration. <br>
Risk: A failed restart could trigger unbounded recovery attempts. <br>
Mitigation: Limit verification to three total attempts over about five minutes, then record a durable failure state and stop. <br>
Risk: The skill requires trusted gateway operations permissions. <br>
Mitigation: Install only in an OpenClaw environment where the agent is authorized for cron or task callbacks, gateway or exec restart actions, and approved message delivery. <br>


## Reference(s): <br>
- [OpenClaw Cron Resume Pattern](references/openclaw-cron-resume.md) <br>
- [ClawHub release page](https://clawhub.ai/udaymanish6/gateway-restart-resume) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with text status templates, JSON payload examples, and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator-facing restart and recovery instructions; it does not restart OpenClaw by itself.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
