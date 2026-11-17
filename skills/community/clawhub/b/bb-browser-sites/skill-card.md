## Description:

Turn any website into a CLI command across 36 platforms and 103 commands, using OpenClaw's browser directly without an extra extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yan5xu](https://clawhub.ai/user/yan5xu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run website-specific bb-browser commands for structured data extraction, search, recommendations, and adapter discovery through OpenClaw's browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Community adapters may change over time and run in an authenticated browser context.

Mitigation: Review adapters before installing or updating them, and update only from sources the operator trusts.

Risk: Authenticated browser sessions may expose sensitive accounts or data to website automation.

Mitigation: Use a separate browser profile or low-privilege accounts when running site commands.

Risk: The security evidence flags unclear integrity and capability controls for downloaded adapters.

Mitigation: Treat new or unknown adapters as untrusted until scanned, reviewed, and tested in a constrained environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yan5xu/skills/bb-browser-sites)
- [ClawHub publisher profile](https://clawhub.ai/user/yan5xu)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Guidance, Configuration]

**Output Format:** [Markdown guidance with inline shell commands; bb-browser commands may emit text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the bb-browser binary and OpenClaw browser context; site commands are expected to use --openclaw.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
