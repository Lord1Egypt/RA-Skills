## Description: <br>
Automatically detect and renew expired Claude Code OAuth tokens via heartbeat with refresh-token renewal, Chrome browser automation, and user alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenhab03](https://clawhub.ai/user/chenhab03) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators running OpenClaw agents with Claude Code use this skill to check token health during heartbeat cycles and attempt renewal before an expired OAuth token interrupts agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically use local Claude credentials and a logged-in Chrome session to renew account access. <br>
Mitigation: Install only when unattended Claude Code OAuth renewal is intended, review the script first, and consider adding a manual approval gate. <br>
Risk: Browser automation can authorize Claude access through the user's active Chrome session. <br>
Mitigation: Disable the Tier 2 browser automation path or run it only in a controlled macOS environment where this behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenhab03/claude-oauth-renewal) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Claude Code repository](https://github.com/anthropics/claude-code) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and heartbeat configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit alert text when token renewal fails; normal healthy checks are silent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
