## Description:

Connect to Civic Nexus MCP for 100+ integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[civictechuser](https://clawhub.ai/user/civictechuser)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Civic Nexus to connect OpenClaw agents to Civic Nexus MCP integrations, list or search available tools, inspect schemas, and call external-service tools through mcporter or the TypeScript fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad access to connected services through a Nexus bearer token.

Mitigation: Use a least-privilege Nexus token and profile, and require explicit review before write, delete, posting, database, email, or storage actions.

Risk: A changed MCP destination or unpinned command path can alter what service or code the agent uses.

Mitigation: Keep NEXUS_URL on the official HTTPS Nexus endpoint and prefer pinned, reviewed installations for mcporter or npx-based execution.

## Reference(s):

- [Civic Nexus documentation](https://docs.civic.com)
- [Civic Nexus](https://nexus.civic.com)
- [ClawHub skill page](https://clawhub.ai/civictechuser/skills/civic-nexus-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; the tool runner emits text or JSON from MCP calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEXUS_URL and NEXUS_TOKEN; can use either mcporter or npx.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
