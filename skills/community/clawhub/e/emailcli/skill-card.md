## Description: <br>
Interact with an email inbox using mail-cli commands to read, search, send, reply, mark, move, delete, manage folders, manage drafts, and manage accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirai3103](https://clawhub.ai/user/mirai3103) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help a user operate their email account from the command line. It is suited for inbox review, message search, sending and replying to email, draft handling, attachment downloads, folder organization, and account management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email or change mailbox state, including deleting or moving messages, deleting drafts, removing accounts, and running batch operations. <br>
Mitigation: Require explicit user confirmation before high-impact actions and review recipients, message content, account, folder, and message IDs before execution. <br>
Risk: Attachment downloads can write email attachments to local storage. <br>
Mitigation: Confirm the intended attachments and destination directory before downloading. <br>
Risk: Batch operations may partially fail while still returning an overall success response. <br>
Mitigation: Inspect any failed array in the JSON response and report partial failures clearly before taking follow-up action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirai3103/emailcli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces mail-cli commands, parses JSON responses, and summarizes success, errors, or partial failures.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
