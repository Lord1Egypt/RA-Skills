## Description: <br>
Email MCP Helper gives an agent a reference for using a self-hosted email MCP server to read, search, send, reply, forward, schedule, organize, and inspect email across configured IMAP/SMTP accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as a tool reference for agents that connect to a self-hosted email MCP server to read, search, send, organize, and inspect email across configured accounts. It is intended for environments where the user controls the email MCP server, proxy, API key, and configured mail credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad multi-account email access, including reading, sending, forwarding, scheduling, deleting, moving, labeling, attachment download, and bulk operations. <br>
Mitigation: Install only when you control and trust the MCP server and proxy, restrict configured accounts to the minimum needed, and protect the API key and email credentials. <br>
Risk: The artifact is primarily a tool reference and does not define enough built-in consent boundaries for high-impact email actions. <br>
Mitigation: Add separate agent rules requiring explicit user approval before sending, replying, forwarding, scheduling, deleting, moving, labeling, downloading attachments, or running bulk email operations. <br>
Risk: Incorrect account names, mailbox paths, or email IDs can cause actions to target the wrong mailbox or message. <br>
Mitigation: Require the agent to call list_accounts and list_mailboxes before acting, use email IDs returned by list_emails or search_emails, and avoid guessing folder paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/encryptshawn/email-mcp-helper) <br>
- [email-mcp source repository](https://github.com/codefuturist/email-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown tool reference with MCP call sequences and parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes MCP email tools and safe call patterns; it does not itself bundle or operate the email server.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence, created 2026-05-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
