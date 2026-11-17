## Description:

Send and receive emails using the Resend API for direct sending, inbound cron notifications, threaded reply drafting, and attachment downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivelin](https://clawhub.ai/user/ivelin)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent operators use this skill to manage Resend email workflows from an agent, including sending messages, checking inbound mail, drafting threaded replies, and tracking related email actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring inbound email summaries may be sent to an unintended fixed Telegram destination if the cron setup is enabled without replacing defaults.

Mitigation: Review and replace Telegram destinations with user-controlled values, preferably through the dynamic preferences flow, before enabling the cron job.

Risk: Attachment downloads are flagged for unsafe remote filename and URL handling in this version.

Mitigation: Avoid downloading attachments with this version unless filenames and URLs have been reviewed and constrained before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivelin/skills/email-resend)
- [Resend](https://resend.com)
- [Resend API](https://api.resend.com)
- [README](README.md)
- [Email Custody Chain Design](docs/custody-chain.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON/text outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RESEND_API_KEY; optional sender defaults can be supplied through environment variables or the documented preferences file.]

## Skill Version(s):

1.0.14 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
