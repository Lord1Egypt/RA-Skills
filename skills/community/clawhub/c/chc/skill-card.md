## Description: <br>
Claw Help Claude helps an agent manage Claude Code CLI sessions through OpenClaw, including session startup, multi-instance management, multi-turn conversations, and fallback PTY control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linux2010](https://clawhub.ai/user/linux2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep Claude Code sessions organized across projects, continue multi-turn work, inspect session state, and recover or stop sessions when ACP or PTY control is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages Claude Code sessions that may access project files, credentials, or local configuration. <br>
Mitigation: Use narrow project directories, review Claude Code permissions before launching sessions, and avoid placing secrets in prompts. <br>
Risk: Cleanup and reset commands can remove session or configuration files. <br>
Mitigation: Back up or rename configuration and session files before running cleanup or reset commands. <br>


## Reference(s): <br>
- [Claude Code CLI documentation](https://docs.anthropic.com/claude-code) <br>
- [Agent Client Protocol](https://github.com/agentclientprotocol) <br>
- [Claude Code CLI configuration reference](artifact/references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ACP-first session guidance with PTY fallback notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
