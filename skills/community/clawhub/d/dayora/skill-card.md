## Description:

Lets an agent use a person's Dayora journal through Dayora's MCP server, with permission, including setup guidance, entry and mood updates, and review of entries and mood history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thedelisle](https://clawhub.ai/user/thedelisle)

### License/Terms of Use:

MIT-0

## Use Case:

External users can connect an AI agent to their Dayora journal to add entries or moods and review existing entries and mood history. The skill guides connection setup and user-controlled access to a private journal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because one local reference was unresolved, so the scan evidence is incomplete.

Mitigation: Resolve and review the referenced material before relying on this release.

Risk: Connecting the skill can expose private journal entries to the agent; a bearer key grants access to the whole journal.

Mitigation: Prefer sign-in and read-only access, ask before each journal tool call, never request or store a key in chat or shared files, and revoke access when it is no longer needed.

## Reference(s):

- [Dayora](https://www.dayora.ai/?utm_source=clawhub&utm_medium=agent_skill)
- [Dayora connection guide](https://www.dayora.ai/how-to/connect-claude-chatgpt?utm_source=clawhub&utm_medium=agent_skill)
- [Dayora MCP server](https://www.dayora.ai/api/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell commands and natural-language journal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Journal access may be read-only or read/write; writing requires user direction and permission.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
