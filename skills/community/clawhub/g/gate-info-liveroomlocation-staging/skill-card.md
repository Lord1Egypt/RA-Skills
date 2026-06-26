## Description: <br>
Gate live stream and replay listing skill for finding live rooms or replays by tag, coin, sort order, or count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request Gate live stream and replay lists filtered by topic tag, coin symbol, popularity, recency, or result count. Agents use it to call the documented Gate Info MCP endpoint and return a concise markdown list of titles and links. <br>

### Deployment Geography for Use: <br>
Global except restricted Gate regions such as the United States, Canada, and Japan <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a configured Gate Info MCP server, so an untrusted or unavailable server can produce missing or unreliable listings. <br>
Mitigation: Install only in environments that trust the configured Gate Info MCP server and degrade gracefully when the endpoint is unavailable. <br>
Risk: Region restrictions can make the live and replay feature unavailable for users in locations such as the United States, Canada, or Japan. <br>
Mitigation: Apply the documented restricted-region block before calling the endpoint when user region is known, and avoid guessing location when it is not clear. <br>
Risk: Creator-provided live and replay content may be mistaken for financial or viewing advice. <br>
Mitigation: Return neutral listing output only and include a disclaimer when needed that creator content is not investment advice. <br>


## Reference(s): <br>
- [Gate runtime rules](references/gate-runtime-rules.md) <br>
- [Info and news runtime rules](references/info-news-runtime-rules.md) <br>
- [Gate live room MCP specification](references/mcp.md) <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-info-liveroomlocation-staging) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown list with live or replay labels, titles, and Gate links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies default filters when omitted, limits results to 10, and returns concise no-result or availability messages when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
