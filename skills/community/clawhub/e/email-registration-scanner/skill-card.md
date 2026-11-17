## Description:

Scans selected email accounts for registration, welcome, and confirmation messages to build a deduplicated chronological list of services the user has signed up for.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatihbtw](https://clawhub.ai/user/fatihbtw)

### License/Terms of Use:

MIT

## Use Case:

External users and privacy-focused individuals use this skill to audit selected mailboxes for registration-related messages, then review a deduplicated list of online services they may want to manage, deactivate, or delete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox scanning can expose credentials and sensitive account-history data.

Mitigation: Prefer OAuth or app-specific passwords, avoid regular mailbox passwords, keep credentials out of output and logs, and use a secret store where available.

Risk: Generated scan results can reveal a map of the user's online accounts.

Mitigation: Store results only in temporary files when needed and delete generated JSON results after use.

Risk: Plaintext IMAP can expose mailbox traffic if used against an untrusted or remote server.

Mitigation: Use SSL for remote IMAP providers and use plaintext IMAP only for a trusted local Proton Mail Bridge at 127.0.0.1.

Risk: Search-query and sender-pattern matching may produce false positives or incomplete registration history.

Mitigation: Review the final service list before taking account deletion or deactivation actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fatihbtw/skills/email-registration-scanner)
- [Email Provider Reference](references/providers.md)
- [Registration Search Queries](references/search-queries.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples, a date-sorted service list, and optional JSON scan result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-account temporary JSON results and a merged, date-sorted list of registered services.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
