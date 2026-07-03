## Description: <br>
agent-team-mesh helps OpenClaw agents on routable team containers or pods discover peers, check connectivity, send messages, wait for replies, and broadcast over direct WebSocket gateway calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and internal teams use this skill to let distributed OpenClaw agents on trusted networks ping teammates, send messages and collect replies, broadcast updates, and maintain registry and token configuration for peer communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages may be shared with another agent and retained in that agent's session history. <br>
Mitigation: Avoid placing secrets or sensitive content in messages and treat sends and broadcasts as shared team communication. <br>
Risk: The skill uses shared gateway tokens and plaintext WebSocket calls intended for trusted internal networks. <br>
Mitigation: Install only in trusted internal team environments, restrict tokens.json permissions, and keep gateway access on a trusted routable network. <br>
Risk: The optional IM fallback can forward content through another messaging channel when an agent is unreachable. <br>
Mitigation: Disable or remove the fallback unless explicitly needed and approved for the team's communication policy. <br>
Risk: Broadcast and send operations can reach unintended teammates if registry or identity detection is wrong. <br>
Mitigation: Use dry-run mode and explicit recipient checks before sending, and keep registry and local identity configuration current. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/songhonglei/agent-team-mesh) <br>
- [registry.json](references/registry.json) <br>
- [tokens.example.json](references/tokens.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON configuration examples, and command-line text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run previews, connectivity status, send and broadcast results, and teammate agent replies when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
