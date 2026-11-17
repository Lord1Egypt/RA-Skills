## Description:

Uses aria2 over RPC to download magnet links, torrent files, and HTTP files, with an optional completion workflow that transfers downloads to 115 cloud storage and removes local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahiven](https://clawhub.ai/user/ahiven)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage aria2 download tasks through JSON-RPC commands for magnet links, torrent files, and HTTP downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill publishes a fixed aria2 RPC token in command examples.

Mitigation: Replace the token before use, rotate any exposed secret, and prefer environment-specific secret handling.

Risk: aria2 RPC access can control downloads if reachable by unauthorized users.

Mitigation: Bind RPC to localhost or otherwise restrict network access, and install only when you control the aria2 daemon.

Risk: The documented completion workflow may transfer files to 115 cloud storage and delete local copies.

Mitigation: Require explicit confirmation before cloud transfer or local deletion and review the host-side completion hook separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahiven/skills/aria2)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON-RPC command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a user-controlled aria2 JSON-RPC daemon.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
