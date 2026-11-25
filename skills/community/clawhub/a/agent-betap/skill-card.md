## Description:

Connect an AI agent to the live BETAP map to visit real places, care for a virtual pet, and use optional business tools when authorized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavierabraham](https://clawhub.ai/user/xavierabraham)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use BETAP's MCP service to appear and move on its live map, visit listed places, interact with a virtual pet, and support linked businesses when separately authorized.

### Deployment Geography for Use:

Los Altos de Jalisco, Mexico (the real places represented on the BETAP map)

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious because reported device-wide display controls appear broader than its map and virtual-pet purpose; its analysis was partial.

Mitigation: Review the full tool permissions and instructions before installing, and only enable device controls when you intend to use them.

Risk: The skill uses a BETAP key and sends requests and related information to BETAP services.

Mitigation: Keep the key secret and use the service only if you trust BETAP with the key and information sent to it.

## Reference(s):

- [BETAP World](https://betap.world/en)
- [BETAP world MCP endpoint](https://api.betap.world/api/mcp/mundo)
- [BETAP public read-only MCP endpoint](https://api.betap.world/api/mcp)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [MCP tool calls with text and structured service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [World actions require a BETAP_WORLD_KEY; public place search is read-only and does not require a key. Actions operate on live BETAP service state.]

## Skill Version(s):

1.18.2 (source: artifact/SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
