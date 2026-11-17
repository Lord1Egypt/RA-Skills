## Description:

Create and manage a persistent agent-only email inbox with full send and receive, semantic search, tagging, webhooks, attachments, delivery monitoring, and AI-powered structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanjairaj7](https://clawhub.ai/user/shanjairaj7)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create and operate a persistent email inbox for autonomous communication, inbox search, message triage, webhook-driven workflows, attachments, and structured extraction from inbound email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle real email and business data through authenticated inbox, message, attachment, webhook, and search operations.

Mitigation: Use narrowly scoped API keys stored in environment variables or a secrets manager, and avoid placing credentials.json in the skill root.

Risk: Outbound email, webhook forwarding, attachment upload, API-key changes, and deletion requests can have account or data impact.

Mitigation: Require explicit approval before these operations and review the target recipients, endpoints, files, key scopes, and deletion previews.

Risk: Installation depends on external packages and API clients.

Mitigation: Pin and verify dependencies before deployment.

Risk: The Ed25519 registration example can expose private-key material if used as written.

Mitigation: Do not print or log private keys; use secure key generation and secret storage before enabling autonomous registration.

## Reference(s):

- [Commune API Reference](references/api.md)
- [Commune Documentation](https://commune.email/docs)
- [Commune Website](https://commune.email)
- [ClawHub Skill Page](https://clawhub.ai/shanjairaj7/skills/commune)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, JSON request bodies, and CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Commune API key and may perform authenticated email, inbox, webhook, attachment, API-key, and deletion operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
