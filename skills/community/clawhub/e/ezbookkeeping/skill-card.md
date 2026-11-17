## Description:

Helps agents use ezBookkeeping API tools to record and query transactions, inspect accounts, categories, tags, and exchange rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayswind](https://clawhub.ai/user/mayswind)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents managing a self-hosted ezBookkeeping instance can use this skill to look up financial records and exchange rates or add transactions, accounts, categories, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create financial records and configuration objects, not just retrieve information.

Mitigation: Review the command list and proposed changes before execution; use an ezBookkeeping token with the least necessary privileges.

Risk: The skill can list session metadata and expose sensitive financial data in responses.

Mitigation: Limit access to results and avoid sharing account, transaction, or session details unnecessarily.

Risk: An API token stored in a broad home-directory .env file or sent over insecure transport could be exposed.

Mitigation: Keep credentials in a restricted location and use HTTPS except for local-only testing.

## Reference(s):

- [ezBookkeeping API Tools release](https://clawhub.ai/mayswind/skills/ezbookkeeping)
- [ezBookkeeping OpenClaw integration](https://ezbookkeeping.mayswind.net/agent/openclaw)
- [ezBookkeeping](https://ezbookkeeping.mayswind.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or text with shell commands and structured API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can contain financial records and session metadata.]

## Skill Version(s):

2.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
