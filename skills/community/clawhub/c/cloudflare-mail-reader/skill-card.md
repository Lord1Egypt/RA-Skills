## Description:

Reads one mailbox's messages or a paginated mail list from a Cloudflare temporary mail admin API and returns normalized JSON or CSV results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcwang502](https://clawhub.ai/user/jcwang502)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to fetch, normalize, and export mailbox messages from a configured Cloudflare temporary mail backend without opening the web UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Admin mail credentials can be sent to a user-selected API URL.

Mitigation: Use only a trusted mail backend, avoid overriding the API URL to untrusted hosts, and use narrowly scoped rotatable credentials.

Risk: Outputs may contain private email content, verification codes, or account-recovery data.

Mitigation: Treat JSON, CSV, transcripts, and exported files as sensitive, and avoid including raw payloads unless needed for debugging.

Risk: Mailbox access depends on the trustworthiness of operators who can invoke the skill.

Mitigation: Limit invocation to authorized users and mailboxes, and review access patterns before deployment.

## Reference(s):

- [API Reference](references/api.md)
- [Example Prompts](references/examples.md)
- [Cloudflare Mail Reader on ClawHub](https://clawhub.ai/jcwang502/skills/cloudflare-mail-reader)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON or CSV, with Markdown summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verification_code when extractable; raw payloads are included only when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
