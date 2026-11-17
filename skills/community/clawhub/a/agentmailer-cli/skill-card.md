## Description:

Operate AgentMailer from a shell with the generated CLI for inboxes, messages, threads, drafts, attachments, domains, webhooks, policy, events, billing, and A2A resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run AgentMailer CLI commands for shell automation, inspection, operational checks, and account-resource management across email and A2A workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad account-sensitive AgentMailer operations, including sending, domain, webhook, policy, billing, and A2A resource actions.

Mitigation: Review before installation on privileged accounts, prefer scoped API keys, and require explicit confirmation for mutating commands.

Risk: Bulk reads, retries, insecure transport settings, or untrusted message content can increase operational exposure.

Mitigation: Use dry-run where available, cap paginated reads, avoid AGENTMAILER_INSECURE outside local debugging, and treat email and A2A content as untrusted.

## Reference(s):

- [CLI operating guide](references/commands.md)
- [AgentMailer CLI examples](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/cli)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce read-only inspection commands, dry-run guidance, structured JSON output recommendations, and cautious retry guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
