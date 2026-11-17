## Description:

Creates single or batch Cloudflare temporary mail addresses through the `/admin/new_address` admin API and returns structured status output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcwang502](https://clawhub.ai/user/jcwang502)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create one or more mailbox addresses in a Cloudflare temporary mail deployment through the admin API, including batch creation and CSV export when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Admin credentials and mailbox access tokens can be exposed through transcripts, logs, shared terminals, or exported JSON/CSV files.

Mitigation: Use environment variables or secure runtime secret handling, avoid sharing raw output, and redact JWTs, passwords, and admin credentials before storing or forwarding results.

Risk: Changing the admin API URL can send credentials and mailbox data to an unintended endpoint.

Mitigation: Set CLOUDFLARE_MAIL_API_URL only when the operator intentionally controls and trusts the replacement endpoint.

## Reference(s):

- [API Reference](references/api.md)
- [Example Prompts](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/jcwang502/skills/cloudflare-mail-address-creator)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON or CSV output, with Markdown summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include mailbox addresses, JWTs, passwords, status counts, and error messages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
