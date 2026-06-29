## Description: <br>
Use the AgentTeam Email CLI command `at-email` to operate an agent mailbox for status checks, inbox listing, safe message reads, search, message state changes, sending, replies, automation-friendly JSON output, version checks, and CLI installation or launch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentteamhq](https://clawhub.ai/user/agentteamhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to operate an AgentTeam mailbox through the `at-email` CLI, including reading, searching, sending, replying, archiving, and producing JSON for downstream automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent read, change, send, or reply to mailbox messages. <br>
Mitigation: Review mailbox actions before execution, especially recipients, message bodies, replies, archive operations, and mark-read operations. <br>
Risk: Mailbox and message-read tokens grant access to email systems and may expose sensitive content if printed or mishandled. <br>
Mitigation: Treat mailbox tokens like passwords, avoid printing secret values, and rely on the CLI's missing-variable messages rather than inventing or echoing credentials. <br>
Risk: Running or installing the CLI from npm or release assets can introduce supply-chain risk. <br>
Mitigation: Prefer pinned or verified CLI versions, ask before modifying global tools, and verify standalone binary checksums before placing binaries on PATH. <br>


## Reference(s): <br>
- [At Email CLI project homepage](https://github.com/agentteamhq/agentteam-email/tree/main/apps/at-email-cli) <br>
- [ClawHub skill page](https://clawhub.ai/agentteamhq/at-email-cli) <br>
- [AgentTeam publisher profile](https://clawhub.ai/user/agentteamhq) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON-oriented CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce mailbox operation commands and guidance for text or JSON CLI output modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
