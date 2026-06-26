## Description: <br>
Claude Code Bridge lets OpenClaw route chat messages from QQ, Telegram, WeChat, and similar channels into a persistent Claude Code CLI session and return terminal output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZLHad](https://clawhub.ai/user/ZLHad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate a logged-in Claude Code CLI session from OpenClaw-connected chat channels, including starting, stopping, monitoring, sending prompts, and responding to tool approval prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat users can gain broad remote control over a persistent Claude Code terminal session on the host machine. <br>
Mitigation: Install only for trusted users and channels; prefer private chats, sender or channel allowlists, a low-privilege OS account, and non-sensitive repositories. <br>
Risk: Tool approvals, especially permanent approvals, can authorize file or command actions with lasting impact. <br>
Mitigation: Review every approval carefully and restrict or disable permanent approval workflows before using the skill in group chats. <br>
Risk: Peek, history, and generic key workflows can expose terminal state or let remote users steer the live session. <br>
Mitigation: Limit these workflows to trusted operators and disable or restrict them where multiple chat participants can reach the bot. <br>


## Reference(s): <br>
- [OpenClaw](https://github.com/nicepkg/openclaw) <br>
- [Claude Code CLI documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [CC-Bridge usage guide](references/usage.md) <br>
- [ClawHub release page](https://clawhub.ai/ZLHad/cc-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text relayed from a Claude Code terminal session, including code blocks and command output when Claude Code produces them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only chat bridge output; long terminal responses may be summarized or retrieved through history commands.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
