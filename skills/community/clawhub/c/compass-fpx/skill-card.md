## Description:

Query compass.com (US real-estate portal) from a shell with the fpx CLI (@fetchproxy/cli) instead of running the compass-mcp server — search listings, get property/agent detail, price history, and resolve street addresses through one-shot fetches over a signed-in browser tab. Use when you want Compass data without the MCP, in a script, or on a machine where the MCP isn't installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use the skill to search Compass listings, retrieve property and agent details or price history, and resolve street addresses from shell workflows without setting up the Compass MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Address searches are sent to Compass through the signed-in browser session.

Mitigation: Avoid submitting confidential addresses unless you are authorized to share them.

Risk: The external CLI and browser extension use a paired session, and fetched page data may be saved locally.

Mitigation: Use them only if you trust both tools, grant only Compass access, revoke pairing when finished, and protect saved data.

Risk: External dependency binaries and live runtime enforcement were not verified.

Mitigation: Review and verify the external CLI and extension releases before installing or using them.

## Reference(s):

- [Compass](https://www.compass.com)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [Compass request recipes](references/requests.md)
- [Embedded data extraction helper](references/extract-global.mjs)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/compass-fpx)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text]

**Output Format:** [Shell commands with extracted Compass data as JSON or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on Compass responses and an available paired browser session.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
