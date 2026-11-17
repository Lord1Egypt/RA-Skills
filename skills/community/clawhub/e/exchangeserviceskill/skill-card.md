## Description:

Cross-platform skill for Exchange Server 2016 CU21 EWS operations on the OpenClaw Node.js runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jokermec](https://clawhub.ai/user/jokermec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and IT operators use this skill to let an agent inspect and manage on-premises Exchange mail, folders, calendar events, and meetings through EWS while requiring explicit confirmation for writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Exchange account may allow the skill to read, send, modify, and delete mailbox, folder, and calendar data.

Mitigation: Use a dedicated least-privilege account and review each planned action before allowing the agent to run Exchange commands.

Risk: Write operations can change or remove mailbox, folder, or calendar data.

Mitigation: Use the documented --dry-run mode for previews and require --confirm true or EXCHANGE_WRITE_CONFIRM=true only after reviewing the operation.

Risk: Passwords and master keys can be exposed if placed directly on command lines or in logs.

Mitigation: Use encrypted config storage or protected environment variables for EXCHANGE_PASSWORD and EXCHANGE_SKILL_MASTER_KEY, and keep secrets out of prompts, shell history, and logs.

Risk: The --insecure and EXCHANGE_INSECURE options weaken TLS certificate validation for Exchange requests.

Mitigation: Require an https:// Exchange URL and avoid insecure transport options except for reviewed temporary troubleshooting.

Risk: The NTLM dependency chain needs review before production deployment.

Mitigation: Review or update the httpntlm dependency chain and run organization-approved dependency scanning before production use.

## Reference(s):

- [Microsoft Exchange EWS operations](https://learn.microsoft.com/en-us/exchange/client-developer/web-service-reference/ews-operations-in-exchange)
- [ClawHub ExchangeService skill page](https://clawhub.ai/jokermec/skills/exchangeserviceskill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with npm shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on Exchange connection settings, credentials, and the configured account's mailbox permissions.]

## Skill Version(s):

1.0.1 (source: server release evidence, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
