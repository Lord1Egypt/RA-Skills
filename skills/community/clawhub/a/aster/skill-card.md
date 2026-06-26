## Description: <br>
Aster lets an AI agent control an Android device through MCP tools for calls, SMS, text-to-speech, UI automation, files, media search, notifications, and other mobile actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satyajiit](https://clawhub.ai/user/satyajiit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and advanced users use Aster to connect an AI agent to an Android phone so the agent can inspect device state, interact with apps, communicate through calls or SMS, manage local files, and react to phone events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an AI agent broad Android device control, including calls, SMS, UI automation, file operations, clipboard access, location access, and restricted shell execution. <br>
Mitigation: Install it only when this level of control is intended, prefer a spare phone, grant only needed Android permissions, and require explicit confirmation before sensitive actions. <br>
Risk: Event callbacks can forward incoming SMS, notifications, device status, and pairing events to an agent, which may cause actions based on message or notification content. <br>
Mitigation: Keep callbacks disabled unless needed, use only trusted authenticated callback endpoints, and require confirmation for actions triggered by incoming messages or notifications. <br>
Risk: Device approval and pairing workflows can expose a connected phone if unexpected devices are approved or if approval is automated without review. <br>
Mitigation: Approve only expected devices through the dashboard or CLI, reject unknown pairing requests, and review connected device status before allowing control. <br>


## Reference(s): <br>
- [ClawHub Aster listing](https://clawhub.ai/satyajiit/aster) <br>
- [Aster website](https://aster.theappstack.in) <br>
- [Aster GitHub repository](https://github.com/satyajiit/aster-mcp) <br>
- [Aster releases](https://github.com/satyajiit/aster-mcp/releases) <br>
- [Tailscale](https://tailscale.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Text] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, MCP tool names, and structured event payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can trigger device-control actions and receive event-forwarded text payloads when configured.] <br>

## Skill Version(s): <br>
0.1.14 (source: server release metadata; artifact frontmatter lists 0.1.13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
