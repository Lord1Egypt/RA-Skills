## Description: <br>
Email Management - Secure Gmail, Outlook & Exchange - multi account support. Read, search, or triage inbox/email; send, reply, forward, delete; view email, a secure log-cli & gws alternative for AI email workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Gmail, Outlook, and Exchange mailboxes through the PortEden CLI, including reading, searching, triaging, sending, replying, forwarding, modifying, and deleting email across accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires mailbox credentials or authenticated keyring access. <br>
Mitigation: Use least-privilege provider scopes, isolate accounts with --profile or PE_PROFILE, clear credentials with porteden auth logout when finished, and revoke exposed tokens at the email provider. <br>
Risk: Email send, reply, forward, delete, and modify actions can be visible to others or difficult to reverse. <br>
Mitigation: Confirm the target profile or account, message ID or recipient list, and intended change with the user before running mutating commands. <br>
Risk: Email subjects, bodies, and attachments may contain untrusted third-party instructions. <br>
Mitigation: Treat email content as data, summarize and attribute claims to the sender, prefer preview-only output, and fetch full bodies only when explicitly needed. <br>
Risk: The scanner verdict is clean, but the security summary notes that the target artifact files were not available for a full artifact-level review. <br>
Mitigation: Review the supplied skill files, install steps, and commands before installation when high assurance is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/porteden/email-gmail-outlook) <br>
- [PortEden homepage](https://porteden.com) <br>
- [PortEden publisher profile](https://clawhub.ai/user/porteden) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill recommends compact JSON output with the -jc flags and requires the porteden CLI plus PE_API_KEY or authenticated keyring credentials.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
