## Description:

Query eventbrite.com from a shell — your tickets/orders, your organizations' events and attendees via the documented token API (curl), and public event discovery/search via the fpx browser bridge (the search API is WAF-walled and absent from the documented API). Use when you want Eventbrite data without an MCP server, in a script, or one-shot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and event organizers use the skill to retrieve Eventbrite account, ticket, organization, and public event data from shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Eventbrite tokens and paired browser access can expose account data, including tickets and attendee information.

Mitigation: Use the intended account, keep the token private, grant only necessary permissions, and revoke persistent pairing when it is no longer needed.

Risk: The external CLI and browser extension binaries were not audited in the release evidence.

Mitigation: Verify CLI and extension versions before installation.

## Reference(s):

- [Documented Eventbrite API recipes](references/token-api.md)
- [Event discovery API recipes](references/discovery-api.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with shell commands and jq recipes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Eventbrite requests return structured JSON data.]

## Skill Version(s):

1.2.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
