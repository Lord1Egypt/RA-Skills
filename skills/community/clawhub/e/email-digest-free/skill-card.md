## Description:

Automates browser-based webmail sessions to extract recent messages and produce daily email digest reports with counts, important items, action suggestions, and optional inbox screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, individual developers, and operations teams use this skill to summarize daily or weekly webmail activity from logged-in browser sessions across supported Web mail providers. It helps an agent generate digest reports, highlight important senders or subjects, and prepare local summary artifacts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may access already logged-in webmail sessions through the local browser.

Mitigation: Run it only against intended mail accounts and avoid using shared browser profiles or accounts outside the digest scope.

Risk: Generated reports and screenshots can contain senders, subjects, timestamps, snippets, and other mailbox metadata.

Mitigation: Use a dedicated output directory with restricted permissions and delete reports or screenshots when they are no longer needed.

Risk: Broad multi-account runs can collect more mailbox information than necessary.

Mitigation: Limit configured inboxes and extraction ranges to the accounts and dates required for the current digest.

Risk: Cron or launchd schedules can continue collecting mailbox summaries without active review.

Mitigation: Review scheduled jobs before enabling them and disable schedules when recurring digests are no longer required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-digest-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports with inline shell command examples and optional PNG screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Markdown reports, snippets, subjects, senders, timestamps, and inbox screenshots to user-selected output directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
