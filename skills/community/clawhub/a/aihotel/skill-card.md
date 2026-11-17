## Description:

AI Go Hotel helps agents search hotels, compare prices, inspect room-rate details, and fetch hotel tag metadata through the AIGoHotel MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiao101660](https://clawhub.ai/user/qiao101660)

### License/Terms of Use:


## Use Case:

Travel-focused agents use this skill to help users find hotels by destination, dates, rating, guests, budget, tags, and brands, then summarize real-time prices, room options, cancellation policies, and booking links returned by the MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged MCP configuration includes a reusable bearer token.

Mitigation: Remove or rotate the packaged token before use and configure per-user secrets outside the artifact.

Risk: Hotel search queries may contain sensitive travel details.

Mitigation: Avoid sending unnecessary sensitive personal details in raw hotel queries and review data-sharing expectations before use.

Risk: The optional local server setup is not pinned to a reviewed revision with locked dependencies.

Mitigation: Run the local server only from a pinned, reviewed source revision with locked dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiao101660/skills/aihotel)
- [Publisher profile](https://clawhub.ai/user/qiao101660)
- [AIGoHotel MCP endpoint](https://mcp.aigohotel.com/mcp)
- [MCP standard](https://modelcontextprotocol.io/)
- [AIGoHotel API key application](https://mcp.agentichotel.cn/apply)
- [Artifact README](artifact/README_EN.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown with structured hotel summaries and JSON-style MCP call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include real-time hotel availability, prices, room-rate details, cancellation policy summaries, and booking links when returned by the MCP service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
