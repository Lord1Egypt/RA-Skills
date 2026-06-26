## Description: <br>
Gate live stream and replay listing skill for finding live rooms or replays by tag, coin, sort order, or count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve Gate live stream and replay listings by tag, coin, sort order, and count through the Gate Info MCP integration. <br>

### Deployment Geography for Use: <br>
Global, excluding Gate-restricted regions such as the US, Canada, and Japan. <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact Gate for public live and replay listing data. <br>
Mitigation: Use only the documented read-only Gate Info MCP endpoint and do not request secrets or trading permissions. <br>
Risk: Gate live and replay features may be unavailable in restricted regions. <br>
Mitigation: Block use before calling the API when the user is in restricted regions such as the US, Canada, or Japan. <br>
Risk: Creator-provided live or replay content could be mistaken for investment advice. <br>
Mitigation: Return neutral listing output, preserve the skill disclaimer when needed, and avoid explicit buy or sell advice. <br>


## Reference(s): <br>
- [Gate Live Room Location MCP Specification](references/mcp.md) <br>
- [Gate Info Liveroom Location Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-info-liveroomlocation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown list with live/replay labels, titles, and Gate links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits listings to 1-10 items, preserves live versus replay link formats, and avoids fabricated entries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter: 2026.4.8-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
