## Description: <br>
Use this skill when the user wants to clean up, back up, or optimize their 126.com (NetEase) email account, including local backup, spam or subscription bulk deletion, and large attachment stripping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinghaojia](https://clawhub.ai/user/yinghaojia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage NetEase 126.com mailboxes through an agent-guided workflow for backup, classification, cleanup, and storage reduction. It is intended for users who can provide 126.com IMAP authorization credentials and review proposed destructive mailbox changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a 126.com mailbox and can change or delete email during the cleanup and attachment-stripping workflows. <br>
Mitigation: Use a revocable IMAP authorization code, keep backups in a private location, review previews carefully, and revoke or rotate the authorization code after cleanup. <br>
Risk: Attachment stripping and bulk cleanup are destructive operations if the user confirms the proposed changes. <br>
Mitigation: Complete and verify local backups before destructive phases, use staging copies where available, and confirm deletion or stripping targets before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinghaojia/126mail-cleanup) <br>
- [Publisher profile](https://clawhub.ai/user/yinghaojia) <br>
- [126.com mail service](https://mail.126.com) <br>
- [Support issues](https://github.com/jimmyclaw/126mail-cleanup/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline commands and local JSON or email backup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and 126.com IMAP credentials supplied through MAIL126_ADDRESS and MAIL126_AUTH_CODE.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, clawhub.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
