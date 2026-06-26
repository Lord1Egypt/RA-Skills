## Description: <br>
Send automatic notifications when the OpenClaw gateway starts up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keaneyan](https://clawhub.ai/user/keaneyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw gateway operators use this skill to configure startup notifications to a chosen messaging channel so gateway restarts are visible without manually checking service status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway startup details may be sent to an unintended or overly broad chat target. <br>
Mitigation: Use a private or least-privilege recipient and review the generated config.json before restarting the gateway. <br>
Risk: The installed startup hook continues sending notifications until it is disabled or removed. <br>
Mitigation: Disable or remove the gateway-notify hook when automatic notifications are no longer needed. <br>


## Reference(s): <br>
- [Channel Reference](references/CHANNELS.md) <br>
- [ClawHub Release Page](https://clawhub.ai/keaneyan/gateway-startup-notify) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown instructions with bash commands and generated OpenClaw hook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The setup flow writes HOOK.md, config.json, and handler.ts under ~/.openclaw/hooks/gateway-notify.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
