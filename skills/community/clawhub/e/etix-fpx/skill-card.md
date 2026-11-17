## Description:

Query etix.com (event ticketing) from a shell with the fpx CLI (@fetchproxy/cli) instead of running the etix-mcp server — search events, venues, and performers, and pull event/venue detail, via one-shot calls through a signed-in browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search public Etix events, venues, and performers and retrieve event or venue details from shell scripts without running the etix-mcp server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser pairing persists and enables fetch access through the connected browser extension.

Mitigation: Approve only etix.com fetch access, use an unsigned-in Etix tab for public discovery, and remove pairing when it is no longer needed.

Risk: The CLI, extension, and their dependency releases are outside the review of the bundled artifact.

Mitigation: Verify the extension archive using its published SHA-256 checksum or build it from source, and assess separately downloaded releases before installation.

## Reference(s):

- [Etix consumer endpoints for fpx](references/etix-endpoints.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [fetchproxy extension setup](https://github.com/chrischall/fetchproxy#extension)

## Skill Output:

**Output Type(s):** [JSON, HTML, Shell commands, Guidance]

**Output Format:** [Etix JSON responses or server-rendered HTML, with Markdown instructions and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Event, venue, and performer discovery data; event and venue detail]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
