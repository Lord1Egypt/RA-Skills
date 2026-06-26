## Description: <br>
Bridges OpenClaw messaging channels to a persistent Claude Code CLI session in tmux so users can start, stop, monitor, and interact with Claude Code from chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZLHad](https://clawhub.ai/user/ZLHad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate a local Claude Code CLI session from OpenClaw-connected chat channels, including selecting a working directory, using sandbox mode, forwarding slash commands, and responding to approval prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat conversations can remotely control a persistent local Claude Code terminal session. <br>
Mitigation: Install only for trusted chat channels and participants, prefer private chats, and stop sessions when work is finished. <br>
Risk: Claude Code may request permission to read or write files or execute commands in the chosen working directory. <br>
Mitigation: Review every approval prompt carefully, avoid persistent project-wide approvals unless needed, and use sandbox mode or low-sensitivity directories when possible. <br>
Risk: History and terminal peek commands can expose sensitive terminal output. <br>
Mitigation: Treat /cc history and /cc peek as sensitive operations and restrict access to chats where their output is appropriate. <br>


## Reference(s): <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [OpenClaw project](https://github.com/nicepkg/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/ZLHad/claude-code-bridge) <br>
- [Claude Code Bridge usage guide](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and terminal output excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May truncate long Claude Code output and direct users to history or peek commands for more context.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
