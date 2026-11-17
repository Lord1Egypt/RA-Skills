## Description:

Get AI ecosystem intelligence from AgentWyre for breaking changes, security vulnerabilities, new model releases, pricing updates, AI news, and sourced signals across the AI ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tcd004](https://clawhub.ai/user/tcd004)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to query AgentWyre for current AI ecosystem intelligence, including release signals, breaking changes, security advisories, pricing information, and service status. It supports both unauthenticated free-tier checks and authenticated AgentWyre API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated workflows use AGENTWYRE_API_KEY and send requests to agentwyre.ai.

Mitigation: Treat AGENTWYRE_API_KEY as a secret, use a scoped and revocable key, and avoid sharing command output that may expose account details.

Risk: The optional MCP setup invokes an unpinned npm package with npx.

Mitigation: Pin and review the agentwyre-mcp package before use, or run it in a restricted environment.

## Reference(s):

- [AgentWyre FAQ](https://agentwyre.ai/faq)
- [AgentWyre service API](https://agentwyre.ai)
- [ClawHub AgentWyre skill page](https://clawhub.ai/tcd004/skills/agentwyre)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with API response summaries and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON API responses, AgentWyre tiers, and user-approved action recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
