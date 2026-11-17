## Description:

Set up and query business data across 100+ sources (Stripe, HubSpot, Salesforce, etc.) via SQL. Agent-driven setup, cross-source joins, mutations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kappa90](https://clawhub.ai/user/kappa90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to initialize Dinobase, connect SaaS and business data sources, sync data, query it with SQL, and perform previewed write-back mutations when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents to pass SaaS API keys to CLI commands.

Mitigation: Use narrowly scoped, revocable API keys and avoid exposing live secrets directly in visible agent commands when possible.

Risk: The skill installs and relies on an unpinned external CLI package.

Mitigation: Review the package before installation and install from a trusted, controlled environment.

Risk: Write-back mutations can change connected business systems.

Mitigation: Confirm mutation previews carefully before running the final confirmation command.

## Reference(s):

- [Dinobase homepage](https://dinobase.ai)
- [ClawHub skill page](https://clawhub.ai/kappa90/skills/dinobase)
- [Publisher profile](https://clawhub.ai/user/kappa90)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands generally produce JSON by default; write-back mutations use a preview and confirmation flow.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
