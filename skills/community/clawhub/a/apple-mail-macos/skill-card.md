## Description: <br>
Use local CLI to manage Gmail, Outlook, iCloud, Yahoo, Fastmail, and other mail accounts synced in Apple Mail on macOS, without APIs or OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, triage, draft, send, move, archive, and delete messages in accounts already connected to Apple Mail on macOS. It is intended for local Mail.app automation with dry-run previews and confirmation gates for write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate real Apple Mail accounts on the local Mac, including write actions such as sending, deleting, forwarding, reply-all, and bulk mailbox changes. <br>
Mitigation: Keep dry-run previews and explicit confirmation gates enabled for all high-risk write actions, with second confirmation for recipient changes, reply-all expansion, forwarding, and bulk operations. <br>
Risk: Retained local mailbox context and operation logs in ~/apple-mail-macos/ may become broader than intended over time. <br>
Mitigation: Review local memory, safety, and operation logs periodically and keep stored context limited to the accounts, mailbox scopes, and preferences needed for current workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/apple-mail-macos) <br>
- [Skill Homepage](https://clawic.com/skills/apple-mail-macos) <br>
- [Setup Guide](setup.md) <br>
- [Command Paths](command-paths.md) <br>
- [Provider Coverage](provider-coverage.md) <br>
- [Safety Checklist](safety-checklist.md) <br>
- [Operation Patterns](operation-patterns.md) <br>
- [Troubleshooting](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include dry-run previews, operation IDs, local configuration notes, and read-back verification summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
