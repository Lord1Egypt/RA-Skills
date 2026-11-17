## Description:

See the user's iPhone or iPad screen by setting up a local AirPlay receiver, registering it as an MCP server, and reading mirrored frames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feedthedogs](https://clawhub.ai/user/feedthedogs)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to set up AirPlay screen mirroring from an iPhone or iPad and let an agent inspect, follow, or save the displayed screen. The phone and computer need to share a Wi-Fi network that permits local discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mirrored screen content may be shared with the connected AI service even when AirPlay reception is local.

Mitigation: Only mirror content you are comfortable sharing, and account for where the AI service processes it.

Risk: Saved screenshots can retain sensitive screen information after mirroring ends.

Mitigation: Manage saved screenshots and stop mirroring when finished.

Risk: Using an untrusted network or changing dependencies without review can increase privacy or dependency risk.

Mitigation: Use a trusted network and consider pinning reviewed dependency versions.

## Reference(s):

- [AirPlay MCP project](https://github.com/feedthedogs/airplay-mcp)
- [UxPlay project](https://github.com/FDH2/UxPlay)
- [ipsw project and releases](https://github.com/blacktop/ipsw)
- [apfs-fuse project](https://github.com/sgan81/apfs-fuse)
- [AirPlay Screen on ClawHub](https://clawhub.ai/feedthedogs/skills/airplay-screen)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, shell commands, configuration snippets, screen observations, and saved image paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can inspect changing screen frames or save a full-resolution screenshot.]

## Skill Version(s):

0.1.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
