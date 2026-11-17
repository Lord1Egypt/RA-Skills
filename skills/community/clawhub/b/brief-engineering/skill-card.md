## Description:

Technical daily brief for engineers: service health, deploys, alerts, DLQ/latency, workflows, migrations, customer signals. Use for engineering/on-call briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vmishra-atlassian](https://clawhub.ai/user/vmishra-atlassian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, on-call responders, engineering managers, and PMs use this skill to turn delegated work, service health, deploy, alert, migration, customer, and communication signals into a daily engineering brief with ordered next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated service names, aliases, or signal-pack values could broaden searches or alter command and query behavior.

Mitigation: Confirm service scope before use, avoid aliases containing quotes, wildcards, shell metacharacters, or query operators, and revise query construction to validate identifiers and use escaping or parameterization.

Risk: Connector gaps or failed runtime routes could be mistaken for healthy services.

Mitigation: Require the brief's per-source coverage table to distinguish checked, not registered, failed, blocked, stale, and runtime unavailable states for each run.

Risk: Copied per-user memory or signal-pack configuration could report another person's services or operational channels.

Mitigation: Install only the skill files, keep per-user scope in memory separate from team signal packs, and reconfirm scope from delegated identity and Compass ownership.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vmishra-atlassian/skills/brief-engineering)
- [README](README.md)
- [Signal catalogue](references/signal-catalog.md)
- [Operational connector authentication](references/connector-auth.md)
- [Team signal pack contract](references/signal-packs.md)
- [Local operational relay](references/local-operational-relay.md)
- [Persona presentation policy](references/personas.md)
- [Rolling this out to a team](references/team-adoption.md)
- [Sharing this with a teammate](references/install-for-teammates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown brief or dashboard with ordered actions, evidence links, coverage status, and optional setup commands/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visible output is capped and grouped by concern; connector coverage is reported for the current run.]

## Skill Version(s):

1.0.7 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
