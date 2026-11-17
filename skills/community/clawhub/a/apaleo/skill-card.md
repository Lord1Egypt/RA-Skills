## Description:

Apaleo hotel property management API integration with managed OAuth. Manage properties, units, unit groups, and unit attributes. Use this skill when users want to list hotel properties, create rooms and units, check availability, or manage property inventory in Apaleo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and hospitality teams use this skill to connect an agent to Apaleo through ClawLink OAuth and manage hotel properties, units, unit groups, and unit attributes. It supports both read workflows, such as listing properties and checking inventory, and high-impact write workflows, such as creating units, archiving properties, cloning properties, and deleting inventory records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned third-party plugin that can access Apaleo through managed OAuth.

Mitigation: Install only if the ClawLink publisher and plugin are trusted, and review the plugin source and allowlist before deployment.

Risk: Write-capable tools can perform high-impact property and inventory changes, including create, delete, archive, reset, clone, and move-to-live operations.

Mitigation: Require human confirmation before destructive or administrative actions and separate read-only from administrative access where possible.

Risk: Broad Apaleo OAuth scopes can expand the impact of a mistaken or unauthorized action.

Mitigation: Prefer minimal Apaleo scopes for the intended workflow and grant elevated scopes only when operationally required.

## Reference(s):

- [Apaleo API Docs](https://apaleo.com/api/)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Apaleo Connection](https://claw-link.dev/dashboard?add=apaleo)
- [ClawHub Apaleo Skill Page](https://clawhub.ai/hith3sh/skills/apaleo)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands, tool names, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ClawLink OAuth connection and Apaleo scopes for protected write operations.]

## Skill Version(s):

1.0.1 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
