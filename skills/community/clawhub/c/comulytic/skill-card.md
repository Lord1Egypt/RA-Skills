## Description:

Comulytic helps agents query Comulytic meetings, contacts, action items, and conversation history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenbaochao](https://clawhub.ai/user/chenbaochao)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or external users who rely on Comulytic use this skill to retrieve meeting summaries, transcripts, contact profiles, meeting history, action items, and conversation search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved Comulytic MCP access tokens can expose meeting, transcript, contact, action-item, and conversation data if mishandled.

Mitigation: Treat the token file and COMULYTIC_MCP_TOKEN as sensitive, keep token access limited to the user account, and avoid showing token status in shared or logged terminals.

Risk: Shell examples that interpolate user-supplied search text can mishandle quotes or special characters.

Mitigation: Prefer hardened commands or scripts that serialize API arguments as JSON instead of substituting raw user text into shell snippets.

Risk: The skill can query sensitive Comulytic meeting summaries, transcripts, contacts, action items, and conversation history.

Mitigation: Install and use it only for accounts and workspaces where the publisher and requested data access are trusted.

## Reference(s):

- [Comulytic Skill Release](https://clawhub.ai/chenbaochao/skills/comulytic)
- [Comulytic MCP API Endpoint](https://api.comulytic.ai/mcp)
- [Comulytic API Service](https://api.comulytic.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-RPC curl examples and parsed JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, python3, and a valid Comulytic MCP access token.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
