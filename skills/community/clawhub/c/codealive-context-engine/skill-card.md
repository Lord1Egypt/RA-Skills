## Description:

CodeAlive Context Engine provides semantic code search and AI-powered codebase Q&A across indexed repositories for code understanding, dependency exploration, pattern discovery, feature planning, debugging, and onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rodion-m](https://clawhub.ai/user/rodion-m)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover indexed repositories, run semantic searches, fetch search result content, and ask CodeAlive's codebase consultant for architectural explanations or implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if pasted into chat, command lines, shell history, transcripts, or logs.

Mitigation: Use the hidden interactive setup or an OS credential store where possible, avoid passing keys directly in chat or command arguments, and rotate any key that may already have been exposed.

Risk: A custom CODEALIVE_BASE_URL can send credentials and codebase queries to an untrusted endpoint.

Mitigation: Use the default CodeAlive endpoint or set CODEALIVE_BASE_URL only to a trusted HTTPS CodeAlive endpoint.

Risk: Repository names, queries, search results, and fetched artifact content may be sent to CodeAlive during normal use.

Mitigation: Install and use the skill only for repositories and questions that are appropriate to share with CodeAlive.

## Reference(s):

- [Query Patterns](references/query-patterns.md)
- [Workflows](references/workflows.md)
- [CodeAlive MCP Server](https://github.com/CodeAlive-AI/codealive-mcp)
- [CodeAlive App](https://app.codealive.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CodeAlive API key; search, fetch, data source, chat, and exploration operations call the configured CodeAlive API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
