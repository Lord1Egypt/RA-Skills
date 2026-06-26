## Description: <br>
Automatically records and backs up conversations with importance tagging to preserve emotional and technical context independently from OpenClaw internals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfanmy](https://clawhub.ai/user/zfanmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill when they intentionally want local transcript backup, importance tagging, and recovery helpers for conversations. It is suited to preserving technical decisions and personal context in local Markdown and JSONL files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically save full chats, including sensitive personal content and passwords, in plaintext local files. <br>
Mitigation: Install only when continuous local transcript logging is intended; set restrictive file permissions and periodically review or delete memory and .guardian files. <br>
Risk: Importance rules may encourage saving secrets or password-related messages. <br>
Mitigation: Remove password and secret keywords from importance rules and avoid recording credentials or private data. <br>
Risk: Users may source a local shell script that writes persistent files. <br>
Mitigation: Pin or verify the script before sourcing it, and review the configured memory paths before enabling automatic recording. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zfanmy/conversation-guard) <br>
- [Publisher profile](https://clawhub.ai/user/zfanmy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Markdown conversation logs, JSONL backups, emergency backup files, and status or recovery text when its shell functions are invoked.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
