## Description: <br>
Claude Code relay via tmux for operating Claude Code remotely from Telegram or any OpenClaw channel by starting sessions, sending messages, and reading output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artwalker](https://clawhub.ai/user/artwalker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to control an existing Claude Code session from a remote channel, including starting, stopping, checking status, sending messages, and reading recent output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote chat messages can drive a persistent local Claude Code session. <br>
Mitigation: Install only when that control path is intended, use private channels, check active sessions with /cc status, and stop sessions with /cc off. <br>
Risk: Session output is stored locally while a relay session is active. <br>
Mitigation: Avoid sending secrets through the relay and stop sessions with /cc off so the tmux session and local log are cleaned up. <br>
Risk: A broad project root can expose unintended local projects to the relay. <br>
Mitigation: Choose project roots carefully and limit them to directories that are appropriate for remote-channel control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/artwalker/cc) <br>
- [Publisher profile](https://clawhub.ai/user/artwalker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell command output in code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Long outputs are summarized; ANSI escape codes are stripped by the script.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
