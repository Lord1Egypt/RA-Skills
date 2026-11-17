## Description:

Sends one or more local files to Feishu chats through bot-triggered requests or command-line invocation, with local configuration support and no external Node.js dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxusong637](https://clawhub.ai/user/zhangxusong637)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to locate files by path or keyword and send selected files into Feishu chats or to Feishu users from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files with broad chat triggers and limited path restriction.

Mitigation: Use it only where chat participants are trusted, Feishu recipients are verified, and the process can access only files that are safe to send; restrict sends to an approved directory.

Risk: Command-line sends can target the wrong recipient when an explicit recipient is omitted or misconfigured.

Mitigation: Require confirmation that shows the file path, size, and recipient before sending, and prefer bot-triggered use where the chat context is explicit.

Risk: Broad contains-style triggers can cause unintended file-send workflows.

Mitigation: Narrow or remove broad contains triggers and require clear send intent before searching or uploading files.

Risk: World-writable log permissions can expose or tamper with local execution logs.

Mitigation: Use owner-only log permissions instead of 777 permissions.

## Reference(s):

- [Feishu Send Files ClawHub page](https://clawhub.ai/zhangxusong637/skills/feishu-send-files)
- [ClawHub installation page](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text status messages with command-line examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload selected local files to Feishu and write local execution logs.]

## Skill Version(s):

1.0.1 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
