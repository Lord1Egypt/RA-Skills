## Description: <br>
Comprehensive Python tool for managing 163.com email with IMAP and SMTP support for sending, reading, searching, folders, message flags, batch actions, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newolf20000](https://clawhub.ai/user/newolf20000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents that operate a 163.com mailbox use this skill to send, read, search, organize, mark, move, delete, and download attachments from messages through a command-line Python tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs credentials and can read, send, and modify a 163.com mailbox. <br>
Mitigation: Use a 163 client authorization code instead of a login password and keep the configuration file private. <br>
Risk: Send, delete, move, and bulk mailbox actions can cause unintended message disclosure or loss. <br>
Mitigation: Require explicit confirmation before sends, deletes, moves, and bulk operations. <br>
Risk: Attachment downloads can write untrusted filenames to disk. <br>
Mitigation: Avoid downloading attachments from untrusted messages until filenames are sanitized and the destination is reviewed. <br>
Risk: Changing mail server settings could redirect mailbox credentials or content. <br>
Mitigation: Verify that IMAP and SMTP settings remain on official 163 hosts before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/newolf20000/email-163-com) <br>
- [Publisher Profile](https://clawhub.ai/user/newolf20000) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Command-line text output, JSON configuration, and downloaded mailbox attachment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a 163.com mailbox and client authorization code; operations may read, send, modify, delete, or download mailbox content.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
