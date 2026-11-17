## Description:

Find serviced apartments and hotels for extended stays, including weekly or monthly rates, kitchenettes, laundry, and home-like amenities for long-term travelers, powered by Fliggy through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search extended-stay hotels and serviced apartments, collect required travel parameters, run flyai CLI hotel searches, and return concise booking-ready results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global flyai CLI.

Mitigation: Review and approve the CLI supply chain before installation; prefer pinned, audited, or sandboxed execution where possible.

Risk: The skill can persist raw travel queries in an execution log.

Mitigation: Disable persistence unless needed, and redact destinations, dates, traveler details, and other sensitive query content before storing logs.

Risk: The skill returns provider booking links and travel-provider branding.

Mitigation: Confirm that results, prices, and booking URLs came from flyai CLI output and clearly treat provider links as third-party booking destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/extended-stay)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise travel guidance with booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel data and booking links; should not return raw JSON.]

## Skill Version(s):

v3.2.4 (source: server release evidence; artifact frontmatter states 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
