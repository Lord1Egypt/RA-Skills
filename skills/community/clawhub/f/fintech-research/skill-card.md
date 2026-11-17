## Description:

A self-hosted equity research toolkit for Claude Code that supports US, Hong Kong, and China-related market analysis with reusable research commands and a local MCP data server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredtai](https://clawhub.ai/user/fredtai)

### License/Terms of Use:

Apache License 2.0

## Use Case:

External users and developers use this skill to screen themes, research single companies, monitor theses or watchlists, and compare market or macro conditions across US, Hong Kong, and China-linked equities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an unsafe raw SQL tool and writable local cache behavior.

Mitigation: Run the skill in a dedicated project or virtual environment, review SQL before execution, and disable or restrict the SQL tool when it is not needed.

Risk: The security evidence notes that sensitive portfolio thesis data may be persisted without clear controls.

Mitigation: Avoid entering private account details or sensitive holdings, keep watchlists non-sensitive, and clear local cache data after research sessions when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fredtai/skills/fintech-research)
- [Publisher Profile](https://clawhub.ai/user/fredtai)
- [README](README.md)
- [MCP Tools Reference](docs/tools.md)
- [Data Sources](docs/data-sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell commands, configuration snippets, and structured research outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use optional FRED_API_KEY and NEWS_API_KEY environment variables for enhanced macro and news data.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
