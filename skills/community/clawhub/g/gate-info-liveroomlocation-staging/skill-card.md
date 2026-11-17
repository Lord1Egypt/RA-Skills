## Description:

Gate live stream and replay listing skill for finding live rooms or replays by tag, coin, sort order, or count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Gate live stream and replay listings by category, coin symbol, popularity or recency, and result count.

### Deployment Geography for Use:

Global except Gate-restricted regions such as the US, Canada, and Japan.

## Known Risks and Mitigations:

Risk: Users in Gate-restricted regions may not be able to access live or replay listing data.

Mitigation: Check for restricted regions such as the US, Canada, and Japan before making the request, and return an availability message instead of calling the API.

Risk: Unavailable endpoints or empty responses could otherwise lead to misleading live or replay listings.

Mitigation: Return concise no-result or setup guidance and do not fabricate entries.

## Reference(s):

- [Gate Info Liveroom Location ClawHub page](https://clawhub.ai/gaixianggeng/skills/gate-info-liveroomlocation-staging)
- [Gate Live Room Location MCP Specification](artifact/references/mcp.md)
- [Gate Info Liveroom Location Runtime Rules](artifact/references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](artifact/references/info-news-runtime-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown list with live or replay labels, titles, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limited to up to 10 entries; returns concise no-result or availability guidance when needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
