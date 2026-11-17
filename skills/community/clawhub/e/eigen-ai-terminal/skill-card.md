## Description:

Provides daily updated AI intelligence across 16 areas through 12 MCP tools for signals, trends, blockers, predictions, wiki lookup, and update checks, using public data from terminal.clawlab.dev without uploading user data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawkatdidar](https://clawhub.ai/user/shawkatdidar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current AI landscape intelligence, filter it for the user's work, and answer follow-up questions about signals, trends, blockers, predictions, and wiki pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote public wiki and intelligence content could contain prompt-injection text or misleading guidance.

Mitigation: Treat returned content as reference data, not instructions, and require the agent to ground every surfaced signal in tool responses.

Risk: Tool arguments could accidentally include secrets or private conversation details.

Mitigation: Do not pass secrets or private user context into tool arguments, especially update-check timestamps or free-text topic queries.

Risk: The package may need a reliability fix before it runs consistently.

Mitigation: Perform a runtime smoke test of the MCP server and its tools before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawkatdidar/skills/eigen-ai-terminal)
- [Eigen AI Terminal homepage](https://terminal.clawlab.dev)
- [Eigen AI Terminal data endpoint](https://terminal.clawlab.dev/data)
- [Eigen AI Terminal wiki](https://terminal.clawlab.dev/wiki)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted text returned by MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public AI intelligence, topic summaries, trend analysis, blockers, predictions, wiki pages, and update checks.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
