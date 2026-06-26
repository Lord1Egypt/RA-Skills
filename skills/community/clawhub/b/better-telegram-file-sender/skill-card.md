## Description: <br>
Send local files such as archives, PDFs, images, and videos to the current Telegram chat through OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzunglaviet](https://clawhub.ai/user/dzunglaviet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to send a selected local file back to the active Telegram conversation. It checks that the file exists, uses the session chat target, and calls OpenClaw to send the file with an optional caption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can send a local file to the active Telegram chat, which may expose sensitive content if the wrong path is selected. <br>
Mitigation: Before each send, verify the exact file path and avoid sending sensitive files unless the user clearly intends it. <br>
Risk: The transfer depends on a trusted OpenClaw CLI and configured Telegram bot. <br>
Mitigation: Use the skill only in environments where the OpenClaw gateway, CLI, and Telegram bot configuration are trusted. <br>


## Reference(s): <br>
- [ClawHub Package Page](https://clawhub.ai/dzunglaviet/better-telegram-file-sender) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces file existence checks, OpenClaw send commands, and send-status confirmation text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
