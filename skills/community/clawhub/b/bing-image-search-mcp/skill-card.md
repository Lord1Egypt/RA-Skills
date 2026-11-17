## Description:

Provides Bing image search tools through OneKey Gateway for single and batch query workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Bing image search queries through OneKey Gateway, either for one query or a batch of queries, and receive image result metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install unpinned third-party npm and Python packages.

Mitigation: Use an isolated environment and pin, review, and verify package versions before installing or running the skill.

Risk: The scripts fall back to a shared demo OneKey Gateway key when no key is provided.

Mitigation: Provide a least-privilege OneKey Gateway key with the DEEPNLP_ONEKEY_ROUTER_ACCESS environment variable and avoid relying on the demo key.

Risk: Image search queries may expose sensitive or regulated text to external services.

Mitigation: Do not submit secrets, personal data, or regulated data in search queries.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ai-hub-admin/skills/bing-image-search-mcp)
- [OneKey MCP Router documentation](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway documentation](https://deepnlp.org/doc/onekey_agent_router)
- [AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Code, Configuration, Guidance]

**Output Format:** [JSON image result metadata with Markdown usage guidance and shell/Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image results include title, thumbnail_url, and url fields; batch mode accepts a list of search queries.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
