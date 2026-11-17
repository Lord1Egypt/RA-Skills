## Description:

Provides real-time AI frontier intelligence through a remote MCP integration, including FP Line scores, intelligence feeds, labor displacement data, investment signals, gap opportunities, daily briefings, and agent economy tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamessunheart](https://clawhub.ai/user/jamessunheart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query a remote MCP service for current AI frontier intelligence, briefings, labor displacement tracking, investment allocation signals, and opportunity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends queries and submitted reports to fullpotential.ai through a remote MCP service.

Mitigation: Avoid entering secrets, confidential material, or sensitive business data unless the service has been approved for that use.

Risk: The setup shown in the artifact runs an unpinned npm package through npx.

Mitigation: Use a pinned, audited mcp-remote version in a constrained environment with minimal exposed credentials.

Risk: The server security verdict is suspicious because external data-sharing behavior is under-disclosed.

Mitigation: Review the skill before installation and only deploy it where outbound access to fullpotential.ai is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jamessunheart/skills/fp-intelligence)
- [Publisher Profile](https://clawhub.ai/user/jamessunheart)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and text responses with MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return current intelligence, rankings, scores, summaries, submitted report outcomes, and metered analysis results from the remote service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
