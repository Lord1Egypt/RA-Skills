## Description: <br>
CLI to manage enterprise Outlook emails via Exchange Web Services (EWS). Use ews-mail.py to list, read, reply, forward, search, send, move, delete emails and download attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyun94](https://clawhub.ai/user/guyun94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate an enterprise Exchange mailbox from the command line, including listing, reading, searching, sending, replying, forwarding, moving, deleting, flagging, and downloading attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, send, modify, delete, and download enterprise email. <br>
Mitigation: Require manual confirmation before sending, replying, forwarding, moving, deleting, flagging, or downloading attachments. <br>
Risk: Downloaded attachments from untrusted messages may be unsafe or may use unsafe filenames. <br>
Mitigation: Avoid downloading attachments from untrusted mail and sanitize filenames before opening or retaining downloaded files. <br>
Risk: Headless Linux setup may rely on a persistent keyring master password environment variable. <br>
Mitigation: Avoid storing KEYRING_CRYPTFILE_PASSWORD in persistent environment or configuration files where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guyun94/ews-email) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Email bodies are truncated at 8000 characters by the script.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
