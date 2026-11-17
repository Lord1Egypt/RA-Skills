## Description:

Manage Freshservice tickets, requesters, agents, assets, changes, problems, and service catalog data via the Freshservice API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, IT service teams, and developers use this skill to inspect and manage Freshservice tickets, requesters, agents, assets, locations, problems, changes, releases, and service catalog items through connected Freshservice tooling. Write and delete operations are intended to be previewed and confirmed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned third-party plugin that handles Freshservice credentials and business data.

Mitigation: Review the ClawLink plugin source, publisher, version, and integrity guarantees before installing or allowing the plugin.

Risk: Freshservice API actions may expose or modify tickets, assets, changes, problems, requesters, agents, and service catalog data accessible to the connected account.

Mitigation: Use a Freshservice account with the least privileges needed for the task and confirm every write or delete preview before execution.

## Reference(s):

- [Freshservice API Documentation](https://api.freshservice.com/)
- [Freshservice Ticket API](https://api.freshservice.com/v2/tickets.html)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [Freshservice Skill Page](https://clawhub.ai/hith3sh/skills/freshservice-it)
- [Publisher Profile](https://clawhub.ai/user/hith3sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands and JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live Freshservice tool catalog as the source of truth and requires confirmation for write or delete actions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
